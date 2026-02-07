from __future__ import annotations
import argparse, json, random, string
from sqlalchemy import create_engine, text
from cdc_pipeline.http import post_json
from cdc_pipeline.consumer import consume
from cdc_pipeline.config import settings
from cdc_pipeline.warehouse_duckdb import DuckDBWarehouse

def cmd_register(args):
    with open(args.config, "r", encoding="utf-8") as f:
        payload = json.load(f)
    res = post_json(f"{args.connect_url.rstrip('/')}/connectors", payload)
    print(res)

def _rand(prefix: str, n: int = 3) -> str:
    return prefix + "-" + "".join(random.choice(string.digits) for _ in range(n))

def cmd_seed(args):
    engine = create_engine(args.pg_url, pool_pre_ping=True)
    with engine.begin() as conn:
        for _ in range(args.inserts):
            cid = _rand("c", 3)
            conn.execute(text("""
            INSERT INTO public.customers(customer_id, email, plan, country, status)
            VALUES (:cid, :email, :plan, :country, :status)
            ON CONFLICT (customer_id) DO UPDATE SET
              email=EXCLUDED.email, plan=EXCLUDED.plan, country=EXCLUDED.country, status=EXCLUDED.status, updated_at=NOW();
            """), {
                "cid": cid,
                "email": f"{cid}@example.com",
                "plan": random.choice(["FREE","PRO","ENT"]),
                "country": random.choice(["NG","GH","KE","ZA"]),
                "status": random.choice(["ACTIVE","SUSPENDED"]),
            })

        for _ in range(args.updates):
            conn.execute(text("""
            UPDATE public.customers SET plan=:plan, updated_at=NOW()
            WHERE customer_id IN (SELECT customer_id FROM public.customers ORDER BY random() LIMIT 1);
            """), {"plan": random.choice(["FREE","PRO","ENT"])})

        for _ in range(args.deletes):
            conn.execute(text("""
            DELETE FROM public.customers
            WHERE customer_id IN (SELECT customer_id FROM public.customers ORDER BY random() LIMIT 1);
            """))

    print({"seeded": True, "inserts": args.inserts, "updates": args.updates, "deletes": args.deletes})

def cmd_consume(args):
    print(consume(topic=args.topic or settings.topic, group=args.group or settings.group, max_messages=args.max_messages))

def cmd_query(args):
    wh = DuckDBWarehouse(settings.duckdb_path)
    df = wh.query_customers(limit=args.limit)
    print(df.to_string(index=False))
    wh.close()

def main():
    p = argparse.ArgumentParser(prog="cdc-dw")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register-connector")
    r.add_argument("--connect-url", required=True)
    r.add_argument("--config", required=True)
    r.set_defaults(fn=cmd_register)

    s = sub.add_parser("seed")
    s.add_argument("--pg-url", required=True)
    s.add_argument("--inserts", type=int, default=10)
    s.add_argument("--updates", type=int, default=5)
    s.add_argument("--deletes", type=int, default=2)
    s.set_defaults(fn=cmd_seed)

    c = sub.add_parser("consume")
    c.add_argument("--topic")
    c.add_argument("--group")
    c.add_argument("--max-messages", type=int, default=0)
    c.set_defaults(fn=cmd_consume)

    q = sub.add_parser("query")
    q.add_argument("--limit", type=int, default=50)
    q.set_defaults(fn=cmd_query)

    args = p.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()

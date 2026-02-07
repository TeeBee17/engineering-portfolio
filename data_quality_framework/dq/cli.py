import argparse
from dq.config import settings
from dq.db import SessionLocal, init_db
from dq.rules import load_rules
from dq.batch import read_csv, run_batch_checks
from dq.stream import stream_consume_and_validate
from dq.alerts import derive_alerts
from dq import repo
from dq.producer import produce_orders

def cmd_batch(args):
    init_db()
    rules = load_rules(args.rules)
    rows = read_csv(args.input)
    db = SessionLocal()
    try:
        run = repo.create_run(db, rules.dataset, "batch")
        results = run_batch_checks(rows, rules)
        repo.add_results(db, run.run_id, rules.dataset, results)
        alerts = derive_alerts(rules.dataset, results)
        repo.add_alerts(db, run.run_id, rules.dataset, alerts)
        status = "SUCCESS" if all(r["passed"] for r in results) else "FAILED"
        summary = {"total_rows": len(rows), "failed_checks": [r["check_name"] for r in results if not r["passed"]], "alerts": len(alerts)}
        repo.finish_run(db, run.run_id, status, summary)
        print({"run_id": str(run.run_id), "status": status, "alerts": alerts})
    finally:
        db.close()

def cmd_stream(args):
    init_db()
    rules = load_rules(args.rules)
    db = SessionLocal()
    try:
        run = repo.create_run(db, rules.dataset, "stream")
        results = stream_consume_and_validate(rules, args.topic, args.bootstrap, args.group, max_messages=args.max_messages)
        repo.add_results(db, run.run_id, rules.dataset, results)
        alerts = derive_alerts(rules.dataset, results)
        repo.add_alerts(db, run.run_id, rules.dataset, alerts)
        status = "SUCCESS" if all(r["passed"] for r in results) else "FAILED"
        summary = {"topic": args.topic, "max_messages": args.max_messages, "failed_checks": [r["check_name"] for r in results if not r["passed"]], "alerts": len(alerts)}
        repo.finish_run(db, run.run_id, status, summary)
        print({"run_id": str(run.run_id), "status": status, "alerts": alerts})
    finally:
        db.close()

def cmd_produce(args):
    produce_orders(args.bootstrap, args.topic, args.count)
    print({"produced": args.count, "topic": args.topic})

def main():
    p = argparse.ArgumentParser(prog="dq")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("batch")
    b.add_argument("--input", required=True)
    b.add_argument("--rules", default=settings.RULES_PATH)
    b.set_defaults(fn=cmd_batch)

    s = sub.add_parser("stream")
    s.add_argument("--topic", required=True)
    s.add_argument("--bootstrap", default=settings.KAFKA_BOOTSTRAP)
    s.add_argument("--group", default="dq-consumer")
    s.add_argument("--max-messages", type=int, default=50)
    s.add_argument("--rules", default=settings.RULES_PATH)
    s.set_defaults(fn=cmd_stream)

    pr = sub.add_parser("produce")
    pr.add_argument("--topic", required=True)
    pr.add_argument("--bootstrap", default=settings.KAFKA_BOOTSTRAP)
    pr.add_argument("--count", type=int, default=100)
    pr.set_defaults(fn=cmd_produce)

    args = p.parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()

from typing import Dict
import json, time, random
from confluent_kafka import Producer

def produce_orders(bootstrap: str, topic: str, count: int = 100) -> None:
    p = Producer({"bootstrap.servers": bootstrap})
    statuses = ["CREATED","PAID","SHIPPED","DELIVERED","CANCELLED"]
    currencies = ["NGN","USD","EUR"]

    for i in range(count):
        rec: Dict = {
            "order_id": f"o-{10000+i}",
            "customer_id": f"c-{random.randint(1,200)}",
            "amount": random.choice([500,1500,2500,-1,0,9999999]),
            "currency": random.choice(currencies + ["BAD"]),
            "status": random.choice(statuses + ["UNKNOWN"]),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - random.randint(0, 2000))),
            "source": random.choice(["web","whatsapp","pos"]),
        }
        p.produce(topic, json.dumps(rec).encode("utf-8"))
        p.poll(0)
    p.flush()

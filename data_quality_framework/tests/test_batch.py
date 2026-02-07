from dq.rules import Ruleset
from dq.batch import run_batch_checks

def test_batch_uniqueness_and_null_ratio():
    rules = Ruleset(
        dataset="orders",
        description="",
        primary_key=["order_id"],
        fields={"order_id":{"required":True,"type":"string"}, "customer_id":{"required":True,"type":"string"}},
        streaming={},
        batch={"uniqueness":[["order_id"]], "max_null_ratio":{"customer_id":0.0}},
    )
    rows = [{"order_id":"1","customer_id":"c1"}, {"order_id":"1","customer_id":"c2"}, {"order_id":"2","customer_id":""}]
    res = run_batch_checks(rows, rules)
    by = {r["check_name"]: r for r in res}
    assert by["uniqueness:order_id"]["passed"] is False
    assert by["null_ratio:customer_id"]["passed"] is False

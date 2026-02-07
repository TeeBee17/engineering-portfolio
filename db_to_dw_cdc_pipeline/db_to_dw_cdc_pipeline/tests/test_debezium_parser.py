from cdc_pipeline.debezium import parse_debezium_envelope

def test_parse_create():
    env = {"payload":{"op":"c","ts_ms":1000,"source":{"schema":"public","table":"customers"},"before":None,
                      "after":{"customer_id":"c-1","email":"a@x.com","plan":"FREE","country":"NG","status":"ACTIVE"}}}
    ch = parse_debezium_envelope(env)
    assert ch.op == "c"
    assert ch.pk["customer_id"] == "c-1"

def test_parse_delete():
    env = {"payload":{"op":"d","ts_ms":2000,"source":{"schema":"public","table":"customers"},"before":{"customer_id":"c-1"},"after":None}}
    ch = parse_debezium_envelope(env)
    assert ch.op == "d"
    assert ch.pk["customer_id"] == "c-1"

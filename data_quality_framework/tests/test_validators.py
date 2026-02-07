from dq.validators import validate_record

def test_row_validation_catches_required_and_range():
    rules = {
        "order_id": {"required": True, "type": "string"},
        "amount": {"required": True, "type": "number", "min": 0, "max": 10},
        "currency": {"required": True, "type": "string", "enum": ["NGN"]},
    }
    ok, viol = validate_record({"order_id":"o1","amount":"-1","currency":"USD"}, rules)
    assert ok is False
    assert any(v.get("rule") == "min" for v in viol)
    assert any(v.get("rule") == "enum" for v in viol)

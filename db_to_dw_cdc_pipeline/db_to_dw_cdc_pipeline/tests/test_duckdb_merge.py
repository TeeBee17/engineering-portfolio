import tempfile, os
from cdc_pipeline.warehouse_duckdb import DuckDBWarehouse

def test_idempotent_and_delete():
    with tempfile.TemporaryDirectory() as td:
        dbp = os.path.join(td, "wh.duckdb")
        wh = DuckDBWarehouse(dbp)

        change = {"event_id":"e1","op":"c","after":{"customer_id":"c-1","email":"a@x.com","plan":"FREE","country":"NG","status":"ACTIVE"},
                  "before":None,"pk":{"customer_id":"c-1"}}
        wh.apply_customer_change(change, {"topic":"t","partition":0,"offset":1})
        wh.apply_customer_change(change, {"topic":"t","partition":0,"offset":2})  # replay
        df = wh.query_customers(10)
        assert len(df) == 1

        delc = {"event_id":"e2","op":"d","after":None,"before":{"customer_id":"c-1"},"pk":{"customer_id":"c-1"}}
        wh.apply_customer_change(delc, {"topic":"t","partition":0,"offset":3})
        df2 = wh.query_customers(10)
        assert len(df2) == 0

        wh.close()

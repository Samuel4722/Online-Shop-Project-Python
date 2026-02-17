from tortoise.transactions import in_transaction
from .model import Customer

async def iterate_customer_orders(customer_id: int):
    if not await Customer.filter(id=customer_id).exists():
        return

    query = "SELECT * FROM klient_produkty_cursor($1)"
    async with in_transaction() as conn:
        rows = await conn.execute_query_dict(query, [customer_id])
        for row in rows:
            yield {
                "produkt_nazwa": row["produkt_nazwa"],
                "laczna_ilosc": row["laczna_ilosc"]
            }


async def customer_order_stats(customer_id: int):
    query = "SELECT * FROM klient_statystyki_cursor($1)"
    async with in_transaction() as conn:
        rows = await conn.execute_query_dict(query, [customer_id])
        if rows:
            return {
                "liczba_zamowien": rows[0]["liczba_zamowien"],
                "laczna_kwota": float(rows[0]["laczna_kwota"])
            }
        return {"liczba_zamowien": 0, "laczna_kwota": 0.0}


async def calculate_customer_total(customer_id: int):
    query = "SELECT laczna_kwota FROM klient_statystyki_cursor($1)"
    async with in_transaction() as conn:
        rows = await conn.execute_query_dict(query, [customer_id])
        if rows:
            return float(rows[0]["laczna_kwota"])
        return 0.0

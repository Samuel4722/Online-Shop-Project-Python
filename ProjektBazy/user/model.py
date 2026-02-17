from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    role = fields.CharField(max_length=20, default="user")

    class Meta:
        table = "users"


class Customer(Model):
    id = fields.IntField(pk=True, source_field="klient_id")
    first_name = fields.CharField(max_length=50, source_field="imie")
    last_name = fields.CharField(max_length=50, source_field="nazwisko")
    email = fields.CharField(max_length=100, unique=True)
    phone = fields.CharField(max_length=20, null=True, source_field="telefon")
    registered_at = fields.DatetimeField(auto_now_add=True, source_field="data_rejestracji")

    class Meta:
        table = "klienci"


class Product(Model):
    id = fields.IntField(pk=True, source_field="produkt_id")
    name = fields.CharField(max_length=100, source_field="nazwa")
    description = fields.TextField(null=True, source_field="opis")
    price = fields.DecimalField(max_digits=10, decimal_places=2, source_field="cena")
    stock = fields.IntField(default=0, source_field="stan_magazynowy")

    class Meta:
        table = "produkty"


class Order(Model):
    id = fields.IntField(pk=True, source_field="zamowienie_id")
    customer = fields.ForeignKeyField("models.Customer", related_name="orders", source_field="klient_id")
    date = fields.DatetimeField(auto_now_add=True, source_field="data_zamowienia")
    status = fields.CharField(max_length=20, default="Nowe")

    class Meta:
        table = "zamowienia"


class OrderItem(Model):
    id = fields.IntField(pk=True, source_field="pozycja_id")
    order = fields.ForeignKeyField("models.Order", related_name="items", source_field="zamowienie_id")
    product = fields.ForeignKeyField("models.Product", source_field="produkt_id")
    quantity = fields.IntField(source_field="ilosc")
    unit_price = fields.DecimalField(max_digits=10, decimal_places=2, source_field="cena_jednostkowa")

    class Meta:
        table = "pozycje_zamowienia"

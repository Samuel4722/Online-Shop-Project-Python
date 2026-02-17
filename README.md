📦 Projekt zaliczeniowy – Zaawansowane Bazy Danych

Aplikacja backendowa służąca do zarządzania użytkownikami, klientami, produktami, zamówieniami oraz pozycjami zamówień. Projekt wykorzystuje nowoczesny stos technologiczny oparty o FastAPI i PostgreSQL, a także zaawansowane funkcje PL/pgSQL do generowania statystyk klientów.
🚀 Technologie

    FastAPI – REST API

    PostgreSQL – relacyjna baza danych

    Tortoise ORM – mapowanie obiektowo-relacyjne

    asyncpg – szybki driver PostgreSQL

    HTTP Basic Auth – autoryzacja użytkowników

    PL/pgSQL cursors – statystyki klientów

🛠 Uruchamianie projektu
1. Instalacja zależności
bash

pip install -r requirements.txt

2. Uruchomienie serwera
bash

uvicorn main:app --reload

3. Dokumentacja API

Po uruchomieniu aplikacji dokumentacja dostępna jest pod adresem:
Kod

http://127.0.0.1:8000/docs

🔐 Logowanie

Domyślny administrator:

    login: admin

    hasło: samuel

Niektóre endpointy wymagają roli administratora.
🗂 Struktura bazy danych (ERD)
Tabela users

    id (PK)

    login (UNIQUE)

    password

    role

Relacja: 1..* z klientami.
Tabela klienci

    klient_id (PK)

    imie

    nazwisko

    email (UNIQUE)

    telefon

    data_rejestracji

Relacja: 1..* z zamówieniami.
Tabela zamowienia

    zamowienie_id (PK)

    klient_id (FK → klienci)

    data_zamowienia

    status

Relacja: 1..* z pozycjami zamówień.
Tabela pozycje_zamowienia

    pozycja_id (PK)

    zamowienie_id (FK)

    produkt_id (FK)

    ilosc

    cena_jednostkowa

Relacja: \..1* z produktami.
Tabela produkty

    produkt_id (PK)

    nazwa

    opis

    cena

    stan_magazynowy

📡 Endpointy API
🔑 Autoryzacja

API korzysta z HTTP Basic Auth.
Część endpointów wymaga roli admin.
👤 Users
POST /api/users

Tworzy nowego użytkownika.
Body:
json

{
  "login": "string",
  "password": "string"
}

Response:

    id

    login

    role

GET /api/users (admin only)

Zwraca listę użytkowników.
🧾 Customers
POST /api/customers

Tworzy nowego klienta.
json

{
  "first_name": "Jan",
  "last_name": "Kowalski",
  "email": "jan@kowalski.pl",
  "phone": "123456789"
}

GET /api/customers

Lista klientów.
GET /api/customers/{id}/orders

Zwraca listę produktów zamówionych przez klienta (cursor SQL).
GET /api/customers/{id}/stats

Zwraca statystyki klienta:

    liczba zamówień

    łączna kwota

GET /api/customers/{id}/total

Zwraca łączną kwotę zamówień klienta.
📦 Products
POST /api/products (admin only)

Tworzy produkt.
GET /api/products

Lista produktów.
🛒 Orders
POST /api/orders

Tworzy zamówienie.
json

{
  "customer_id": 1
}

GET /api/orders

Lista zamówień.
GET /api/orders/me

Zamówienia zalogowanego użytkownika.
🧩 Order Items
POST /api/order_items

Dodaje pozycję zamówienia.
GET /api/order_items

Lista pozycji zamówień.
🧠 Funkcje PL/pgSQL

Projekt zawiera kursory SQL:

    klient_produkty_cursor

    klient_statystyki_cursor

Służą one do generowania statystyk klientów oraz pobierania danych o zamówieniach.

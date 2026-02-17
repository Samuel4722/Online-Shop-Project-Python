-- ============================
--  Tabela: users
-- ============================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

-- ============================
--  Tabela: klienci
-- ============================
CREATE TABLE klienci (
    klient_id SERIAL PRIMARY KEY,
    imie VARCHAR(50) NOT NULL,
    nazwisko VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    data_rejestracji TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ============================
--  Tabela: produkty
-- ============================
CREATE TABLE produkty (
    produkt_id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    opis TEXT,
    cena NUMERIC(10,2) NOT NULL,
    stan_magazynowy INT NOT NULL DEFAULT 0
);

-- ============================
--  Tabela: zamowienia
-- ============================
CREATE TABLE zamowienia (
    zamowienie_id SERIAL PRIMARY KEY,
    klient_id INT NOT NULL REFERENCES klienci(klient_id) ON DELETE CASCADE,
    data_zamowienia TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Nowe'
);

-- ============================
--  Tabela: pozycje_zamowienia
-- ============================
CREATE TABLE pozycje_zamowienia (
    pozycja_id SERIAL PRIMARY KEY,
    zamowienie_id INT NOT NULL REFERENCES zamowienia(zamowienie_id) ON DELETE CASCADE,
    produkt_id INT NOT NULL REFERENCES produkty(produkt_id),
    ilosc INT NOT NULL CHECK (ilosc > 0),
    cena_jednostkowa NUMERIC(10,2) NOT NULL
);

-- ============================
--  Funkcja: klient_produkty_cursor
-- ============================
CREATE OR REPLACE FUNCTION klient_produkty_cursor(p_klient_id INT)
RETURNS TABLE (
    produkt_nazwa TEXT,
    laczna_ilosc INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.nazwa, SUM(pz.ilosc)
    FROM zamowienia z
    JOIN pozycje_zamowienia pz ON z.zamowienie_id = pz.zamowienie_id
    JOIN produkty p ON pz.produkt_id = p.produkt_id
    WHERE z.klient_id = p_klient_id
    GROUP BY p.nazwa;
END;
$$ LANGUAGE plpgsql;

-- ============================
--  Funkcja: klient_statystyki_cursor
-- ============================
CREATE OR REPLACE FUNCTION klient_statystyki_cursor(p_klient_id INT)
RETURNS TABLE (
    liczba_zamowien INT,
    laczna_kwota NUMERIC(10,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(z.zamowienie_id),
        COALESCE(SUM(pz.ilosc * pz.cena_jednostkowa), 0)
    FROM zamowienia z
    LEFT JOIN pozycje_zamowienia pz ON z.zamowienie_id = pz.zamowienie_id
    WHERE z.klient_id = p_klient_id;
END;
$$ LANGUAGE plpgsql;

-- ============================
--  Dane przykładowe
-- ============================

INSERT INTO klienci (imie, nazwisko, email, telefon) VALUES
('Jan', 'Krawczyk', 'jan.krawczyk@example.com', '501234567'),
('Ewa', 'Maj', 'ewa.maj@example.com', '502345678'),
('Tomasz', 'Lis', 't.lis@example.com', '503456789'),
('Karolina', 'Zielinska', 'karo.ziel@example.com', '504567890'),
('Piotr', 'Lewandowski', 'piotr.lew@example.com', '505678901'),
('Anna', 'Piasecka', 'ania.pia@example.com', '506789012');

INSERT INTO produkty (nazwa, opis, cena, stan_magazynowy) VALUES
('Monitor 24"', 'Monitor LED 24 cale', 699.99, 30),
('Karta Graficzna', 'GPU 8GB', 1899.00, 15),
('Dysk SSD 1TB', 'Dysk NVMe 1TB', 399.99, 40),
('Słuchawki', 'Słuchawki bezprzewodowe', 249.99, 80),
('Laptop Gamingowy', 'Laptop 17" RTX3060', 6999.00, 5),
('Router WiFi', 'Router 5GHz', 159.90, 60),
('Pendrive 64GB', 'USB 3.0 64GB', 29.99, 150),
('Mata pod mysz', 'Duża mata gamingowa', 39.99, 70);

INSERT INTO zamowienia (klient_id, status) VALUES
(3, 'Nowe'),
(4, 'Wysłane'),
(5, 'Zrealizowane'),
(6, 'Nowe'),
(1, 'W trakcie'),
(2, 'Zrealizowane');

INSERT INTO pozycje_zamowienia (zamowienie_id, produkt_id, ilosc, cena_jednostkowa) VALUES
(3, 4, 1, 249.99),
(3, 8, 1, 39.99),
(4, 6, 1, 159.90),
(4, 7, 3, 29.99),
(5, 5, 1, 6999.00),
(5, 2, 1, 1899.00),
(6, 3, 2, 399.99),
(1, 4, 1, 249.99),
(5, 1, 1, 3500.00),
(4, 2, 1, 1899.00),
(2, 7, 5, 29.99),
(1, 3, 1, 399.99);


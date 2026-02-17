--PLIK Z ITERATORAMI 

-- FUNKCJA 1
-- Lista wszystkich produktów zamówionych przez danego klienta
-- Zagnieżdżone kursory: zamówienia -> pozycje zamówień


CREATE OR REPLACE FUNCTION klient_produkty_cursor(p_klient_id INT)
RETURNS TABLE (
    produkt_nazwa TEXT,
    laczna_ilosc INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    rec_zamowienie RECORD;

    cur_zamowienia CURSOR FOR
        SELECT z.zamowienie_id
        FROM zamowienia z
        WHERE z.klient_id = p_klient_id;
BEGIN
    FOR rec_zamowienie IN cur_zamowienia LOOP
        RETURN QUERY
        SELECT
            p.nazwa::TEXT,
            SUM(pz.ilosc)::INT
        FROM pozycje_zamowienia pz
        JOIN produkty p ON p.produkt_id = pz.produkt_id
        WHERE pz.zamowienie_id = rec_zamowienie.zamowienie_id
        GROUP BY p.nazwa;
    END LOOP;
END;
$$;




-- FUNKCJA 2
-- Statystyki klienta: liczba zamówień + łączna wartość zakupów
-- Kursory + agregacja danych

CREATE OR REPLACE FUNCTION klient_statystyki_cursor(p_klient_id INT)
RETURNS TABLE (
    liczba_zamowien INT,
    laczna_kwota NUMERIC
) AS $$
DECLARE
    cur_zamowienia CURSOR FOR
        SELECT zamowienie_id
        FROM zamowienia
        WHERE klient_id = p_klient_id;

    cur_pozycje CURSOR (p_zamowienie_id INT) FOR
        SELECT ilosc, cena_jednostkowa
        FROM pozycje_zamowienia
        WHERE zamowienie_id = p_zamowienie_id;

    zam_rec RECORD;
    poz_rec RECORD;

    zam_count INT := 0;
    suma NUMERIC := 0;
BEGIN
    OPEN cur_zamowienia;
    LOOP
        FETCH cur_zamowienia INTO zam_rec;
        EXIT WHEN NOT FOUND;

        zam_count := zam_count + 1;

        OPEN cur_pozycje(zam_rec.zamowienie_id);
        LOOP
            FETCH cur_pozycje INTO poz_rec;
            EXIT WHEN NOT FOUND;

            suma := suma + (poz_rec.ilosc * poz_rec.cena_jednostkowa);
        END LOOP;
        CLOSE cur_pozycje;
    END LOOP;
    CLOSE cur_zamowienia;

    RETURN QUERY SELECT zam_count, suma;
END;
$$ LANGUAGE plpgsql;

# Arek Scan Suite — DEMO

Edukacyjny, **legalny** przykład automatycznego skanowania portów.
Pokazuje ten sam wzorzec co pełne zestawy OSINT (masscan → parser → raport),
ale **działa wyłącznie na Twoim własnym sprzęcie / Twojej własnej sieci**.

> **Zasada:** wolno Ci skanować tylko to, co do Ciebie należy
> (local peer, Twój router, Twoje urządzenia w domowej sieci).
> Skanowanie cudzych systemów bez zgody jest nielegalne — w tym projekcie jest zablokowane.

## Co robi

1. Wykrywa Twoje własne IP (`--target localhost` domyślnie)
2. Skanuje **localhost + własne IP** przez `masscan` (porty 22, 80, 443, 3389, 8080)
3. Parsuje wyniki i pokazuje otwarte porty
4. Zapisuje raport do `reports/`

## Wymagania

- Python 3.10+
- `masscan` (instalacja: `sudo apt install masscan`)

## Uruchomienie

```bash
python3 scan_demo.py                 # skanuje localhost + własne IP
python3 scan_demo.py --target 192.168.100.1   # własny router (wymaga potwierdzenia)
```

## Ograniczenia bezpieczeństwa

- Cel spoza sieci lokalnej (nie `127.0.0.*`, `192.168.*`, `10.*`, `172.16-31.*`, `100.64.*`) → **blokada**.
- Zawsze pytamy o potwierdzenie, że cel jest Twój.
- Stawka skanowania obniżona (1000 pkt/s) — nie obciąża sieci.
- Bez list haseł, bez brute-force, bez list krajowych.

## Autor

**Arek** — pseudonim **h5n1** (z czasów IRC, ~2001). Samouk, od zawsze
zafascynowany tym, jak działają sieci. Skanery pisał na własne potrzeby
(uczenie się), nigdy nie udostępniał wyników ani nie używał ich publicznie —
ta demo-wersja pokazuje tę samą umiejętność, w granicach prawa i zdrowego
rozsądku. Pisany z pomocą AI, pomysły i weryfikacja — moje.

## Licencja

MIT — patrz `LICENSE`. Użyj zgodnie z prawem i sumieniem.
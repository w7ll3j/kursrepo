# Uppgift 1 - RANSOM!

### Krypterat meddelande:
> Eiz hvieizi äi oåhgz lxs yzxpfkvimz äi izwvizwv. Sprxpz 24 yrgxlrm uöiv nåmwzt po 90:99, zmmzih häoqvi er pfmwfkktrugvimz kå mägvg!
### Dekrypterat meddelande:
> Era servrar är låsta och backuperna är raderade. Skicka 75 bitcoin före måndag kl 09:00, annars säljer vi kunduppgifterna på nätet!


## Hur man kör programmet
- Gå till mappen uppgift-1 `cd uppgift-1`
- Kör `uv sync` för att uppdatera mappen med de paket som behövs för att köra filen.
- Kör testet med `uv run pytest .\solution.py`

    *eller*: 
    
    Om du vill se alla test i en tydlig lista: `uv run pytest .\solution.py -v`
- `uv run .\solution.py` kör programmet och ger den returnerade dekrypteringen av meddelandet.

## Antaganden
- Krypteringen följer Atbash-chiffret.
- Endast små bokstäver och siffror dekrypteras. Stora bokstäver och andra symboler skrivs som de är.
- Dekryptering och kryptering använder samma logik och fungerar i testerna, eftersom Atbash speglar symmetriskt.
- Lösningen innehåller string-modulen för att slippa skriva ut alla bokstäver, siffror och andra tecken för hand.


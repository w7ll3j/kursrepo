# Uppgift 2 - RANSOM!

## Logganalys - svar
Personer som gick ut från datorhallen den 14:e augusti mellan timmarna 13 och 18 (13.00 - 18.59):

['id001', 'id007', 'id009', 'id015']

## Hur man kör programmet
- Gå till mappen uppgift-2 `cd uppgift-2`
- Kör `uv sync` för att uppdatera mappen med de paket som behövs för att köra filen.
- Kör testerna med `uv run pytest .\solution.py`

    *eller*: 
    
    Om du vill se alla test i en tydlig lista: `uv run pytest .\solution.py -v`
- `uv run .\solution.py` kör programmet på access.log och ger den returnerade listan

## Antaganden
- Filen läses i UTF-8. Är den inte det så kastas ett UnicodeDecodeError som programmet inte hanterar.
- Om filen saknas hanterar programmet inte det. FileNotFoundError kastas direkt.
- access.log ligger i samma mapp programmet körs ifrån.
- Ett ID består av 5 tecken. Uppgiftens exempel har 4 tecken, men jag följer access.logs format.
- Tomma rader hoppas över och trasiga rader ger ett ValueError med radnummer och ett meddelande.

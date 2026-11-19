# Kursrepo: IT-säkerhet och Python
 
Samlingsrepo för mina kursuppgifter på YH-utbildningen IT-säkerhetsspecialist (IT-Högskolan).
 
Läs mer om scenariot och uppgifternas syfte i [RANSOM-berattelse.md](RANSOM-berattelse.md).
 
## Uppgifter
 
| Uppgift | Beskrivning | Status |
|---|---|---|
| [uppgift-1](uppgift-1/) | Dekryptera ett krypterat meddelande (Atbash-chiffret) | Klar |
| [uppgift-2](uppgift-2/) | Läsa en passerkortslogg och hitta vilka som lämnade datorhallen | Klar |
| [uppgift-3](uppgift-3/) | Hitta den dator som står ensam, utifrån GPS-positioner | Klar |
| [uppgift-4](uppgift-4/) | RANSOM! Hitta vilken användare som hade access till den stulna datorn | Klar |
 
Varje uppgiftsmapp har en egen README med svar, körinstruktioner och antaganden.
 
## Installation
 
Projekten använder **Python 3.13** och verktyget **uv**.
 
**Steg 0:** Installera uv enligt instruktionerna på https://docs.astral.sh/uv/.
 
Gå till uppgiftens mapp och installera de paket projektet behöver:
 
```bash
cd uppgift-4
uv sync
```
 
## Användning
 
Kör testerna:
 
```bash
uv run pytest
```
 
Kör programmet:
 
```bash
uv run solution.py
```
 
## Licens
 
MIT
 
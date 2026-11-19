# RANSOM! - Projektets bakgrund och uppgifter
 
Projektet är en serie övningar i Python inom IT-säkerhet. Alla fyra uppgifterna hör ihop i ett fiktivt scenario: ett företag har utsatts för en ransomware-attack, och uppgifterna handlar om att utreda vem som låg bakom den.
 
Det här dokumentet beskriver vad varje uppgift handlade om och vilka tekniska begrepp den täckte. Det innehåller inga lösningar eller svar.
 
---
 
## Scenariot: Anaconda Industries
 
Det multinationella företaget **Anaconda Industries** utsattes för en **ransomware-attack**.
 
**Ransomware** (utpressningsprogram) är skadlig kod som låser eller krypterar en organisations data och kräver betalning för att släppa den. Jämför med ett inbrott där tjuven låser in dig i ditt eget hus och kräver lösen för nyckeln.
 
Hackarna lämnade ett krypterat meddelande på företagets hemsida. Uppgifterna följer utredningen från meddelandet, via ett stulet passerkort och en stulen dator, fram till den skyldiga.
 
---
 
## Uppgift 1: Meddelandet
 
**Vad uppgiften handlade om:**
Meddelandet på hemsidan var krypterat med en enkel krypteringsmetod (**cipher**). Uppgiften var att identifiera metoden och skriva en funktion som dekrypterar meddelandet.
 
**Vad som ingick:**
- Identifiera ciphern utifrån exempeltester.
- Skriva en funktion som tar det krypterade meddelandet och returnerar den lästa texten.
- Dokumentera ciphern i en docstring.
- Skriva egna tester, minst sex totalt.
**Vad som lämnades in:** Det dekrypterade meddelandet i `README.md`, samt `solution.py`.
 
---
 
## Uppgift 2: Passerkortet
 
**Vad uppgiften handlade om:**
Hackarna hade tagit sig in och stulit datorn med kontouppgifterna. Inga spår av våldsamt inbrott hittades, så misstanken riktades mot någon med ett passerkort. Varje in- och utpassering i datorhallen loggades i `access.log`, med dag, tid, riktning (in eller ut) och ett ID.
 
**Vad som ingick:**
- Läsa loggfilen och hitta vilka ID:n som lämnade datorhallen under ett angivet tidsfönster.
- Skriva en funktion som tar sökvägen som parameter, så att den fungerar med vilken loggfil som helst.
- Hantera tidsgränserna korrekt (inklusive eller exklusive).
- Skriva en docstring och egna tester, minst tre.
**Vad som lämnades in:** Listan med misstänkta ID:n i `README.md`, samt `solution.py`.
 
---
 
## Uppgift 3: Den stulna datorn
 
**Vad uppgiften handlade om:**
IT-säkerhetsavdelningen hade gömt spårsändare (GPS-sändare) i alla företagets datorer. Sändarna skickade regelbundet sin position som latitud och longitud, och positionerna sparades i `tracking.json`. Den stulna datorn antogs vara ensam på sin plats.
 
Eftersom positionerna inte är exakta, måste två datorer på samma plats räknas som "nära nog" varandra. Det krävde ett tröskelvärde.
 
**Vad som ingick:**
- Hitta den dator som är ensam på sin plats.
- Skriva en hjälpfunktion som avgör om två positioner är nära nog.
- Lägga tröskelvärdet på ett enda ställe i koden, med en motivering i kommentaren.
- Kasta ett undantag om ingen eller flera datorer är ensamma, i stället för att gissa.
- Skriva egna tester för hjälpfunktionen, gränsen och felfallet.
- Analysera tröskelvärdet i `README.md` genom att köra programmet med ett mycket litet och ett mycket stort värde.
**Vad som lämnades in:** Namnet på datorn, dess koordinater och stad, analysen av tröskelvärdet i `README.md`, samt `solution.py`.
 
---
 
## Uppgift 4: Utpressaren
 
**Vad uppgiften handlade om:**
Med de misstänkta från uppgift 2 och datorns plats från uppgift 3 återstod att ta reda på vilken av de misstänkta som hade **access** till rummet där datorn stod.
 
Informationen kom från två källor:
- **Ett användarsystem på webben**, som svarade med en JSON-lista över användare och deras åtkomst.
- **`rooms.csv`**, en databasdump som visade vilken dator som stod i vilket rum.
Åtkomsten lagrades som en sträng med ettor och nollor, där varje tecken motsvarade ett rum. Byggnaden hade flera våningar med olika antal rum, vilket gjorde det knepigt att räkna ut vilket tecken som hörde till vilket rum.
 
**Vad som ingick:**
- Hämta användarlistan med timeout och kontroll av statuskod, och ge ett begripligt felmeddelande vid fel.
- Validera datan innan den används, eftersom den kommer från internet.
- Implementera klasserna `Room`, `User` och `NoUniqueCulpritError`.
- Implementera funktionerna `parse_users`, `load_rooms`, `find_culprit`, `write_report` och `solution`.
- Kasta `NoUniqueCulpritError` när ingen eller flera misstänkta har access.
- Skriva `rapport.csv` även när det inte finns någon unik skyldig.
- Skriva minst fem egna tester som fungerar utan internet.
- Analysera i `README.md` vilka antaganden koden gör om byggnaden och vad som kan gå fel när datan kommer från internet.
**Vad som lämnades in:** Namnet på den skyldige i `README.md`, `solution.py`, `test_solution.py` och `rapport.csv`.
 
---
 
## Så hänger uppgifterna ihop
 
Ransomware-attacken är utgångspunkten. Passerkortsloggen (uppgift 2) ger en lista med misstänkta. Spårsändarna (uppgift 3) visar var datorn fanns. Åtkomstkoderna (uppgift 4) avgör vilka av de misstänkta som kunde komma in i rummet. Krypteringen (uppgift 1) var det första spåret i utredningen.
 
## Köra projekten
 
```bash
uv run solution.py            # uppgift 1-4
uv run pytest solution.py     # uppgift 1-3
uv run pytest                 # uppgift 4
```
 
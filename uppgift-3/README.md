# Uppgift 3 - RANSOM!

## Den stulna datorn

Läser tracking.json och räknar ut vilken dator som befinner sig på en ensam plats.

### Datornamnet jag fick ut från programmet:

> Makar

### Datorns latitud och longitud:

> 59.8586, 17.6391

Koordinaterna pekar på Uppsala.

*gpskoordinater.com*

### Tröskelvärde

Jag använde tröskelvärdet 0.05. En breddgrad är 111 km, vilket innebär cirka 5,6 km. Longituden är kortare ju längre nord man kommer, men jag mätte avståndet i km mellan två punkter med samma latitud och olika longitud med avståndskalkylatorn omnicalculator.com. Då kunde jag räkna ut att 1 grad longitud ligger på cirka 57 km. Det motsvarar 2,85 km med tröskelvärdet på 0.05.

### Tröskelanalys

**Programmet kört med MAX_AVSTAND på 0.0001:**

*Hypotes:*

> Min hypotes är ValueError med ett utfall på flera datorer, då avståndet bara är några meter.

*Resultat:*
```python
ValueError: Flera datorer är ensamma:


['link', 'ganon', 'marin', 'tingle', 'beedle', 'medli', 'komali', 'makar', 'midna', 'linebeck', 'yuga', 'ravio', 'tuft', 'mipha', 'daruk']
```

*Med en tröskel på 0.0001 grad motsvarar det cirka 11 meter i nord-syd och cirka 6 meter i öst-väst. Datorer på samma plats har positioner som skiljer sig mer än 0.0001. zelda och ganon skiljer sig 0.0001 i latitud, men 0.0008 i longitud, så de räknas som skilda.*

**Programmet kört med MAX_AVSTAND på 1:**

*Hypotes:*

> Min hypotes är ValueError med ett utfall på ingen dator, då jag tror att alla datorer har en annan dator inom 1 grad.

*Resultat:*

```python
ValueError: Ingen dator är ensam
```

*Med en tröskel på 1 grad motsvarar det cirka 111 km i nord-syd och 57 km i öst-väst. Alla datorer har en annan dator inom 1 grad, så ingen är ensam.*


## Hur man kör programmet

Gå till mappen uppgift-3:
```bash
cd uppgift-3
```

Uppdatera mappen med de paket som behövs för att köra filen:
```bash
uv sync
```

Kör testet med:
```bash
uv run pytest .\solution.py
```
*eller*: 

Om du vill se alla test i en tydlig lista: 
```bash
uv run pytest .\solution.py -v
```

Kör programmet och returnera den ensamma datorn:
```bash
uv run .\solution.py
```

## Antaganden

- Filen tracking.json ligger i samma mapp som programmet.
- Positionerna är ungefärliga och kan avvika några meter från de faktiska platserna. Det innebär att tröskeln behöver vara större än mätfelet som kan uppstå.
- Tröskeln är samma för latitud och longitud. En grad latitud är längre än en grad longitud. Tröskeln motsvarar därför olika många kilometer i de två riktningarna.
- Filen innehåller endast en position per dator. Programmet vet inget om datorn förflyttas, så en dator som rör sig går ej att upptäcka.
- Filen kan innehålla fel värden eller positioner i fel format. Programmet kastar felen med ett felmeddelande.
- En stulen dator är den enda som inte har en annan dator nära sig.

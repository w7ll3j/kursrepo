# Uppgift 4 - RANSOM!

Hittar vilken av användarna som hade access till den stulna datorn.

## Namnet på den skyldige

**Robert Bennett**

## Hur man kör programmet

Gå till mappen uppgift-4:

```bash
cd uppgift-4
```

Installera de paket projektet behöver:

```bash
uv sync
```

Kör testerna med:

```bash
uv run pytest
```

*eller*:

Om du vill se testerna i en tydlig lista:

```bash
uv run pytest -v
```

Kör programmet och skriv ut namnet på den skyldige. Filen `rapport.csv` sparas även med de misstänkta användarna och deras status:

```bash
uv run solution.py
```

*Programmet avslutas med ett kort meddelande om inte exakt en misstänkt har access till datorns rum.
Rapporten skrivs även om ingen unik skyldig finns bland de misstänkta.*

## Antaganden

- Varje dator står bara på en rad i rooms.csv. Skulle en dator stå på två rader skriver programmet över den ena utan felmeddelande. Det är en risk som inte hanteras.

- Programmet antar att varje användar-ID är unikt och förekommer bara en gång.

## Analys

### Byggnaden och rooms.csv

Metoden `has_access` kastar ett `ValueError` om längden i accesskoden inte stämmer överens med antal rum, eller om rummet saknas i rumslistan, eftersom den inte kan hitta rätt position i accesskoden.

Om tecknen i accesskoden inte ligger i rätt ordning kastas inget fel, och programmet fortsätter som vanligt. Det är en risk som kan göra att fel användare pekas ut som skyldig.

Ett exempelscenario är om ett nytt rum läggs till mitt i byggnaden utan att användarnas accesskoder uppdateras. Då stämmer inte längre accesskodens längd med antalet rum, vilket gör att `ValueError` kastas och felet blir tydligt.

Samma rum förekommer flera gånger med olika datornamn, vilket innebär att ett rum innehåller flera datorer. Det påverkar inte resultatet i programmet eftersom funktionen unika_rum tar bort dubbletterna av rum innan has_access används.

### Datan från internet

Att hämta data från internet medför några risker:

- Om nätverket är nere kan datan inte hämtas.

- Om servern svarar med fel statuskod.

- Om servern tar för lång tid på sig att svara (timeout).

- Om JSON-datan är ogiltig och inte följer rätt format.

- Om strukturen är fel eller om innehållet har ändrats kan programmet tolka datan fel.

Vissa av dessa fel hanterar programmet. Vid hämtning av data kontrolleras HTTP-svaret med raise_for_status(). Om servern svarar med en felaktig statuskod, exempelvis 4xx (fel från klienten) eller 5xx (fel på servern), kastas ett fel som fångas av programmets except.
Om servern tar för lång tid på sig att svara uppstår en timeout, vilket ger ett fel innan något svar har kommit. Ogiltig JSON och nätverksfel fångas också av programmet och hanteras som ValueError.

Strukturfel hanteras av parse_users, som kastar ValueError om något saknas eller har fel datatyp.

Vissa saker kan däremot inte kontrolleras av programmet. Det gäller exempelvis datans integritet och om den verkligen kommer från rätt källa. Om någon ändrar innehållet, till exempel byter plats på användare eller lägger till ett extra fält, märker programmet inte det så länge formatet fortfarande stämmer. Programmet kan kontrollera att datan har rätt format och struktur, men inte garantera att innehållet är korrekt.

### Varför timeout och validering är viktiga

Om servern aldrig svarar väntar programmet i oändlighet och kan därför inte ge något svar. Att ha en timeout på 5 sekunder innebär att om servern inte svarat innan dess så kastas ett ValueError. Det skyddar tillgängligheten eftersom utredningen annars står still.

Om felaktig data får ändra resultatet av programmet kan det peka ut fel person, eller frikänna den som faktiskt har gjort det. Då blir utredningen felaktig och det kan få allvarliga följder. Valideringen minskar risken att felaktig data påverkar resultatet.

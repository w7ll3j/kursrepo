"""Hittar vilken av användarna som hade access till den stulna datorn."""

import csv
import string
import sys
from pathlib import Path
from typing import Any

import requests

# Svaret från uppgift 2: ID:n som lämnade datorhallen den 14:e mellan kl 13 och 18.
SUSPECTS: list[str] = ["id001", "id007", "id009", "id015"]

# Svaret från uppgift 3: namnet på den stulna datorn.
COMPUTER = "makar"

URL = "https://gist.githubusercontent.com/Grokzen/11ddfa83c0f0d379d33d7abbfdd1c77e/raw/aafbe6fce8a47e80edfe45e464791f7b66607fb7/gistfile1.txt"

RAPPORT_CSV = Path(__file__).parent / "rapport.csv"

ROOMS_CSV = Path(__file__).parent / "rooms.csv"


def room_kontroll(varde: str, del_: str) -> None:
    """Kontrollerar att en del har ett värde och endast innehåller siffror.

    ValueError om delen saknar värde eller innehåller andra tecken än siffrorna 0-9.

    varde: värdet som ska kontrolleras.
    del_: namnet på delen som används i felmeddelandet.

    Returnerar ingenting.
    """
    if not varde:
        raise ValueError(f"{del_} saknar värde.")

    for tecken in varde:
        if tecken not in string.digits:
            raise ValueError(f"{del_} måste vara ett heltal.")


class Room:
    """Representerar rummen på kontoret.

    Ett Room-objekt håller ett rum i sitt minne tillsammans med våning och rumsnummer.
    Två objekt räknas som lika om namnet är samma.
    Room kan inte användas i set eller som nyckel i dicts,
    eftersom klassen definierar __eq__ men inte __hash__.

    Attribut:
        name: rumsnamnet i formatet room-<våning>-<rumsnummer>.
        floor: våningen i rumsnamnet.
        number: rumsnumret i rumsnamnet.
    """

    def __init__(self, name: str) -> None:
        """Sparar namnet och räknar ut våning och rumsnummer.

        ValueError om name inte följer formatet room-<våning>-<rumsnummer>,
        samt i hjälpfunktionen room_kontroll om en del saknar värde eller innehåller
        något annat än siffror.

        name: rumsnamnet.
        """
        self.name = name
        delar = name.split("-")

        if len(delar) != 3 or delar[0] != "room":
            raise ValueError("Fel format. Ska vara room-<våning>-<rumsnummer>.")

        room_kontroll(delar[1], "Våningen")

        self.floor = int(delar[1])

        room_kontroll(delar[2], "Rummet")

        self.number = int(delar[2])

    def __str__(self) -> str:
        """Returnerar rumsnamnet."""
        return self.name

    def __eq__(self, other: object) -> bool:
        """Jämför två rum på deras namn, och inte på objektet.

        TypeError om ett Room jämförs med något som inte är Room.

        other: det rum som jämförs med.

        Returnerar True om namnen är lika, False om namnen är olika.
        """
        if not isinstance(other, Room):
            # Ger ett tydligt fel, istället för att returnera False eller annan felkod.
            raise TypeError(f"{other} är inget Room-objekt.")

        return self.name == other.name


class User:
    """Representerar en användare med dess id, namn och accesskod.

    Publika metoder:
        has_access: Kontrollerar access.

    Attribut:
        id: id-koden på användaren.
        name: namnet på användaren.
        access: koden som anger vilka rum användaren har tillgång till.
    """

    def __init__(self, id: str, name: str, access: str) -> None:
        """Sparar id, namn och accesskoden.

        id: id-numret.
        name: namnet.
        access: koden.
        """
        self.id = id
        self.name = name
        self.access = access

    def __str__(self) -> str:
        """Returnerar namnet och id-koden som en sträng med formatet:
        name (id).
        """
        return f"{self.name} ({self.id})"

    def has_access(self, room: Room, rooms: list[Room]) -> bool:
        """Kontrollerar om användaren har tillgång till ett visst rum och returnerar en bool.

        ValueError om rummet inte finns i listan, och när accesskodens längd inte stämmer.

        room: Room-objektet som ska kontrolleras.
        rooms: listan över alla Room-objekt.

        Returnerar True om indexet i accesskoden är 1. False om indexet i accesskoden är 0.
        """
        if room not in rooms:
            raise ValueError(f"{room} finns inte.")

        if len(self.access) != len(rooms):
            raise ValueError(
                f"{self.access}({len(self.access)}) har fel längd. "
                f"Den ska innehålla {len(rooms)}."
            )

        # Tupler för att våning jämförs först, och sedan rumsnummer.
        plats = sum(
            1 for rum in rooms if (rum.floor, rum.number) < (room.floor, room.number)
        )

        return self.access[plats] == "1"


class NoUniqueCulpritError(Exception):
    """Representerar ett undantag som kastas om det finns inga eller flera misstänkta.

    Kastas av find_culprit.
    """


def kontrollera_post(post: dict[str, Any]) -> None:
    """Kontrollerar att en post innehåller rätt nycklar och värden.

    ValueError om nycklarna id, name och access inte finns i posten,
    om något av värdena inte är en sträng,
    om accesskoden innehåller något annat än 0 eller 1,
    om accesskoden är tom.

    post: en dict som ska kontrolleras.

    Returnerar ingenting.
    """
    for nyckel in ("id", "name", "access"):
        if nyckel not in post:
            raise ValueError(f"{post}: Posten saknar {nyckel}.")
        if not isinstance(post[nyckel], str):
            raise ValueError(f"{post[nyckel]} är ingen sträng.")  # noqa: TRY004

    if post["access"] == "":
        raise ValueError("Accesskoden får inte vara tom.")

    for tecken in post["access"]:
        if tecken not in "01":
            raise ValueError(f"{tecken} är inte 0 eller 1.")


def parse_users(data: list[dict[str, Any]]) -> list[User]:
    """Kontrollerar användardatan och returnerar en lista med User-objekt.

    ValueError om datan inte är en lista och om någon post i listan inte är en dict.
    ValueError från kontrollera_post skickas vidare till anropande kod.

    data: Användarlistan som hämtas från webben med funktionen hamta_anvandare.
    Varje post är en dict med nycklarna id, name och access.

    Returnerar en lista med User-objekt som innehåller värdena för id, name och access.
    """
    anvandare_lista = []

    if not isinstance(data, list):
        raise ValueError(f"{data} är ingen lista.")  # noqa: TRY004

    for post in data:
        if not isinstance(post, dict):
            raise ValueError(f"{post} är inte en dict.")  # noqa: TRY004

        kontrollera_post(post)

        anvandare_lista.append(User(post["id"], post["name"], post["access"]))

    return anvandare_lista


def load_rooms(path: str) -> dict[str, Room]:
    """Läser CSV-filen och skapar en dict med rum per dator.

    FileNotFoundError om filen inte finns i path.
    ValueError om rumsnamnet har fel format. Kastas i Room-klassen.

    path: sökvägen till CSV-filen med rader som innehåller ett rum samt datorn som ligger i rummet.

    Returnerar en dict med datornamn som nyckel och ett Room-objekt som värde.
    """
    with open(path, newline="", encoding="utf-8") as fil:
        rum_per_dator = {
            rad["Computer"]: Room(rad["Room"]) for rad in csv.DictReader(fil)
        }

    return rum_per_dator


def unika_rum(rum_per_dator: dict[str, Room]) -> list[Room]:
    """Tar emot en dict med datorer och Room-objekt, och returnerar en lista med Room-objekt.

    rum_per_dator: en dict från load_rooms() med datornamn som nycklar och Room-objektet som värde.

    Returnerar en lista med Room-objekt, som endast innehåller varje rum en gång.
    """
    resultat = []

    for rum in rum_per_dator.values():
        if rum not in resultat:
            resultat.append(rum)

    return resultat


def hamta_datorns_rum(computer: str, computer_rooms: dict[str, Room]) -> Room:
    """Tar emot en dator och en dict med datorer och Room-objekt, och returnerar datorns Room-objekt.

    ValueError om datorn inte finns i computer_rooms.

    computer: datornamnet som ska hämtas.
    computer_rooms: en dict från load_rooms() med datornamn som nycklar och Room-objektet som värde.

    Returnerar Room-objektet för den angivna datorn.
    """
    try:
        return computer_rooms[computer]
    except KeyError as fel:
        raise ValueError(f"{computer} saknas i rooms.csv.") from fel


def find_culprit(
    suspects: list[str],
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> User:
    """Returnerar användaren som har access till den stulna datorns rum.

    ValueError om datornamnet saknas i rumslistan.
    ValueError från anropade funktioner och metoder skickas vidare till anropande kod.
    NoUniqueCulpritError när inte exakt en misstänkt har access till datorns rum.

    suspects: en lista över de suspekta id-numren från svaret i uppgift-2.
    computer: en sträng med den stulna datorn från svaret i uppgift-3.
    users: en lista över alla användare.
    computer_rooms: en dict med datorer som nycklar och vilket rum den befann sig i som värde.

    Returnerar användaren om det finns exakt en misstänkt med
    access till rummet med den stulna datorn.
    """

    datorns_rum = hamta_datorns_rum(computer, computer_rooms)

    alla_rum = unika_rum(computer_rooms)

    med_access = [
        user
        for user in users
        if user.id in suspects and user.has_access(datorns_rum, alla_rum)
    ]

    if not med_access:
        raise NoUniqueCulpritError("Ingen misstänkt har access till datorns rum.")
    if len(med_access) == 1:
        return med_access[0]
    raise NoUniqueCulpritError(
        f"{len(med_access)} misstänkta har access. Kunde ej fastställa en."
    )


def write_report(
    path: str,
    suspects: list[str],
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> None:
    """Skriver en CSV-rapport över de misstänkta och deras access till datorns rum.

    Filen skrivs över varje gång funktionen körs med rubrikerna: id, namn, access och status.
    Därefter en rad för varje ID i suspects i dess ordning, med användarens uppgifter.
    Status skrivs ut som "har access" eller "saknar access"
    beroende på om användaren har access till rummet med den stulna datorn.

    ValueError om den stulna datorn inte finns i computer_rooms.
    ValueError om ett misstänkt ID inte finns bland alla ID:n i users.
    ValueError från anropade funktioner och metoder skickas vidare till anropande kod.

    path: sökvägen till csv-filen.
    suspects: en lista över de suspekta id-numren från svaret i uppgift-2.
    computer: en sträng med den stulna datorn från svaret i uppgift-3.
    users: en lista över alla användare.
    computer_rooms: en dict med datorer som nycklar, och vilket rum den befann sig i som värde.

    Returnerar ingenting, utan skriver rapporten till path med de misstänkta användarna.
    """

    datorns_rum = hamta_datorns_rum(computer, computer_rooms)

    anvandare_lista = []
    for suspekta_idn in suspects:
        anvandare = next((user for user in users if user.id == suspekta_idn), None)
        if anvandare is None:
            raise ValueError(f"{suspekta_idn} finns inte bland användarna.")
        anvandare_lista.append(anvandare)

    alla_rum = unika_rum(computer_rooms)

    with open(path, "w", newline="", encoding="utf-8") as fil:
        writer = csv.writer(fil)
        writer.writerow(["id", "namn", "access", "status"])

        for misstankt in anvandare_lista:
            if misstankt.has_access(datorns_rum, alla_rum):
                status = "har access"
            else:
                status = "saknar access"
            writer.writerow(
                [
                    misstankt.id,
                    misstankt.name,
                    misstankt.access,
                    status,
                ]
            )


def hamta_anvandare() -> list[dict[str, Any]]:
    """Hämtar användarlistan från URL-konstanten.

    ValueError om hämtningen misslyckas och vid ogiltig JSON.

    Returnerar en lista med dicts, ett per användare.
    """
    try:
        # 5 sekunders timeout för att ge rimlig tid för svar
        # utan att programmet fastnar för länge om något går fel.
        svar = requests.get(URL, timeout=5)
        svar.raise_for_status()
        data: list[dict[str, Any]] = svar.json()
    except requests.RequestException as fel:
        # Originalfelet bevaras för felsökning.
        raise ValueError(f"Det gick inte att hämta användarna.\n{fel}") from fel

    return data


def solution() -> str:
    """Kör alla funktioner och returnerar namnet på den skyldige.

    Anropar hamta_anvandare och får en lista med dicts för varje användare.
    Anropar sedan parse_users med listan från ovan och får User-objekt för varje användare.
    Läser CSV-filen med load_rooms och får varje datornamn och deras rum.
    Anropar sedan write_report och find_culprit med resultaten från tidigare steg.
    Rapporten skrivs även om ingen unik skyldig finns.

    Undantag (exceptions) från de anropade funktionerna skickas vidare till anropande kod.
    Se feltyper FileNotFoundError, ValueError och NoUniqueCulpritError i respektive funktion.

    Returnerar namnet på den skyldige användaren. Filen rapport.csv skrivs som bieffekt
    med de misstänkta användarna och deras status.
    """
    data = hamta_anvandare()

    anvandare_lista = parse_users(data)

    rum_per_dator = load_rooms(ROOMS_CSV)

    write_report(RAPPORT_CSV, SUSPECTS, COMPUTER, anvandare_lista, rum_per_dator)

    skyldig = find_culprit(SUSPECTS, COMPUTER, anvandare_lista, rum_per_dator)

    return skyldig.name


if __name__ == "__main__":
    try:
        print(solution())
    # TypeError betyder att koden har en bugg.
    # Därför behålls tracebacken för att kunna hitta felet.
    except (ValueError, NoUniqueCulpritError, FileNotFoundError) as fel:
        # Förväntade fel visas som ett kort meddelande.
        # Eftersom användaren ska förstå dem utan tracebacken.
        print("Något gick fel:", fel)
        sys.exit(1)

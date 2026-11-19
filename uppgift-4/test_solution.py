"""Tester för uppgift 4. Kör dem från den här mappen med: uv run pytest"""

import csv

import pytest
from solution import (
    RAPPORT_CSV,
    NoUniqueCulpritError,
    Room,
    User,
    find_culprit,
    load_rooms,
    parse_users,
    solution,
    unika_rum,
    write_report,
)


# En liten exempelbyggnad som testerna använder: 2 rum på våning 1 och 3 rum på
# våning 2. Du får använda hjälpfunktionerna i dina egna tester också.
def exempelrum():
    return [
        Room("room-2-2"),
        Room("room-1-1"),
        Room("room-2-3"),
        Room("room-1-2"),
        Room("room-2-1"),
    ]


def exempelanvandare():
    return [
        User("id1", "Anna", "01000"),
        User("id2", "Bo", "00010"),
        User("id3", "Cia", "00100"),
        User("id4", "Dan", "01000"),
    ]


def exempeldatorer():
    return {
        "pc-c": Room("room-2-1"),
        "pc-a": Room("room-1-1"),
        "pc-e": Room("room-2-3"),
        "pc-b": Room("room-1-2"),
        "pc-d": Room("room-2-2"),
    }


def test_room():
    room = Room("room-2-3")
    assert room.name == "room-2-3"
    assert room.floor == 2
    assert room.number == 3
    assert str(room) == "room-2-3"


def test_user():
    user = User("id900", "Anna Exempel", "01101")
    assert user.id == "id900"
    assert user.name == "Anna Exempel"
    assert user.access == "01101"
    assert str(user) == "Anna Exempel (id900)"


def test_has_access():
    # Rummen skickas in i blandad ordning: metoden får inte lita på ordningen.
    rooms = exempelrum()
    user = User("id900", "Anna Exempel", "01101")
    assert user.has_access(Room("room-1-2"), rooms) is True
    assert user.has_access(Room("room-2-2"), rooms) is False
    assert user.has_access(Room("room-2-3"), rooms) is True


def test_find_culprit():
    # pc-d står i room-2-2 (plats 3): bara id2 har en etta där.
    skyldig = find_culprit(
        ["id1", "id2", "id3"], "pc-d", exempelanvandare(), exempeldatorer()
    )
    assert skyldig.name == "Bo"


def test_solution():
    # Kräver internet, och att SUSPECTS och COMPUTER är ifyllda i solution.py.
    namn = solution()
    assert type(namn) == str, "solution() should return a string"
    assert len(namn) > 0, "solution() should return a name"

    with open(RAPPORT_CSV, newline="", encoding="utf-8") as fil:
        rader = list(csv.reader(fil))
    assert rader[0] == ["id", "namn", "access", "status"]
    assert len(rader) > 1, "rapport.csv should have one row per suspect"


def test_room_fel_format_ger_fel():
    with pytest.raises(ValueError) as fel:
        Room("Rum 28")
    assert "room-<våning>-<rumsnummer>" in str(fel.value)


@pytest.mark.parametrize(
    "rumsnamn, meddelande",
    [
        # Våningen är inget heltal.
        (
            "room-+1-1",
            "Våningen måste vara ett heltal.",
        ),
        # Rummet är inget heltal.
        (
            "room-1-+1",
            "Rummet måste vara ett heltal.",
        ),
        # En tom våning.
        (
            "room--1",
            "Våningen saknar värde.",
        ),
        # Ett tomt rum.
        (
            "room-1-",
            "Rummet saknar värde.",
        ),
    ],
)
def test_ogiltig_del_ger_fel(rumsnamn, meddelande):
    with pytest.raises(ValueError, match=meddelande):
        Room(rumsnamn)


def test_has_access_forsta_och_sista():
    rooms = exempelrum()
    user = User("id001", "William Ring", "10001")
    assert user.has_access(Room("room-1-1"), rooms) is True
    assert user.has_access(Room("room-2-3"), rooms) is True
    assert user.has_access(Room("room-1-2"), rooms) is False


def test_has_access_raknar_over_vaningar():
    rooms = [
        Room("room-2-2"),
        Room("room-1-1"),
        Room("room-2-3"),
        Room("room-2-1"),
        Room("room-3-1"),
        Room("room-3-2"),
    ]
    user = User("id001", "William Ring", "000010")
    # Rummet room-3-1 är det femte i ordningen och ska ha access.
    assert user.has_access(Room("room-3-1"), rooms) is True


def test_fel_langd_pa_access_kod_ger_fel():
    rooms = exempelrum()
    # Accesskoden har bara 4 siffror, medan exempelrummen är 5 stycken.
    user = User("id001", "William Ring", "1011")
    with pytest.raises(ValueError) as fel:
        user.has_access(Room("room-1-1"), rooms)
    assert "1011(4) har fel längd" in str(fel.value)


def test_rum_inte_i_byggnad_ger_fel():
    rooms = [
        Room("room-2-2"),
        Room("room-1-1"),
        Room("room-2-1"),
    ]
    user = User("id001", "William Ring", "10010")
    with pytest.raises(ValueError) as fel:
        user.has_access(Room("room-1-2"), rooms)
    assert "room-1-2 finns inte." in str(fel.value)


# Alla fall nedan ska ge ValueError med rätt text.
@pytest.mark.parametrize(
    "data, meddelande",
    [
        # Accesskoden är tom.
        (
            [{"id": "id001", "name": "William Ring", "access": ""}],
            "får inte vara tom.",
        ),
        # Nyckeln "id" finns inte i posten.
        (
            [{"name": "William Ring", "access": "10110"}],
            "Posten saknar id.",
        ),
        # Ingen lista.
        (
            {"id": "id001", "name": "William Ring", "access": "10110"},
            "är ingen lista.",
        ),
        # Ett av värdena är inte en sträng.
        (
            [{"id": "id001", "name": "William Ring", "access": 10110}],
            "är ingen sträng.",
        ),
        # Accesskoden innehåller en 2:a.
        (
            [{"id": "id001", "name": "William Ring", "access": "10112"}],
            "är inte 0 eller 1",
        ),
        # En post är inte en dict.
        (
            ["Användare", {"id": "id001", "name": "William Ring", "access": "10110"}],
            "är inte en dict",
        ),
    ],
)
def test_trasig_data_ger_fel(data, meddelande):
    with pytest.raises(ValueError, match=meddelande):
        parse_users(data)


def test_find_culprit_ger_fel_nar_inga_traffar():
    with pytest.raises(NoUniqueCulpritError, match="Ingen misstänkt"):
        find_culprit(
            ["id1", "id3", "id4"], "pc-d", exempelanvandare(), exempeldatorer()
        )


def test_find_culprit_ger_fel_nar_flera_traffar():
    with pytest.raises(NoUniqueCulpritError, match="2 misstänkta har access"):
        find_culprit(["id1", "id4"], "pc-b", exempelanvandare(), exempeldatorer())


def test_load_rooms_returnerar_dict(tmp_path):
    fil = tmp_path / "rooms.csv"
    fil.write_text(
        "Room,Computer\nroom-1-1,crypto\nroom-2-2,python\nroom-1-2,delta\nroom-2-1,supra"
    )
    resultat = load_rooms(str(fil))
    assert len(resultat) == 4
    assert str(resultat["crypto"]) == "room-1-1"


def test_write_report_skriver_vid_flera_traffar(tmp_path):
    fil = tmp_path / "rapport.csv"
    write_report(
        str(fil), ["id1", "id2", "id4"], "pc-b", exempelanvandare(), exempeldatorer()
    )
    with open(fil, newline="", encoding="utf-8") as rapport:
        rader = list(csv.reader(rapport))
    assert rader == [
        ["id", "namn", "access", "status"],
        ["id1", "Anna", "01000", "har access"],
        ["id2", "Bo", "00010", "saknar access"],
        ["id4", "Dan", "01000", "har access"],
    ]


def test_unika_rum_tar_bort_dubbletter():
    rum = {
        "crypto": Room("room-1-1"),
        "java": Room("room-1-1"),
        "delta": Room("room-1-2"),
    }
    assert unika_rum(rum) == [Room("room-1-1"), Room("room-1-2")]

import json
from pathlib import Path

import pytest

# Tröskeln är större än de meter som positionerna kan skilja sig, och mindre än avståndet mellan olika tätorter.
MAX_AVSTAND = 0.05

TRACKING_JSON = Path(__file__).parent / "tracking.json"


def solution(path):
    """Läser JSON-filen med datornamn och dess position med latitud och longitud.

    Positionerna är en ögonblicksbild och är ungefärliga.
    Den stulna datorn förväntas vara den enda som är ensam.

    ValueError: om inte exakt en dator är ensam.
    Fel kastas även i hjälpfunktionen ar_nara.

    path: sökväg till JSON-filen.
    Returnerar namnet på den ensamma dator.
    """
    with open(path, encoding="utf-8") as fil:
        datorer = json.load(fil)

        # Behåller en dator om ingen annan dator är nära.
        ensam_dator = [
            namn
            for namn in datorer
            if not any(
                ar_nara(datorer[namn], datorer[annat])
                for annat in datorer
                if annat != namn
            )
        ]

        if len(ensam_dator) == 1:
            return ensam_dator[0]
        elif len(ensam_dator) == 0:
            raise ValueError("Ingen dator är ensam")
        else:
            raise ValueError(f"Flera datorer är ensamma:\n{ensam_dator}")


def ar_nara(position_a, position_b):
    """Hjälpfunktion som jämför två positioner och returnerar en bool.

    TypeError: Om en position saknar längd, om det är ett tal och inte en lista eller null.
    ValueError: Om latituden och longituden för de båda positionerna har fel värden,
    fel antal värden eller fel typ.

    position_a, position_b: en lista med [latitud, longitud]
    Returnerar True om skillnaden på latitud och longitud båda är under MAX_AVSTAND.
    """

    if len(position_a) != 2:
        raise ValueError(f"{position_a} har inte två tal.")
    if len(position_b) != 2:
        raise ValueError(f"{position_b} har inte två tal.")

    latitud_a, longitud_a = position_a
    latitud_b, longitud_b = position_b

    for varde in (latitud_a, latitud_b):
        if type(varde) not in (float, int):
            raise ValueError(f'"{varde}" är inget tal.')
        if not -90 <= varde <= 90:
            raise ValueError(f"{varde} är inget korrekt värde på latitud.")

    for varde in (longitud_a, longitud_b):
        if type(varde) not in (float, int):
            raise ValueError(f'"{varde}" är inget tal.')
        if not -180 <= varde <= 180:
            raise ValueError(f"{varde} är inget korrekt värde på longitud.")

    return (
        abs(latitud_a - latitud_b) < MAX_AVSTAND
        and abs(longitud_a - longitud_b) < MAX_AVSTAND
    )


def test_hjalpfunktion_korrekt_svar():
    """Testar om hjälpfunktionen ger korrekt svar utifrån MAX_AVSTAND.
    Testar även om ordningen på jämförelsen spelar roll.
    """
    a = [59.3291, 18.0681]
    # Latitud skiljer 0.049 från a.
    b = [59.2801, 18.0681]
    # Longitud skiljer 0.049 från a.
    c = [59.3291, 18.0191]
    # Latitud skiljer 0.051 från a.
    d = [59.3801, 18.0681]
    # Longitud skiljer 0.051 från a.
    e = [59.3291, 18.1191]
    # Latitud, longitud skiljer sig kraftigt från a.
    f = [55.4575, 11.678]
    assert ar_nara(a, b)
    assert ar_nara(b, a)
    assert ar_nara(a, c)
    assert ar_nara(c, a)
    assert not ar_nara(a, d)
    assert not ar_nara(a, e)
    assert not ar_nara(a, f)


def test_hjalpfunktion_kastar_korrekt():
    """Testar att hjälpfunktionen kastar korrekta exceptions."""
    a = 7
    b = [59.2801, 18.0681]
    c = [58.1432]
    d = [91.124, -170.333]
    e = [59.1242, -181.643]
    f = ["xyz", 69.1358]
    with pytest.raises(TypeError):
        ar_nara(a, b)
    with pytest.raises(ValueError) as excinfo:
        ar_nara(b, c)
    assert "har inte två tal." in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        ar_nara(b, f)
    assert '"xyz" är inget tal.' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        ar_nara(b, d)
    assert "är inget korrekt värde på latitud." in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        ar_nara(b, e)
    assert "är inget korrekt värde på longitud." in str(excinfo.value)


def test_solution_far_hjalpfunktionens_fel(tmp_path):
    """Testar att ett fel i hjälpfunktionen går vidare upp till solution."""
    fil = tmp_path / "hjalp.json"
    fil.write_text(
        json.dumps(
            {
                "a": [100.124, 19.4578],
                "b": [57.1642, 21.6423],
            }
        )
    )
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert "är inget korrekt värde på latitud." in str(excinfo.value)


def test_solution(tmp_path):
    """Testar att funktionen returnerar en sträng som finns med i tracking.json."""
    namn = solution(TRACKING_JSON)
    assert type(namn) == str, "solution() should return a string"
    with open(TRACKING_JSON) as fil:
        assert namn in json.load(fil), (
            "The name should be one of the computers in the file"
        )
    fil = tmp_path / "exempel.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3291, 18.0681],
                "b": [59.3293, 18.0687],
                "c": [57.7089, 11.9746],
            }
        )
    )
    assert solution(str(fil)) == "c"


def test_ingen_ensam_kastar_valueerror(tmp_path):
    """Ingen ensam dator kastar ValueError."""
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59.3291, 18.0681], "b": [59.3293, 18.0687]}))
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert "'a'" not in str(excinfo.value)
    assert "'b'" not in str(excinfo.value)


def test_flera_ensamma_kastar_valueerror(tmp_path):
    """Flera ensamma datorer kastar ValueError och ett meddelande med datorerna."""
    fil = tmp_path / "flera.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3281, 18.0354],
                "b": [59.3281, 16.0354],
                "c": [59.3281, 18.0354],
                "d": [54.3281, 15.0354],
            }
        )
    )
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert "'b'" in str(excinfo.value)
    assert "'d'" in str(excinfo.value)
    assert "'a'" not in str(excinfo.value)
    assert "'c'" not in str(excinfo.value)


def test_latitud_och_longitud_kravs(tmp_path):
    """Testar att både latitud och longitud jämförs.

    Exemplet har två positioner som är ensamma, varav ena har en annan latitud,
    och den andra en annan longitud.
    """
    fil = tmp_path / "test.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3281, 18.0354],
                "b": [59.3281, 16.0354],
                "c": [53.3281, 18.0354],
                "d": [59.3281, 18.0354],
            }
        )
    )
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert "'b'" in str(excinfo.value)
    assert "'c'" in str(excinfo.value)


if __name__ == "__main__":
    print(solution(TRACKING_JSON))

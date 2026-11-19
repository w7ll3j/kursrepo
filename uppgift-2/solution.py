from pathlib import Path

import pytest

ACCESS_LOG = Path(__file__).parent / "access.log"


def solution(path):
    """Läser loggfilen på sökvägen (path)
    Funktionen returnerar en lista i stigande ordning, innehållande ID:n på personer som
    lämnade datorhallen den 14e augusti mellan timmarna 13 och 18.

    Ett ID består av 5 tecken.
    Tomma rader hoppas över, och trasiga rader kastar ValueError med ett meddelande.
    Ett ID som lämnat hallen flera gånger ska bara stå med en gång.
    """
    with open(path, encoding="utf-8") as fil:
        ids = set()

        for radnummer, rad in enumerate(fil, start=1):
            delar = rad.split()
            if not delar:
                continue

            if len(delar) != 4:
                raise ValueError(
                    f"Rad {radnummer} har fel format. "
                    f"Raden består av {len(delar)}. Det ska vara 4."
                )

            dag, timme, passering, id_ = delar

            try:
                dag_tal = int(dag)
            except ValueError:
                raise ValueError(f'Rad {radnummer}: "{dag}" är inget giltigt heltal.')

            try:
                timme_tal = int(timme)
            except ValueError:
                raise ValueError(f'Rad {radnummer}: "{timme}" är inget giltigt heltal.')

            if not 1 <= dag_tal <= 31:
                raise ValueError(f"Rad {radnummer}: {dag_tal} är ingen giltig dag.")
            if not 0 <= timme_tal <= 23:
                raise ValueError(f"Rad {radnummer}: {timme_tal} är ingen giltig timme.")
            if passering not in ("in", "out"):
                raise ValueError(
                    f'Rad {radnummer}: "{passering}" är inte "in" eller "out".'
                )
            if len(id_) != 5 or id_[0:2] != "id" or not id_[2:].isdecimal():
                raise ValueError(
                    f'Rad {radnummer}: "{id_}" följer inte korrekt format.'
                )

            if dag_tal == 14 and 13 <= timme_tal <= 18 and passering == "out":
                ids.add(id_)

    return sorted(ids)


def test_tomma_rader(tmp_path):
    """Kontrollerar att tomma rader hoppas över"""
    fil = tmp_path / "tom.log"
    fil.write_text(" \n14 16 out id023\n   \n\n")
    assert solution(str(fil)) == ["id023"]


def test_fel_antal_delar(tmp_path):
    """Kontrollerar att ValueError kastas när en rad har fler än 4 delar."""
    fil = tmp_path / "fem.log"
    fil.write_text("2 13 14 out id153")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert (
        str(excinfo.value) == "Rad 1 har fel format. Raden består av 5. Det ska vara 4."
    )


def test_trasiga_siffror(tmp_path):
    """Kontrollerar att ValueError kastas när tid och dag inte är heltal och ligger utanför intervallet."""
    fil = tmp_path / "inget_tal.log"
    fil.write_text("14 hej out id023")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 1: "hej" är inget giltigt heltal.'

    fil = tmp_path / "inget_tal.log"
    fil.write_text("hej 15 out id023")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 1: "hej" är inget giltigt heltal.'

    fil = tmp_path / "fel_timme.log"
    fil.write_text("14 87 out id023")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == "Rad 1: 87 är ingen giltig timme."

    fil = tmp_path / "fel_dag.log"
    fil.write_text("14 16 out id024\n32 16 out id023")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == "Rad 2: 32 är ingen giltig dag."


def test_trasig_passering(tmp_path):
    """Kontrollerar att ValueError kastar när passeringen inte innehåller in eller out"""
    fil = tmp_path / "trasig_passering.log"
    fil.write_text("12 17 out id025\n14 13 in id156\n14 15 fel id023")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 3: "fel" är inte "in" eller "out".'


def test_trasigt_id(tmp_path):
    """Kontrollerar att ValueError kastas när ID inte följer korrekt format."""
    fil = tmp_path / "trasigt_id.log"
    fil.write_text("12 17 out id025\n14 13 in i3034\n14 15 out id047")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 2: "i3034" följer inte korrekt format.'

    fil = tmp_path / "trasigt_id.log"
    fil.write_text("12 17 out id025\n18 14 in id004\n14 15 out id8x1")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 3: "id8x1" följer inte korrekt format.'

    fil = tmp_path / "trasigt_id.log"
    fil.write_text("12 17 out id025\n14 17 out id3456")
    with pytest.raises(ValueError) as excinfo:
        solution(str(fil))
    assert str(excinfo.value) == 'Rad 2: "id3456" följer inte korrekt format.'


def test_fel_dag(tmp_path):
    """Kontrollerar att rader som anger andra dagar än 14 ger en tom lista."""
    fil = tmp_path / "fel_dag.log"
    fil.write_text("13 15 out id023\n15 17 out id024")
    assert solution(str(fil)) == []


def test_fel_tid(tmp_path):
    """Testfil som endast har tid utanför intervall returnerar en tom lista."""
    fil = tmp_path / "fel_tid.log"
    fil.write_text("14 12 out id123\n14 19 out id029\n14 21 out id456")
    assert solution(str(fil)) == []


def test_solution(tmp_path):
    """Testar om nedan påståenden är sanna i utskriften från access.log:
    Returneras endast ID:n?
    Är det en sträng?
    ID består av fler än 4 tecken, och
    Endast innehåller a-z och/eller siffror.
    """
    ids = solution(ACCESS_LOG)
    assert len(ids) > 0, "No ID:s returned"
    assert all(type(id) == str for id in ids), "Not a string"
    assert all(len(id) > 4 for id in ids), "ID should contain at least 4 characters"
    assert all(id.isalnum() for id in ids), (
        "ID should only contain letters a-z or numbers"
    )


def test_fel_passering(tmp_path):
    """Kontrollerar att funktionen inte visar rader med inpassering."""
    fil = tmp_path / "fel_passering.log"
    fil.write_text("14 14 out id001\n14 14 in id002\n")
    assert solution(str(fil)) == ["id001"]


def test_sallar_dubletter(tmp_path):
    """Kontrollerar att funktionen sållar ut dubbletter"""
    fil = tmp_path / "blandad.log"
    fil.write_text(
        "14 12 out id010\n"
        "14 13 out id011\n"
        "14 14 in id012\n"
        "14 15 out id013\n"
        "13 15 out id014\n"
        "14 17 out id013\n"
        "1 14 out id015\n"
        "14 18 out id012\n"
        "14 19 out id016\n"
    )
    assert solution(str(fil)) == ["id011", "id012", "id013"]


if __name__ == "__main__":
    print(solution(ACCESS_LOG))

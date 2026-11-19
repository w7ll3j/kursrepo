import string

alfabet = string.ascii_lowercase
speglat_alfabet = string.ascii_lowercase[::-1]
siffror = string.digits
speglade_siffror = string.digits[::-1]
tecken = alfabet + siffror
speglade_tecken = speglat_alfabet + speglade_siffror

# Sparar kod och gör den mer lättläst gentemot att skriva ut alla par i en ordbok för hand.
speglad_input = dict(zip(tecken, speglade_tecken))


def solution(note):
    """Krypterar och dekrypterar text med Atbash-chiffret.
    Varje liten bokstav ersätts med bokstaven på samma position i det omvända alfabetet.
    a blir exempelvis z, och b blir y.
    Siffror speglas och ersätts på samma sätt. 0 blir 9, och 1 blir 8.
    Stora bokstäver och andra tecken lämnas oförändrade.
    Kryptering och dekryptering fungerar på samma sätt, eftersom ett tecken som speglas två gånger
    ger tillbaka originalet. a blir z, och z blir a.
    Parametern note är en sträng med texten som ska krypteras eller dekrypteras.
    Funktionen returnerar en sträng där små bokstäver och siffror byts ut utifrån Atbash.
    """
    resultat = "".join(
        [speglad_input.get(alla_tecken, alla_tecken) for alla_tecken in note]
    )
    return resultat


def test_abba():
    """De två första bokstäverna i alfabetet visar
    bokstäverna på samma position i det omvända alfabetet
    """
    assert solution("abba") == "zyyz"


def test_mening():
    """Ett exempel på en vanlig mening från en angripare"""
    assert (
        solution("Aoo blfi yzhv ziv yvolmt gl fh!") == "All your base are belong to us!"
    )


def test_siffror():
    """Siffror speglas"""
    assert solution(string.digits) == string.digits[::-1]
    assert solution(string.digits[::-1]) == string.digits


def test_versaler():
    """Stora bokstäver speglas inte"""
    assert solution(string.ascii_uppercase) == string.ascii_uppercase
    assert solution(string.ascii_uppercase[::-1]) == string.ascii_uppercase[::-1]


def test_gemener():
    """Små bokstäver speglas"""
    assert solution(string.ascii_lowercase) == string.ascii_lowercase[::-1]
    assert solution(string.ascii_lowercase[::-1]) == string.ascii_lowercase


def test_ovriga():
    """Andra tecken speglas inte"""
    assert solution(string.punctuation) == string.punctuation
    assert solution(string.punctuation[::-1]) == string.punctuation[::-1]


def test_solution():
    """Testar det krypterade meddelandet. Dekrypteringen fungerar"""
    assert (
        solution(
            "Eiz hvieizi äi oåhgz lxs yzxpfkvimz äi izwvizwv. Sprxpz 24 yrgxlrm uöiv nåmwzt po 90:99, zmmzih häoqvi er pfmwfkktrugvimz kå mägvg!"
        )
        == "Era servrar är låsta och backuperna är raderade. Skicka 75 bitcoin före måndag kl 09:00, annars säljer vi kunduppgifterna på nätet!"
    )


if __name__ == "__main__":
    print(
        solution(
            "Eiz hvieizi äi oåhgz lxs yzxpfkvimz äi izwvizwv. Sprxpz 24 yrgxlrm uöiv nåmwzt po 90:99, zmmzih häoqvi er pfmwfkktrugvimz kå mägvg!"
        )
    )

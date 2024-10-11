"""Diese Datei bietet einen Zuweisungsgenerator per Zufallsprinzip."""

import random
import time


def warte():
    time.sleep(0.8)


def eingabe_namen():    # Teilnehmer für die Verteilung hinzufügen.
    namen = []
    while True:
        print(f"Bisherige Teilnehmer: {", ".join(namen)}")
        warte()
        befehl = input("Bitte Namen eingeben (oder nur Enter, um die Eingabe zu beenden): ")
        if befehl == "":
            break
        else:
            namen.append(befehl)
    return namen


def gruppenschluessel():  # Maximale Anzahl von Teilnehmern je Gruppe
    while True:
        try:
            anzahl = int(input("Maximale Teilnehmerzahl je gruppe eingeben: "))
        except (ValueError, TypeError):
            print("Fehler bei der Eingabe!")
            warte()
        else:
            return anzahl


def zufallsgenerator():
    namensliste = []
    gruppen = [[]]
    namen = eingabe_namen()
    teilnehmer = gruppenschluessel()
    for element in namen:
        namensliste.append(element)
    for element in range(len(namensliste)):
        name = random.choice(namensliste)
        namensliste.remove(name)
        if len(gruppen[-1]) < teilnehmer:
            gruppen[-1].append(name)
        else:
            gruppen.append([name])

    while not paritaet(gruppen):
        umverteilen(gruppen)
    gruppennummer = 1           # Ausgabe
    for gruppe in gruppen:
        if len(gruppe) > 0:
            print(f"Gruppe {gruppennummer}: {", ".join(gruppe)}")
            gruppennummer += 1
            warte()


def paritaet(gruppen):
    groessen = [len(gruppe) for gruppe in gruppen]
    for gruppe in gruppen:
        if len(gruppe) < 2 and len(gruppen) > 1:  # Keine Gruppe soll weniger als zwei Mitglieder haben.
            return False
    return max(groessen) - min(groessen) <= 1


def umverteilen(gruppen):
    # Listen vereinfachen
    alle_namen = [name for gruppe in gruppen for name in gruppe]
    random.shuffle(alle_namen)

    # Mindest- und Höchstanzahl festlegen
    anzahl_gruppen = len(gruppen)
    teilnehmer_pro_gruppe, rest = divmod(len(alle_namen), anzahl_gruppen)

    # Gruppen neu mischen
    for element in range(anzahl_gruppen):
        gruppen[element] = alle_namen[element * teilnehmer_pro_gruppe: (element + 1) * teilnehmer_pro_gruppe]

    # Den Rest aufteilen
    for element in range(rest):
        gruppen[element].append(alle_namen[anzahl_gruppen * teilnehmer_pro_gruppe + element])


zufallsgenerator()

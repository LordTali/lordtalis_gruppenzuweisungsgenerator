"""Diese Datei bietet einen Zuweisungsgenerator per Zufallsprinzip."""

import random
import tkinter
from tkinter import scrolledtext, messagebox


def anzeigepause():
    global gruppennummer
    if gruppennummer <= len(gruppen):
        gruppe = gruppen[gruppennummer - 1]  # Get the current group
        if len(gruppe) > 0:
            ergebnis_feld.insert(tkinter.END, f"Gruppe {gruppennummer}: {', '.join(gruppe)}\n\n")
        gruppennummer += 1
        fenster.after(800, anzeigepause)


def eingabe_namen():    # Teilnehmer für die Verteilung hinzufügen.
    namen = namen_feld.get("1.0", tkinter.END).strip().splitlines()
    if not namen:
        messagebox.showerror("Fehler bei der Eingabe", "Bitte mindestens einen Namen eintragen.")
        return None
    return namen


def gruppenschluessel():  # Maximale Anzahl von Teilnehmern je Gruppe
    try:
        max_teilnehmer = int(max_teilnehmer_eingabe.get())
        if max_teilnehmer < 2:
            raise ValueError("Die Mindestanzahl der Teilnehmer pro Gruppe ist 2.")
    except ValueError:
        messagebox.showerror("Fehler bei der Eingabe",
                             "Die Mindestanzahl der Teilnehmer pro Gruppe ist 2.")
        return None
    return max_teilnehmer


def zufallsgenerator():
    global gruppen, gruppennummer
    namen = eingabe_namen()
    teilnehmer = gruppenschluessel()
    if not namen or not teilnehmer:
        return
    namensliste = namen.copy()          # Die Namen aus der GUI holen
    gruppen = [[]]                      # Gruppenliste initialisieren.
    for element in range(len(namensliste)):
        name = random.choice(namensliste)
        namensliste.remove(name)
        if len(gruppen[-1]) < teilnehmer:
            gruppen[-1].append(name)
        else:
            gruppen.append([name])
    while not paritaet(gruppen):
        umverteilen(gruppen)
    ergebnis_feld.delete(1.0, tkinter.END)
    gruppennummer = 1
    fenster.after(800, anzeigepause)


def paritaet(gruppen):
    groessen = [len(gruppe) for gruppe in gruppen]
    for gruppe in gruppen:
        if len(gruppe) < 2 and len(gruppen) > 1:  # Keine Gruppe soll weniger als zwei Mitglieder haben.
            return False
    return max(groessen) - min(groessen) <= 1


def umverteilen(gruppen):       # Hilfe von ChatGPT
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


# GUI erstellen

fenster = tkinter.Tk()
fenster.title("LordTalis Gruppenzuweisungsgenerator")
fenster.geometry("550x550")
fenster.resizable(False, False)
fenster.configure(bg="")

# Eingabefeld für Teilnehmer und Gruppengröße
eingabe_frame = tkinter.Frame(fenster)
eingabe_frame.pack(pady=10)

# Eingabe Name
tkinter.Label(eingabe_frame, text="Bitte Namen eingeben (ein Name pro Zeile):").pack(anchor='w')
namen_feld = scrolledtext.ScrolledText(eingabe_frame, width=60, height=10)
namen_feld.pack(pady=5)

# Maximale Teilnehmer grafisch festlegen.
tkinter.Label(eingabe_frame, text="Höchstanzahl der Teilnehmer pro Gruppe:").pack(anchor='w')
max_teilnehmer_eingabe = tkinter.Entry(eingabe_frame, width=5)
max_teilnehmer_eingabe.pack(pady=5)

# Die Schalfläche zum Erstellen der Gruppen
schaltflaeche = tkinter.Button(eingabe_frame, text="Gruppen erstellen", command=zufallsgenerator)
schaltflaeche.pack(pady=10)

# Ergebnis anzeigen
anzeige_frame = tkinter.Frame(fenster)
anzeige_frame.pack(pady=10)

# Ergebnisfeld
tkinter.Label(anzeige_frame, text="Erstellte Gruppen:").pack(anchor='w')
ergebnis_feld = scrolledtext.ScrolledText(anzeige_frame, width=60, height=10)
ergebnis_feld.pack(pady=5)

fenster.configure(bg="#D3C9E0")  # Lavendel
eingabe_frame.configure(bg="#A8D8A1")  # dunkelgrün
anzeige_frame.configure(bg="#A8D8A1")  # dunkelgrün

fenster.mainloop()

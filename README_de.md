## Nejistota_posuvka_3.0

[![Čeština](https://flagcdn.com/w20/cz.png)](README.md) [![English](https://flagcdn.com/w20/gb.png)](README_en.md) [![Deutsch](https://flagcdn.com/w20/de.png)](README_de.md)

Anwendung zur Berechnung der Messunsicherheit bei Messungen mit einer Schieblehre. Die grafische Benutzeroberfläche wird mit **customtkinter** (modernes Erscheinungsbild für Tkinter) erstellt.

Die Anwendung unterstützt derzeit folgende Sprachen für Bedienoberfläche und Messprotokoll:

- Tschechisch (cs)
- Englisch (en)
- Deutsch (de)

Die Sprache kann über die Flaggen-Schaltflächen in der unteren rechten Ecke des Hauptfensters umgeschaltet werden.

### Voraussetzungen

- Python 3.8 oder neuer
- Windows (empfohlen)

### Installation

1. Dieses Repository klonen oder als ZIP herunterladen.
2. Im Projektwurzelverzeichnis die Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

### Anwendung starten

Im Projektverzeichnis ausführen:

```bash
python posuvka.py
```

Nach dem Start öffnet sich ein Fenster mit dem Titel „Výpočet nejistoty měření posuvné měřítko“ (Berechnung der Messunsicherheit einer Schieblehre).

### Bedienung

- Im Feld **Zadej hodnoty** (Werte eingeben) die gemessenen Werte eingeben (als Dezimaltrennzeichen sind Komma oder Punkt möglich) und mit der Schaltfläche **Zadej** (Hinzufügen) oder der Eingabetaste bestätigen.
- Mit den Schaltflächen **Odstranit** (Entfernen) und **Odstraň vše** (Alles entfernen) können einzelne oder alle Werte aus der Liste gelöscht werden.
- Im Feld **Zadej rozlišení měřidla** (Auflösung des Messmittels) die Auflösung der verwendeten Schieblehre eingeben.
- Optional können **Abbe-Fehler** und **Temperatureinfluss** über Kontrollkästchen in die Berechnung ein- oder ausgeschlossen werden.
- Mit **Vypočítej** (Berechnen) werden berechnet:
  - die Unsicherheit vom Typ A,
  - die Anteile der Unsicherheit vom Typ B (Abbe-Fehler, Temperatureinfluss, Ablesefehler),
  - die kombinierte Standardunsicherheit,
  - die erweiterte Unsicherheit,
  - sowie das Messergebnis in der Form _x ± U_ [mm].

Weitere Funktionen:

- **Diagramm und Protokoll** – mit der Schaltfläche **Graf** (Diagramm) wird ein neues Fenster mit einem Diagramm der Messwerte und einem vollständigen Textprotokoll im A4-Layout geöffnet.
- **Export nach PDF** – mit der Schaltfläche **Protokol PDF** (oder der Schaltfläche im Diagrammfenster) kann das Protokoll direkt als PDF-Datei gespeichert werden.
- **Logo im Protokoll** – im Menü **Soubor** (Datei) kann das im Programm und im PDF-Protokoll verwendete Logo geändert oder auf das Standardlogo zurückgesetzt werden.
- **Design-Themen** – im Menü **Motiv** (Design) kann zwischen System-, hellem und dunklem Design gewechselt werden.
- **Info über die Anwendung** – im Menü **Nápověda → O aplikaci** (Hilfe → Über) wird ein Dialog mit grundlegenden Informationen zur Anwendung angezeigt.
- **Sprachauswahl** – in der rechten unteren Ecke des Hauptfensters befinden sich drei Flaggen (🇨🇿/🇬🇧/🇩🇪) zum schnellen Umschalten der Sprache der Oberfläche und des Protokolls.

### Projektstruktur

- `posuvka.py` – Hauptskript der Anwendung mit GUI, Berechnung der Messunsicherheit, Diagrammerstellung und PDF-Protokoll.
- `translations.py` – Sprachschicht (`cs`, `en`, `de`) für Texte in der Oberfläche, Meldungen und im Protokoll.
- `requirements.txt` – Liste der Python-Abhängigkeiten.
- `img/` – Bilder, z. B. das Standardlogo der Anwendung `sumixon130x50_black.png`.

### Lizenz

Copyright © 2024–2026 Sumixon

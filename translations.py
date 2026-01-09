import math

# Aktuální jazyk aplikace (cs / en / de)
CURRENT_LANG = "cs"

TEXTS = {
    "cs": {
        # Základní aplikace
        "app_title": "Výpočet nejistoty měření posuvné měřítko",

        # Menu
        "menu_file": "Soubor",
        "menu_file_open": "Otevřít",
        "menu_file_save": "Uložit",
        "menu_file_change_logo": "Změnit logo…",
        "menu_file_reset_logo": "Obnovit výchozí logo",
        "menu_file_exit": "Ukončit",

        "menu_edit": "Upravit",
        "menu_edit_cut": "Vyjmout",
        "menu_edit_copy": "Kopírovat",
        "menu_edit_paste": "Vložit",

        "menu_help": "Nápověda",
        "menu_help_about": "O aplikaci",

        "menu_theme": "Motiv",
        "menu_theme_system": "Systémový motiv",
        "menu_theme_light": "Světlý motiv",
        "menu_theme_dark": "Tmavý motiv",

        # Vstupní hodnoty vlevo
        "input_measured_values": "Naměřené hodnoty",
        "input_enter_values": "Zadej hodnoty",
        "input_button_add": "Zadej",
        "input_button_remove": "Odstranit",
        "input_button_remove_all": "Odstraň vše",

        # Střední panel – výpočet
        "calc_title": "Výpočet nejistoty",
        "calc_resolution_label": "Zadej rozlišení měřidla",
        "calc_A_label": "Nejistota typu A",
        "calc_B_group": "Složky nejistoty typu B",
        "calc_abbe_label": "Abbeho chyba",
        "calc_temp_label": "Vliv teploty 21 ± 1 °C",
        "calc_reading_error": "Chyba odečtu",
        "calc_combined": "Kombinovaná nejistota A/B",
        "calc_expanded": "Rozšířená nejistota U",
        "calc_result_title": "Výsledek měření",
        "calc_checkbox_include": "Zahrnout\n do výpočtu",

        # Pravý panel – ostatní info
        "right_count_label": "Počet zadaných hodnot",
        "right_part_name": "Název dílu",
        "right_part_mat": "Materiálové číslo",
        "right_nominal": "Nominální hodnota [mm]",
        "right_tol_lower": "Spodní tolerance [mm]",
        "right_tol_upper": "Horní tolerance [mm]",

        "right_proto_number": "Číslo protokolu",
        "right_operator": "Operátor měření",
        "right_gauge": "Použité měřidlo",
        "right_note": "Poznámka / akreditace",

        "button_calculate": "Vypočítej",
        "button_chart": "Graf",
        "button_pdf": "Protokol PDF",

        # Copyright
        "copyright": "Copyright © 2024-2026 Sumixon",

        # Hlášky / messageboxy / varování
        "warn_empty_value": "Zadal jste prázdnou hodnotu.",
        "warn_min_values": "Zadej minimálně dvě hodnoty.",
        "warn_not_number": "Některá zadaná hodnota není číslo.",
        "warn_resolution_missing": "Zadej rozlišení měřidla.",
        "warn_resolution_not_number": "Rozlišení měřidla musí být číslo.",
        "warn_graph_min_values": "Pro graf zadej minimálně dvě hodnoty.",
        "warn_graph_resolution_missing": "Pro graf zadej také rozlišení měřidla.",
        "warn_nominal_numbers": "Nominál a tolerance musí být čísla.",
        "warn_proto_min_values": "Pro protokol zadej minimálně dvě hodnoty.",
        "warn_proto_resolution_missing": "Pro protokol zadej také rozlišení měřidla.",

        # Messagebox – logo
        "msg_logo_error_title": "Chyba načtení loga",
        "msg_logo_error_text": "Obrázek se nepodařilo načíst.",
        "msg_logo_default_error_title": "Chyba načtení výchozího loga",
        "msg_logo_default_error_text": "Výchozí logo se nepodařilo načíst.",

        # Messagebox – O aplikaci
        "msg_about_title": "O aplikaci",
        "msg_about_text": (
            "Výpočet nejistoty měření – posuvné měřítko\n\n"
            "Verze: 3.0\n"
            "Autor: Sumixon\n\n"
            "Aplikace slouží k výpočtu nejistoty typu A a B,\n"
            "k určení kombinované a rozšířené nejistoty U\n"
            "pro měření posuvným měřítkem a k vytvoření\n"
            "protokolu s grafem včetně exportu do PDF."
        ),

        # Protokol – nadpisy a texty
        "proto_title": "PROTOKOL O MĚŘENÍ – posuvné měřítko",
        "proto_header_title": "PROTOKOL O MĚŘENÍ – Výsledné údaje",
        "proto_number": "Číslo protokolu:",
        "proto_datetime": "Datum a čas měření:",
        "proto_operator": "Operátor měření:",
        "proto_gauge": "Použité měřidlo:",

        "proto_info_part": "Informace o předmětu měření:",
        "proto_part_name": "  Název dílu:",
        "proto_part_mat": "  Materiálové číslo:",
        "proto_nominal": "  Nominální hodnota:",
        "proto_tol_lower": "  Spodní tolerance:",
        "proto_tol_upper": "  Horní tolerance:",

        "proto_summary": "Shrnutí výsledku:",
        "proto_avg": "  Průměrná hodnota:",
        "proto_u": "  Rozšířená nejistota U (k = 2):",
        "proto_u_note": "  Uvedená nejistota odpovídá přibližně 95% hladině spolehlivosti.",
        "proto_conclusion": "  Vyhodnocení shody s tolerancí:",

        "proto_values": "Naměřené hodnoty [mm]:",
        "proto_note": "Poznámka:",

        # Protokol – vyhodnocení shody
        "proto_ok": "VYHOVUJE (interval měření včetně nejistoty je celý v toleranci).",
        "proto_nok": "NEVYHOVUJE (interval měření včetně nejistoty leží mimo tolerance).",
        "proto_unclear": "NELZE JEDNOZNAČNĚ POSOUDIT\n (interval měření včetně nejistoty překrývá hraniční hodnoty).",

        # Graf
        "chart_y_label": "Hodnota [mm]",
        "chart_x_label": "Pořadí měření",
        "chart_title": "Naměřené hodnoty, průměr, nominál a tolerance",
        "chart_series_nominal": "Nominální hodnota",
        "chart_series_tol_lower": "Spodní tolerance",
        "chart_series_tol_upper": "Horní tolerance",
        "chart_series_mean": "Průměr",
        "chart_series_values": "Hodnoty ± U",

        # Uložení PDF
        "filedialog_pdf_title_chart": "Uložit graf jako PDF",
        "filedialog_pdf_title_proto": "Uložit protokol do PDF",
        "filedialog_pdf_type_pdf": "PDF soubory",
        "filedialog_pdf_type_all": "Všechny soubory",
    },

    "en": {
        # Base application
        "app_title": "Measurement uncertainty – caliper",

        # Menu
        "menu_file": "File",
        "menu_file_open": "Open",
        "menu_file_save": "Save",
        "menu_file_change_logo": "Change logo…",
        "menu_file_reset_logo": "Reset default logo",
        "menu_file_exit": "Exit",

        "menu_edit": "Edit",
        "menu_edit_cut": "Cut",
        "menu_edit_copy": "Copy",
        "menu_edit_paste": "Paste",

        "menu_help": "Help",
        "menu_help_about": "About",

        "menu_theme": "Theme",
        "menu_theme_system": "System theme",
        "menu_theme_light": "Light theme",
        "menu_theme_dark": "Dark theme",

        # Left – measured values
        "input_measured_values": "Measured values",
        "input_enter_values": "Enter values",
        "input_button_add": "Add",
        "input_button_remove": "Remove",
        "input_button_remove_all": "Remove all",

        # Center – calculation
        "calc_title": "Uncertainty calculation",
        "calc_resolution_label": "Enter instrument resolution",
        "calc_A_label": "Type A uncertainty",
        "calc_B_group": "Type B uncertainty components",
        "calc_abbe_label": "Abbe error",
        "calc_temp_label": "Temperature influence 21 ± 1 °C",
        "calc_reading_error": "Reading error",
        "calc_combined": "Combined uncertainty A/B",
        "calc_expanded": "Expanded uncertainty U",
        "calc_result_title": "Measurement result",
        "calc_checkbox_include": "Include\n in calculation",

        # Right – additional info
        "right_count_label": "Number of entered values",
        "right_part_name": "Part name",
        "right_part_mat": "Material number",
        "right_nominal": "Nominal value [mm]",
        "right_tol_lower": "Lower tolerance [mm]",
        "right_tol_upper": "Upper tolerance [mm]",

        "right_proto_number": "Protocol number",
        "right_operator": "Measurement operator",
        "right_gauge": "Instrument used",
        "right_note": "Note / accreditation",

        "button_calculate": "Calculate",
        "button_chart": "Chart",
        "button_pdf": "Protocol PDF",

        # Copyright
        "copyright": "Copyright © 2024-2026 Sumixon",

        # Warnings / message boxes
        "warn_empty_value": "You entered an empty value.",
        "warn_min_values": "Enter at least two values.",
        "warn_not_number": "One of the entered values is not a number.",
        "warn_resolution_missing": "Enter instrument resolution.",
        "warn_resolution_not_number": "Instrument resolution must be a number.",
        "warn_graph_min_values": "For the chart, enter at least two values.",
        "warn_graph_resolution_missing": "For the chart, also enter the instrument resolution.",
        "warn_nominal_numbers": "Nominal and tolerances must be numbers.",
        "warn_proto_min_values": "For the protocol, enter at least two values.",
        "warn_proto_resolution_missing": "For the protocol, also enter the instrument resolution.",

        # Messagebox – logo
        "msg_logo_error_title": "Logo load error",
        "msg_logo_error_text": "The image could not be loaded.",
        "msg_logo_default_error_title": "Default logo load error",
        "msg_logo_default_error_text": "The default logo could not be loaded.",

        # Messagebox – About
        "msg_about_title": "About",
        "msg_about_text": (
            "Measurement uncertainty – caliper\n\n"
            "Version: 3.0\n"
            "Author: Sumixon\n\n"
            "The application calculates type A and B uncertainty,\n"
            "combined and expanded uncertainty U for measurements\n"
            "with a caliper and generates a report with a chart,\n"
            "including export to PDF."
        ),

        # Protocol – headings and text
        "proto_title": "MEASUREMENT PROTOCOL – caliper",
        "proto_header_title": "MEASUREMENT PROTOCOL – Final data",
        "proto_number": "Protocol number:",
        "proto_datetime": "Measurement date and time:",
        "proto_operator": "Measurement operator:",
        "proto_gauge": "Instrument used:",

        "proto_info_part": "Information about the measured part:",
        "proto_part_name": "  Part name:",
        "proto_part_mat": "  Material number:",
        "proto_nominal": "  Nominal value:",
        "proto_tol_lower": "  Lower tolerance:",
        "proto_tol_upper": "  Upper tolerance:",

        "proto_summary": "Result summary:",
        "proto_avg": "  Average value:",
        "proto_u": "  Expanded uncertainty U (k = 2):",
        "proto_u_note": "  The stated uncertainty corresponds approximately to the 95% confidence level.",
        "proto_conclusion": "  Conformity assessment with tolerance:",

        "proto_values": "Measured values [mm]:",
        "proto_note": "Note:",

        # Protocol – conformity assessment
        "proto_ok": "CONFORMING (the interval of measurement including uncertainty is fully within tolerance).",
        "proto_nok": "NON-CONFORMING (the interval of measurement including uncertainty lies outside tolerance).",
        "proto_unclear": "INCONCLUSIVE (the interval of measurement including uncertainty overlaps the limit values).",

        # Chart
        "chart_y_label": "Value [mm]",
        "chart_x_label": "Measurement index",
        "chart_title": "Measured values, mean, nominal and tolerance",
        "chart_series_nominal": "Nominal value",
        "chart_series_tol_lower": "Lower tolerance",
        "chart_series_tol_upper": "Upper tolerance",
        "chart_series_mean": "Mean",
        "chart_series_values": "Values ± U",

        # Save PDF
        "filedialog_pdf_title_chart": "Save chart as PDF",
        "filedialog_pdf_title_proto": "Save protocol as PDF",
        "filedialog_pdf_type_pdf": "PDF files",
        "filedialog_pdf_type_all": "All files",
    },

    "de": {
        # Grundanwendung
        "app_title": "Messunsicherheit – Messschieber",

        # Menü
        "menu_file": "Datei",
        "menu_file_open": "Öffnen",
        "menu_file_save": "Speichern",
        "menu_file_change_logo": "Logo ändern…",
        "menu_file_reset_logo": "Standardlogo wiederherstellen",
        "menu_file_exit": "Beenden",

        "menu_edit": "Bearbeiten",
        "menu_edit_cut": "Ausschneiden",
        "menu_edit_copy": "Kopieren",
        "menu_edit_paste": "Einfügen",

        "menu_help": "Hilfe",
        "menu_help_about": "Über das Programm",

        "menu_theme": "Design",
        "menu_theme_system": "Systemdesign",
        "menu_theme_light": "Helles Design",
        "menu_theme_dark": "Dunkles Design",

        # Linke Seite – Messwerte
        "input_measured_values": "Messwerte",
        "input_enter_values": "Werte eingeben",
        "input_button_add": "Hinzufügen",
        "input_button_remove": "Entfernen",
        "input_button_remove_all": "Alle entfernen",

        # Mitte – Berechnung
        "calc_title": "Berechnung der Unsicherheit",
        "calc_resolution_label": "Auflösung des Messmittels eingeben",
        "calc_A_label": "Unsicherheit Typ A",
        "calc_B_group": "Unsicherheitskomponenten Typ B",
        "calc_abbe_label": "Abbe-Fehler",
        "calc_temp_label": "Temperatureinfluss 21 ± 1 °C",
        "calc_reading_error": "Ablesefehler",
        "calc_combined": "Kombinierte Unsicherheit A/B",
        "calc_expanded": "Erweiterte Unsicherheit U",
        "calc_result_title": "Messergebnis",
        "calc_checkbox_include": "In Berechnung\n einbeziehen",

        # Rechte Seite – weitere Infos
        "right_count_label": "Anzahl der eingegebenen Werte",
        "right_part_name": "Teilename",
        "right_part_mat": "Materialnummer",
        "right_nominal": "Nennmaß [mm]",
        "right_tol_lower": "Untere Toleranz [mm]",
        "right_tol_upper": "Obere Toleranz [mm]",

        "right_proto_number": "Protokollnummer",
        "right_operator": "Messoperator",
        "right_gauge": "Verwendetes Messmittel",
        "right_note": "Bemerkung / Akkreditierung",

        "button_calculate": "Berechnen",
        "button_chart": "Diagramm",
        "button_pdf": "Protokoll PDF",

        # Copyright
        "copyright": "Copyright © 2024-2026 Sumixon",

        # Warnungen / Meldungen
        "warn_empty_value": "Sie haben einen leeren Wert eingegeben.",
        "warn_min_values": "Geben Sie mindestens zwei Werte ein.",
        "warn_not_number": "Einer der eingegebenen Werte ist keine Zahl.",
        "warn_resolution_missing": "Geben Sie die Auflösung des Messmittels ein.",
        "warn_resolution_not_number": "Die Auflösung des Messmittels muss eine Zahl sein.",
        "warn_graph_min_values": "Für das Diagramm mindestens zwei Werte eingeben.",
        "warn_graph_resolution_missing": "Für das Diagramm auch die Auflösung des Messmittels eingeben.",
        "warn_nominal_numbers": "Nennmaß und Toleranzen müssen Zahlen sein.",
        "warn_proto_min_values": "Für das Protokoll mindestens zwei Werte eingeben.",
        "warn_proto_resolution_missing": "Für das Protokoll auch die Auflösung des Messmittels eingeben.",

        # Meldungsfenster – Logo
        "msg_logo_error_title": "Fehler beim Laden des Logos",
        "msg_logo_error_text": "Das Bild konnte nicht geladen werden.",
        "msg_logo_default_error_title": "Fehler beim Laden des Standardlogos",
        "msg_logo_default_error_text": "Das Standardlogo konnte nicht geladen werden.",

        # Meldungsfenster – Über das Programm
        "msg_about_title": "Über das Programm",
        "msg_about_text": (
            "Messunsicherheit – Messschieber\n\n"
            "Version: 3.0\n"
            "Autor: Sumixon\n\n"
            "Die Anwendung berechnet die Unsicherheit Typ A und B,\n"
            "kombinierte und erweiterte Unsicherheit U für Messungen\n"
            "mit einem Messschieber und erstellt ein Protokoll mit\n"
            "Diagramm einschließlich Export in PDF."
        ),

        # Protokoll – Überschriften und Texte
        "proto_title": "MESSPROTOKOLL – Messschieber",
        "proto_header_title": "MESSPROTOKOLL – Ergebnisdaten",
        "proto_number": "Protokollnummer:",
        "proto_datetime": "Messdatum und -zeit:",
        "proto_operator": "Messoperator:",
        "proto_gauge": "Verwendetes Messmittel:",

        "proto_info_part": "Informationen zum Prüfteil:",
        "proto_part_name": "  Teilename:",
        "proto_part_mat": "  Materialnummer:",
        "proto_nominal": "  Nennmaß:",
        "proto_tol_lower": "  Untere Toleranz:",
        "proto_tol_upper": "  Obere Toleranz:",

        "proto_summary": "Ergebniszusammenfassung:",
        "proto_avg": "  Mittelwert:",
        "proto_u": "  Erweiterte Unsicherheit U (k = 2):",
        "proto_u_note": "  Die angegebene Unsicherheit entspricht etwa einem Vertrauensniveau von 95%.",
        "proto_conclusion": "  Beurteilung der Übereinstimmung mit der Toleranz:",

        "proto_values": "Messwerte [mm]:",
        "proto_note": "Bemerkung:",

        # Protokoll – Konformitätsbewertung
        "proto_ok": "ENTSPRICHT (das Messintervall mit Unsicherheit liegt vollständig innerhalb der Toleranz).",
        "proto_nok": "ENTSPRICHT NICHT (das Messintervall mit Unsicherheit liegt außerhalb der Toleranz).",
        "proto_unclear": "NICHT EINDEUTIG (das Messintervall mit Unsicherheit überlappt die Grenzwerte).",

        # Diagramm
        "chart_y_label": "Wert [mm]",
        "chart_x_label": "Messindex",
        "chart_title": "Messwerte, Mittelwert, Nennmaß und Toleranz",
        "chart_series_nominal": "Nennmaß",
        "chart_series_tol_lower": "Untere Toleranz",
        "chart_series_tol_upper": "Obere Toleranz",
        "chart_series_mean": "Mittelwert",
        "chart_series_values": "Werte ± U",

        # PDF speichern
        "filedialog_pdf_title_chart": "Diagramm als PDF speichern",
        "filedialog_pdf_title_proto": "Protokoll als PDF speichern",
        "filedialog_pdf_type_pdf": "PDF-Dateien",
        "filedialog_pdf_type_all": "Alle Dateien",
    },
}


def t(key: str) -> str:
    """Vrátí lokalizovaný text pro daný klíč.

    Pokud pro daný jazyk/klíč neexistuje text,
    vrátí samotný klíč.
    """

    return TEXTS.get(CURRENT_LANG, TEXTS["cs"]).get(key, key)


def set_language(lang: str) -> None:
    """Nastaví aktuální jazyk aplikace.

    Neplatný jazyk se přepne na "cs".
    """

    global CURRENT_LANG

    if lang not in TEXTS:
        lang = "cs"
    CURRENT_LANG = lang

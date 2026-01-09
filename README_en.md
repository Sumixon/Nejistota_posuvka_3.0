## Nejistota_posuvka_3.0

[![Čeština](https://flagcdn.com/w20/cz.png)](README.md) [![English](https://flagcdn.com/w20/gb.png)](README_en.md) [![Deutsch](https://flagcdn.com/w20/de.png)](README_de.md)

Application for calculating measurement uncertainty when using a vernier caliper. The graphical user interface is built with **customtkinter** (a modern look for Tkinter).

The application currently supports the following interface and report languages:

- Czech (cs)
- English (en)
- German (de)

Language can be switched by clicking the flag buttons in the lower right corner of the main window.

### Requirements

- Python 3.8 or newer
- Windows (recommended)

### Installation

1. Clone or download this repository.
2. In the project root folder, install dependencies:

```bash
pip install -r requirements.txt
```

### Running the application

In the project directory, run:

```bash
python posuvka.py
```

After start, a window titled "Measurement uncertainty of a vernier caliper" will appear.

### How to use

- In the **Enter values** field, enter measured values (decimal separator can be comma or dot) and confirm with the **Add** button or the Enter key.
- Use **Remove** and **Remove all** buttons to delete single or all values from the list.
- In the **Resolution of the gauge** field, enter the resolution of the caliper used.
- Optionally, you can include or exclude **Abbe error** and **temperature influence** in the calculation using the checkboxes.
- Press **Vypočítej** (Calculate) to compute:
  - type A uncertainty,
  - components of type B uncertainty (Abbe error, temperature influence, reading error),
  - combined standard uncertainty,
  - expanded uncertainty,
  - and the measurement result in the form _x ± U_ [mm].

Additional features:

- **Graph and report** – the **Chart** button opens a new window with a chart of measured values and a complete text report laid out on an A4 page.
- **Export to PDF** – the button for the PDF report (or the button in the chart window) lets you save the report directly to a PDF file.
- **Logo in the report** – in the **File** menu you can change the logo image used both in the application and in the PDF report, or revert to the default logo.
- **Themes** – in the **Theme** menu you can switch between system, light and dark appearance.
- **About dialog** – in the **Help → About** menu you can open a small dialog with basic information about the application.
- **Language selection** – in the bottom-right corner of the main window there are three flags (🇨🇿/🇬🇧/🇩🇪) for quickly switching the GUI and report language.

### Project structure

- `posuvka.py` – main application script with GUI, uncertainty calculation, chart rendering and PDF report generation.
- `translations.py` – language layer (`cs`, `en`, `de`) for GUI texts, messages and report content.
- `requirements.txt` – list of Python dependencies.
- `img/` – images, e.g. the default application logo `sumixon130x50_black.png`.

### License

Copyright © 2024–2026 Sumixon

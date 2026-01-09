## Nejistota_posuvka_3.0

Aplikace pro výpočet nejistoty měření při měření posuvným měřítkem. Grafické rozhraní je vytvořené pomocí knihovny **customtkinter** (moderní vzhled pro Tkinter).

Aplikace aktuálně podporuje tyto jazyky rozhraní i výstupního protokolu:

- čeština (cs)
- angličtina (en)
- němčina (de)

Přepínání jazyka probíhá kliknutím na vlaječky v pravém dolním rohu hlavního okna.

### Požadavky

- Python 3.8 nebo novější
- Windows (doporučeno)

### Instalace

1. Naklonujte nebo stáhněte tento repozitář.
2. V kořenové složce projektu nainstalujte závislosti:

```bash
pip install -r requirements.txt
```

### Spuštění aplikace

V adresáři projektu spusťte:

```bash
python posuvka.py
```

Po spuštění se otevře okno aplikace „Výpočet nejistoty měření posuvné měřítko“.

### Popis použití

- Do pole **Zadej hodnoty** zadávejte naměřené hodnoty (desetinný oddělovač může být čárka i tečka) a potvrďte tlačítkem **Zadej** nebo klávesou Enter.
- Tlačítky **Odstranit** a **Odstraň vše** můžete mazat jednotlivé nebo všechny hodnoty.
- Do pole **Zadej rozlišení měřidla** zadejte rozlišení použitého posuvného měřítka.
- Volitelně můžete přepínat zahrnutí **Abbeho chyby** a **vlivu teploty** do výpočtu pomocí zaškrtávacích polí.
- Stiskněte tlačítko **Vypočítej** pro výpočet:
  - nejistoty typu A,
  - složek nejistoty typu B (Abbeho chyba, vliv teploty, chyba odečtu),
  - kombinované nejistoty,
  - rozšířené nejistoty,
  - a výsledku měření ve tvaru _x ± U_ [mm].

Další funkce:

- **Graf a protokol** – tlačítko **Graf** otevře nové okno s grafem naměřených hodnot a kompletním textovým protokolem na formátu A4.
- **Export do PDF** – tlačítko **Protokol PDF** (nebo tlačítko v okně grafu) umožňuje uložit protokol přímo do PDF.
- **Logo v protokolu** – v menu **Soubor** můžete změnit obrázek loga, který se zobrazuje jak v aplikaci, tak v PDF protokolu, nebo se vrátit k výchozímu logu.
- **Motivy vzhledu** – v menu **Motiv** lze přepnout mezi systémovým, světlým a tmavým vzhledem.
- **O aplikaci** – v menu **Nápověda → O aplikaci** je k dispozici stručná informace o programu.
- **Výběr jazyka** – v pravém dolním rohu okna jsou tři vlaječky (🇨🇿/🇬🇧/🇩🇪) pro rychlé přepnutí jazyka GUI i protokolu.

### Struktura projektu

- `posuvka.py` – hlavní skript aplikace s GUI, výpočtem nejistoty, generováním grafu a PDF protokolu.
- `translations.py` – jazyková vrstva (`cs`, `en`, `de`) pro texty v GUI, hláškách a protokolu.
- `requirements.txt` – seznam Python závislostí.
- `img/` – obrázky, např. výchozí logo aplikace `sumixon130x50_black.png`.

### Licence

Copyright © 2024–2026 Sumixon

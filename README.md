## Nejistota_posuvka_3.0

Aplikace pro výpočet nejistoty měření při měření posuvným měřítkem. Grafické rozhraní je vytvořené pomocí knihovny **customtkinter** (moderní vzhled pro Tkinter).

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
	- a výsledku měření ve tvaru *x ± U* [mm].

### Struktura projektu

- `posuvka.py` – hlavní skript aplikace s GUI a výpočtem nejistoty.
- `requirements.txt` – seznam Python závislostí.
- `img/` – obrázky, např. logo aplikace `sumixon130x50_black.png`.

### Licence

Copyright © 2024–2026 Sumixon

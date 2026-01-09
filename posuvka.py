import math
import os
from datetime import datetime
import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import matplotlib.image as mpimg


# Definování stylů a cest
main_color = "grey"
main_font = ("Helvetica", 16)
second_font = ("Helvetica", 14)

# Výchozí logo pro aplikaci i PDF protokol
DEFAULT_PROTOCOL_LOGO_PATH = "img/sumixon130x50_black.png"
# Aktuálně používané logo (může být změněno uživatelem během běhu aplikace)
PROTOCOL_LOGO_PATH = DEFAULT_PROTOCOL_LOGO_PATH

# Maximální rozměry loga v GUI (pixely)
GUI_LOGO_MAX_WIDTH = 180
GUI_LOGO_MAX_HEIGHT = 80

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


def change_theme(mode: str):
    """Změna motivu aplikace: "system" | "light" | "dark"."""
    if mode == "light":
        ctk.set_appearance_mode("light")
    elif mode == "dark":
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("system")

#  Okno
window = ctk.CTk()
width = 1150
height = 700
window.geometry(f"{width}x{height}")
window.minsize(width, height)
window.resizable(True, True)
window.title("Výpočet nejistoty měření posuvné měřítko")


def _nacist_logo_do_gui(cesta: str) -> tk.PhotoImage:
    """Načte obrázek loga a případně ho zmenší na rozumnou velikost pro GUI.

    Pro protokol se používá originální soubor, zde řešíme pouze vzhled v aplikaci.
    """

    try:
        img = tk.PhotoImage(file=cesta)
    except Exception:
        # Když se logo nepodaří načíst, vrátíme prázdný obrázek 1x1
        return tk.PhotoImage(width=1, height=1)

    w = img.width()
    h = img.height()

    if w <= GUI_LOGO_MAX_WIDTH and h <= GUI_LOGO_MAX_HEIGHT:
        return img

    scale = max(w / GUI_LOGO_MAX_WIDTH, h / GUI_LOGO_MAX_HEIGHT)
    faktor = max(1, int(math.ceil(scale)))

    # subsample zmenšuje obrázek celočíselným faktorem
    zmensene = img.subsample(faktor, faktor)
    return zmensene


# Logo v GUI (zmenšené na max. velikost)
logo = _nacist_logo_do_gui(PROTOCOL_LOGO_PATH)


def zmenit_logo():
    """Otevře dialog pro výběr souboru s logem a aktualizuje logo v aplikaci i v protokolu.

    Očekává se obrázek (např. PNG). Pokud se obrázek nepodaří načíst, zobrazí chybové okno.
    """

    global PROTOCOL_LOGO_PATH, logo, logo_label

    soubor = fd.askopenfilename(
        parent=window,
        title="Vyberte obrázek loga",
        filetypes=(
            ("Obrázky PNG", "*.png"),
            ("Obrázky GIF", "*.gif"),
            ("Všechny soubory", "*.*"),
        ),
    )

    if not soubor:
        return

    try:
        nove_logo = _nacist_logo_do_gui(soubor)
    except Exception as e:
        mb.showerror("Chyba načtení loga", f"Obrázek se nepodařilo načíst.\n\n{e}")
        return

    # Aktualizace cesty pro protokol / grafy
    PROTOCOL_LOGO_PATH = soubor

    # Aktualizace loga v GUI
    logo = nove_logo
    if "logo_label" in globals():
        logo_label.configure(image=logo)


def obnovit_vychozi_logo():
    """Vrátí logo zpět na výchozí obrázek.

    Použije DEFAULT_PROTOCOL_LOGO_PATH a aktualizuje jak GUI, tak protokol.
    """

    global PROTOCOL_LOGO_PATH, logo, logo_label

    PROTOCOL_LOGO_PATH = DEFAULT_PROTOCOL_LOGO_PATH

    try:
        nove_logo = _nacist_logo_do_gui(PROTOCOL_LOGO_PATH)
    except Exception as e:
        mb.showerror("Chyba načtení výchozího loga", f"Výchozí logo se nepodařilo načíst.\n\n{e}")
        return

    logo = nove_logo
    if "logo_label" in globals():
        logo_label.configure(image=logo)


def vytvor_protokol_figure(
    hodnoty,
    prumer,
    roz_nej_u,
    nominal,
    spod_mez,
    horni_mez,
    cislo_protokolu,
    operator_mereni,
    pouzite_meridlo,
    nazev,
    matcislo,
    poznamka_proto,
    x_indexy,
):
    """Vytvoří a vrátí Figure ve formátu A4 s hlavičkou, textovými položkami a grafem.

    Funkce se používá jak pro zobrazení v okně, tak pro export do PDF.
    """

    # A4 na výšku (~8.27 x 11.69 palců)
    A4_WIDTH_INCH = 8.27
    A4_HEIGHT_INCH = 11.69
    fig = Figure(figsize=(A4_WIDTH_INCH, A4_HEIGHT_INCH), dpi=100)

    # Tři oblasti: hlavička (logo + nadpis + číslo protokolu), textové položky, graf
    header_ax = fig.add_axes([0.05, 0.80, 0.90, 0.18])
    text_ax = fig.add_axes([0.05, 0.42, 0.90, 0.34])
    ax = fig.add_axes([0.10, 0.07, 0.82, 0.30])

    header_ax.axis("off")
    text_ax.axis("off")

    # Výchozí texty, pokud uživatel nic nezadal (použito i v hlavičce)
    cislo_protokolu_fmt = cislo_protokolu if cislo_protokolu else "—"

    # Hlavička protokolu: logo uprostřed, pod ním nadpis a číslo protokolu
    header_ax.set_xlim(0, 1)
    header_ax.set_ylim(0, 1)

    if os.path.exists(PROTOCOL_LOGO_PATH):
        try:
            logo_img = mpimg.imread(PROTOCOL_LOGO_PATH)
            # Zachování poměru stran loga, mírně větší výška pro lepší čitelnost
            logo_height = 0.40
            logo_width = logo_height * (logo_img.shape[1] / logo_img.shape[0])
            logo_x_min = 0.5 - logo_width / 2
            logo_x_max = 0.5 + logo_width / 2
            logo_y_min = 0.62
            logo_y_max = logo_y_min + logo_height
            header_ax.imshow(
                logo_img,
                extent=[logo_x_min, logo_x_max, logo_y_min, logo_y_max],
                aspect="equal",
            )
        except Exception:
            # Pokud se logo nepodaří načíst, hlavička bude jen textová
            pass

    # Nadpis protokolu a číslo protokolu, obojí centrované
    header_ax.text(
        0.5,
        0.40,
        "PROTOKOL O MĚŘENÍ – posuvné měřítko",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
    )
    header_ax.text(
        0.5,
        0.18,
        f"Číslo protokolu: {cislo_protokolu_fmt}",
        ha="center",
        va="center",
        fontsize=12,
    )

    # Plné čáry: nominální hodnota a tolerance (graf dole na stránce)
    ax.axhline(nominal, color="tab:green", linestyle="-", label="Nominální hodnota")
    ax.axhline(spod_mez, color="tab:gray", linestyle="-", label="Spodní tolerance")
    ax.axhline(horni_mez, color="tab:gray", linestyle="-", label="Horní tolerance")

    # Pruhovaná čára = průměr
    ax.axhline(prumer, color="tab:blue", linestyle="--", label="Průměr")

    # Body měření s errorbary ± rozšířená nejistota
    ax.errorbar(
        x_indexy,
        hodnoty,
        yerr=[roz_nej_u] * len(hodnoty),
        fmt="o",
        color="tab:red",
        ecolor="gray",
        elinewidth=1,
        capsize=4,
        label="Hodnoty ± U",
    )

    # Nastavení osy Y tak, aby byl prostor i pro hodnoty mimo tolerance
    vsechny_y = hodnoty + [nominal, spod_mez, horni_mez]
    y_min = min(vsechny_y)
    y_max = max(vsechny_y)
    rozsah = y_max - y_min if y_max != y_min else max(1.0, abs(y_max))
    mezera = 0.2 * rozsah
    ax.set_ylim(y_min - mezera, y_max + mezera)

    ax.set_xlabel("Pořadí měření")
    ax.set_ylabel("Hodnota [mm]")
    ax.set_title("Naměřené hodnoty, průměr, nominál a tolerance")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="best")

    # Text s informacemi a hodnotami NAD grafem (textové položky jako první)
    # Naformátování hodnot: max. 4 desetinná místa bez zbytečných koncových nul
    formatted_hodnoty = []
    for h in hodnoty:
        s = f"{h:.4f}".rstrip("0").rstrip(".")
        formatted_hodnoty.append(s)

    # Rozdělení hodnot do více řádků, aby se text vešel na A4
    hodnoty_radky = []
    hodnot_na_radek = 15  # počet hodnot na jeden řádek (dle potřeby lze změnit)
    for i in range(0, len(formatted_hodnoty), hodnot_na_radek):
        radek = ", ".join(formatted_hodnoty[i : i + hodnot_na_radek])
        hodnoty_radky.append(radek)

    datum_mereni = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Vyhodnocení shody s tolerancemi včetně nejistoty
    dolni_hranice_s_U = prumer - roz_nej_u
    horni_hranice_s_U = prumer + roz_nej_u

    if horni_hranice_s_U <= horni_mez and dolni_hranice_s_U >= spod_mez:
        vyhodnoceni_text = "VYHOVUJE (interval měření včetně nejistoty je celý v toleranci)."
    elif dolni_hranice_s_U > horni_mez or horni_hranice_s_U < spod_mez:
        vyhodnoceni_text = "NEVYHOVUJE (interval měření včetně nejistoty leží mimo tolerance)."
    else:
        vyhodnoceni_text = (
            "NELZE JEDNOZNAČNĚ POSOUDIT\n (interval měření včetně nejistoty překrývá hraniční hodnoty)."
        )

    # Výchozí texty, pokud uživatel nic nezadal
    operator_fmt = operator_mereni if operator_mereni else "—"
    meridlo_fmt = pouzite_meridlo if pouzite_meridlo else "Posuvné měřítko"

    info_text_lines = [
        "PROTOKOL O MĚŘENÍ – Výsledné údaje",
        f"Číslo protokolu: {cislo_protokolu_fmt}",
        f"Datum a čas měření: {datum_mereni}",
        f"Operátor měření: {operator_fmt}",
        f"Použité měřidlo: {meridlo_fmt}",
        "",
        "Informace o předmětu měření:",
        f"  Název dílu: {nazev if nazev else '—'}",
        f"  Materiálové číslo: {matcislo if matcislo else '—'}",
        f"  Nominální hodnota: {nominal:.4f} mm",
        f"  Spodní tolerance: {spod_mez:.4f} mm",
        f"  Horní tolerance: {horni_mez:.4f} mm",
        "",
        "Shrnutí výsledku:",
        f"  Průměrná hodnota: {prumer:.4f} mm",
        f"  Rozšířená nejistota U (k = 2): {roz_nej_u:.4f} mm",
        "  Uvedená nejistota odpovídá přibližně 95% hladině spolehlivosti.",
        f"  Vyhodnocení shody s tolerancí: {vyhodnoceni_text}",
        "",
        "Naměřené hodnoty [mm]:",
    ]

    for radek in hodnoty_radky:
        info_text_lines.append(f"  {radek}")

    if poznamka_proto:
        info_text_lines.extend([
            "",
            f"Poznámka: {poznamka_proto}",
        ])

    info_text = "\n".join(info_text_lines)
    text_ax.set_xlim(0, 1)
    text_ax.set_ylim(0, 1)
    text_ax.text(0.0, 1.0, info_text, fontsize=9, va="top", ha="left", linespacing=1.3)

    return fig, ax, text_ax



# Funkce

def add_text():
    vystraha.configure(text="")
    if input_entry_1.get() == "":
        vystraha.configure(text="Zadal jste prázdnou hodnotu.")
    else:
        carka = input_entry_1.get()
        if carka.__contains__(","):
            oprava = carka.replace(",", ".")
            list_box.insert(tk.END, oprava)
            input_entry_1.delete(0, tk.END)
        else:
            list_box.insert(tk.END, input_entry_1.get())
            input_entry_1.delete(0, tk.END)


def add_text_enter(event):
    """Obsluha klávesy Enter – znovupoužije logiku add_text()."""
    add_text()


def remove_text_item():
    # Odstraní položku seznamu
    list_box.delete(tk.ANCHOR)
    pocet_zadanych_hodnot.configure(text="")

def remove_all_text_item():
    # Odstraní položku seznamu
    list_box.delete(0, tk.END)
    pocet_zadanych_hodnot.configure(text="")


def vypocitej():
    """Výpočet nejistoty měření z hodnot v seznamu a zadaného rozlišení."""

    # reset základního stavu
    vystraha.configure(text="")
    rozliseni_meridla.configure(text_color=default_rozliseni_meridla_color)

    # Načtení hodnot ze seznamu
    seznam_text = list_box.get(0, tk.END)
    if len(seznam_text) < 2:
        vystraha.configure(text="Zadej minimálně dvě hodnoty.")
        rozliseni_meridla.configure(text_color="#8B0013")
        vysledek_mereni_label_1.configure(text="")
        return

    try:
        seznam_vstupu = [float(x) for x in seznam_text]
    except ValueError:
        vystraha.configure(text="Některá zadaná hodnota není číslo.")
        return

    # Výpočet součtu a průměru
    soucet = sum(seznam_vstupu)
    prumer = soucet / len(seznam_vstupu)

    # Vytvoření další proměnné pro cyklus, kterým sečteme umocněné rozdíly proměnných a průměru
    soucet_2 = 0
    for x in seznam_vstupu:
        soucet_2 = pow(x - prumer, 2) + soucet_2

    # Konečný výpočet nejistoty A
    sumax = soucet_2 / (len(seznam_vstupu) * (len(seznam_vstupu) - 1))
    nej_a = round(math.sqrt(sumax), 3)
    nejistota_a_label_2.configure(text=str(nej_a))

    # Deklarace proměnné rozlišení měřidla a výpočet chyby pro další postup
    carka = input_rozliseni_entry.get().strip()
    if not carka:
        vystraha.configure(text="Zadej rozlišení měřidla.")
        rozliseni_meridla.configure(text_color="#8B0013")
        return

    if "," in carka:
        carka = carka.replace(",", ".")

    try:
        rozliseni = float(carka)
    except ValueError:
        vystraha.configure(text="Rozlišení měřidla musí být číslo.")
        rozliseni_meridla.configure(text_color="#8B0013")
        return

    chyba_odectu = rozliseni / 2
    chyba_odectu_label.configure(text=str(chyba_odectu))

    # Deklarace abbeho chyby
    abbe = 0.033
    abbeho_chyba_label.configure(text=str(abbe))
    abbe_check = checkbutton_abbe_value.get()

    # Deklarace teplotního vlivu
    teplota = round(11.5 * 0.000001 * prumer / pow(3, 1 / 3), 5)
    vliv_teploty_label.configure(text=str(teplota))
    teplota_check = checkbutton_teplota_value.get()

    # Deklarace a výpočet nejistoty B
    if not abbe_check:
        abbe = 0
    if not teplota_check:
        teplota = 0

    nej_b = math.sqrt(pow(abbe, 2) + pow(teplota, 2) + pow(chyba_odectu, 2))

    # Deklarace kombinované nejistoty
    komb_nej = round(math.sqrt(pow(nej_a, 2) + pow(nej_b, 2)), 3)
    kombinovana_nejistota_label.configure(text=str(komb_nej))

    # Deklarace a výpočet rozšířené nejistoty
    roz_nej_u = komb_nej * 2
    rozsirena_nejistota_label.configure(text=str(roz_nej_u))

    # Výpis výsledku
    prumer_pro_vysledek = round(prumer, 2)
    roz_nej_u_vysledek = round(roz_nej_u, 2)
    vysledek_mereni_label_1.configure(text=f"{prumer_pro_vysledek} ± {roz_nej_u_vysledek} mm")
    pocet_zadanych_hodnot.configure(text=str(len(seznam_vstupu)))

    # Ulož aktuální statistiky pro případné použití v grafu
    global posledni_prumer, posledni_rozsirena_nejistota
    posledni_prumer = prumer
    posledni_rozsirena_nejistota = roz_nej_u


def zobraz_graf():
    """Zobrazí nové okno s grafem hodnot, průměrem a bias + nejistota jako errorbar."""

    # Znovu použijeme stejné kontroly jako ve vypocitej()
    seznam_text = list_box.get(0, tk.END)
    if len(seznam_text) < 2:
        vystraha.configure(text="Pro graf zadej minimálně dvě hodnoty.")
        return

    try:
        hodnoty = [float(x) for x in seznam_text]
    except ValueError:
        vystraha.configure(text="Některá zadaná hodnota není číslo.")
        return

    # Spočítáme průměr a rozšířenou nejistotu stejně jako ve vypocitej()
    soucet = sum(hodnoty)
    prumer = soucet / len(hodnoty)

    soucet_2 = 0
    for x in hodnoty:
        soucet_2 = pow(x - prumer, 2) + soucet_2

    sumax = soucet_2 / (len(hodnoty) * (len(hodnoty) - 1))
    nej_a = math.sqrt(sumax)

    # Rozlišení
    carka = input_rozliseni_entry.get().strip()
    if not carka:
        vystraha.configure(text="Pro graf zadej také rozlišení měřidla.")
        return
    if "," in carka:
        carka = carka.replace(",", ".")
    try:
        rozliseni = float(carka)
    except ValueError:
        vystraha.configure(text="Rozlišení měřidla musí být číslo.")
        return

    chyba_odectu = rozliseni / 2

    # Abbeho chyba a vliv teploty podle zaškrtávacích tlačítek
    abbe = 0.033
    teplota = round(11.5 * 0.000001 * prumer / pow(3, 1 / 3), 5)

    if not checkbutton_abbe_value.get():
        abbe = 0
    if not checkbutton_teplota_value.get():
        teplota = 0

    nej_b = math.sqrt(pow(abbe, 2) + pow(teplota, 2) + pow(chyba_odectu, 2))
    komb_nej = math.sqrt(pow(nej_a, 2) + pow(nej_b, 2))
    roz_nej_u = komb_nej * 2

    # Nominální hodnota a tolerance pro zobrazení v grafu
    nazev = info_nazev_entry.get().strip()
    matcislo = info_mat_entry.get().strip()

    # Další informace pro protokol
    cislo_protokolu = info_protokol_entry.get().strip()
    operator_mereni = info_operator_entry.get().strip()
    pouzite_meridlo = info_meridlo_entry.get().strip()
    poznamka_proto = info_poznamka_entry.get().strip()

    nom_text = info_nom_entry.get().strip()
    tol_spod_text = info_tol_spod_entry.get().strip()
    tol_horn_text = info_tol_horn_entry.get().strip()

    try:
        if "," in nom_text:
            nom_text = nom_text.replace(",", ".")
        if "," in tol_spod_text:
            tol_spod_text = tol_spod_text.replace(",", ".")
        if "," in tol_horn_text:
            tol_horn_text = tol_horn_text.replace(",", ".")

        nominal = float(nom_text) if nom_text else prumer
        spod_mez = float(tol_spod_text) if tol_spod_text else nominal
        horni_mez = float(tol_horn_text) if tol_horn_text else nominal
    except ValueError:
        vystraha.configure(text="Nominál a tolerance musí být čísla.")
        return

    # Připravíme data pro graf
    x_indexy = list(range(1, len(hodnoty) + 1))

    # Vytvoříme a naplníme objekt Figure s protokolem (A4 stránka)
    fig, ax, text_ax = vytvor_protokol_figure(
        hodnoty=hodnoty,
        prumer=prumer,
        roz_nej_u=roz_nej_u,
        nominal=nominal,
        spod_mez=spod_mez,
        horni_mez=horni_mez,
        cislo_protokolu=cislo_protokolu,
        operator_mereni=operator_mereni,
        pouzite_meridlo=pouzite_meridlo,
        nazev=nazev,
        matcislo=matcislo,
        poznamka_proto=poznamka_proto,
        x_indexy=x_indexy,
    )

    # Vytvoříme nové okno pro graf, nad hlavním oknem
    okno_graf = ctk.CTkToplevel(window)
    okno_graf.title("Graf naměřených hodnot a nejistoty")
    okno_graf.geometry("800x500")
    okno_graf.transient(window)
    okno_graf.lift()
    okno_graf.attributes("-topmost", True)
    okno_graf.after(100, lambda: okno_graf.attributes("-topmost", False))

    # Vyhodnocení shody s tolerancemi včetně nejistoty
    dolni_hranice_s_U = prumer - roz_nej_u
    horni_hranice_s_U = prumer + roz_nej_u

    if horni_hranice_s_U <= horni_mez and dolni_hranice_s_U >= spod_mez:
        vyhodnoceni_text = "VYHOVUJE (interval měření včetně nejistoty je celý v toleranci)."
    elif dolni_hranice_s_U > horni_mez or horni_hranice_s_U < spod_mez:
        vyhodnoceni_text = "NEVYHOVUJE (interval měření včetně nejistoty leží mimo tolerance)."
    else:
        vyhodnoceni_text = (
            "NELZE JEDNOZNAČNĚ POSOUDIT (interval měření včetně nejistoty překrývá hraniční hodnoty)."
        )

    # Text a další informace už jsou ve fig/text_ax vytvořené funkcí vytvor_protokol_figure

    canvas = FigureCanvasTkAgg(fig, master=okno_graf)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Tlačítko pro export grafu do PDF
    def uloz_pdf():
        soubor = fd.asksaveasfilename(
            parent=okno_graf,
            defaultextension=".pdf",
            filetypes=(("PDF soubory", "*.pdf"), ("Všechny soubory", "*.*")),
            title="Uložit graf jako PDF",
        )
        if soubor:
            fig.savefig(soubor, format="pdf")

    ulozit_button = ctk.CTkButton(okno_graf, text="Uložit protokol do PDF", command=uloz_pdf, width=160)
    ulozit_button.pack(pady=5)


def exportovat_protokol_pdf():
    """Přímý export protokolu do PDF z hlavního okna bez zobrazování grafu.

    Používá stejná data a rozložení jako zobraz_graf().
    """

    # Stejné kontroly jako ve zobraz_graf
    seznam_text = list_box.get(0, tk.END)
    if len(seznam_text) < 2:
        vystraha.configure(text="Pro protokol zadej minimálně dvě hodnoty.")
        return

    try:
        hodnoty = [float(x) for x in seznam_text]
    except ValueError:
        vystraha.configure(text="Některá zadaná hodnota není číslo.")
        return

    soucet = sum(hodnoty)
    prumer = soucet / len(hodnoty)

    soucet_2 = 0
    for x in hodnoty:
        soucet_2 = pow(x - prumer, 2) + soucet_2

    sumax = soucet_2 / (len(hodnoty) * (len(hodnoty) - 1))
    nej_a = math.sqrt(sumax)

    # Rozlišení
    carka = input_rozliseni_entry.get().strip()
    if not carka:
        vystraha.configure(text="Pro protokol zadej také rozlišení měřidla.")
        return
    if "," in carka:
        carka = carka.replace(",", ".")
    try:
        rozliseni = float(carka)
    except ValueError:
        vystraha.configure(text="Rozlišení měřidla musí být číslo.")
        return

    chyba_odectu = rozliseni / 2

    # Abbeho chyba a vliv teploty podle zaškrtávacích tlačítek
    abbe = 0.033
    teplota = round(11.5 * 0.000001 * prumer / pow(3, 1 / 3), 5)

    if not checkbutton_abbe_value.get():
        abbe = 0
    if not checkbutton_teplota_value.get():
        teplota = 0

    nej_b = math.sqrt(pow(abbe, 2) + pow(teplota, 2) + pow(chyba_odectu, 2))
    komb_nej = math.sqrt(pow(nej_a, 2) + pow(nej_b, 2))
    roz_nej_u = komb_nej * 2

    # Nominál a tolerance
    nom_text = info_nom_entry.get().strip()
    tol_spod_text = info_tol_spod_entry.get().strip()
    tol_horn_text = info_tol_horn_entry.get().strip()

    try:
        if "," in nom_text:
            nom_text = nom_text.replace(",", ".")
        if "," in tol_spod_text:
            tol_spod_text = tol_spod_text.replace(",", ".")
        if "," in tol_horn_text:
            tol_horn_text = tol_horn_text.replace(",", ".")

        nominal = float(nom_text) if nom_text else prumer
        spod_mez = float(tol_spod_text) if tol_spod_text else nominal
        horni_mez = float(tol_horn_text) if tol_horn_text else nominal
    except ValueError:
        vystraha.configure(text="Nominál a tolerance musí být čísla.")
        return

    # Další informace pro protokol
    nazev = info_nazev_entry.get().strip()
    matcislo = info_mat_entry.get().strip()
    cislo_protokolu = info_protokol_entry.get().strip()
    operator_mereni = info_operator_entry.get().strip()
    pouzite_meridlo = info_meridlo_entry.get().strip()
    poznamka_proto = info_poznamka_entry.get().strip()

    x_indexy = list(range(1, len(hodnoty) + 1))

    fig, ax, text_ax = vytvor_protokol_figure(
        hodnoty=hodnoty,
        prumer=prumer,
        roz_nej_u=roz_nej_u,
        nominal=nominal,
        spod_mez=spod_mez,
        horni_mez=horni_mez,
        cislo_protokolu=cislo_protokolu,
        operator_mereni=operator_mereni,
        pouzite_meridlo=pouzite_meridlo,
        nazev=nazev,
        matcislo=matcislo,
        poznamka_proto=poznamka_proto,
        x_indexy=x_indexy,
    )

    soubor = fd.asksaveasfilename(
        parent=window,
        defaultextension=".pdf",
        filetypes=(("PDF soubory", "*.pdf"), ("Všechny soubory", "*.*")),
        title="Uložit protokol do PDF",
    )
    if soubor:
        fig.savefig(soubor, format="pdf")

# Hlavní menu
hlavniMenu = tk.Menu(window)

# Vytvořit rozbalovací menu a přidat ho k hlavnímu menu
menuSoubor = tk.Menu(hlavniMenu, tearoff=0, bg=main_color)
menuSoubor.add_command(label="Otevřít")
menuSoubor.add_command(label="Uložit")
menuSoubor.add_separator()
menuSoubor.add_command(label="Změnit logo…", command=zmenit_logo)
menuSoubor.add_command(label="Obnovit výchozí logo", command=obnovit_vychozi_logo)
menuSoubor.add_separator()
menuSoubor.add_command(label="Ukončit", command=window.quit)
hlavniMenu.add_cascade(label="Soubor", menu=menuSoubor)

# Další rozbalovací menu
menuUpravy = tk.Menu(hlavniMenu, tearoff=0, bg=main_color)
menuUpravy.add_command(label="Vyjmout")
menuUpravy.add_command(label="Kopírovat")
menuUpravy.add_command(label="Vložit")
hlavniMenu.add_cascade(label="Upravit", menu=menuUpravy)

menuNapoveda = tk.Menu(hlavniMenu, tearoff=0, bg=main_color)
menuNapoveda.add_command(label="O aplikaci")
hlavniMenu.add_cascade(label="Nápověda", menu=menuNapoveda)

# Menu pro motiv vzhledu
menuMotiv = tk.Menu(hlavniMenu, tearoff=0, bg=main_color)
menuMotiv.add_command(label="Systémový motiv", command=lambda: change_theme("system"))
menuMotiv.add_command(label="Světlý motiv", command=lambda: change_theme("light"))
menuMotiv.add_command(label="Tmavý motiv", command=lambda: change_theme("dark"))
hlavniMenu.add_cascade(label="Motiv", menu=menuMotiv)

window.configure(menu=hlavniMenu)

# Hlavní kontejner pro responzivní rozložení
main_frame = ctk.CTkFrame(window)
main_frame.pack(fill="both", expand=True)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Levý, střední a pravý sloupec
left_frame = ctk.CTkFrame(main_frame, corner_radius=8)
left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

center_frame = ctk.CTkFrame(main_frame, corner_radius=8)
center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

right_frame = ctk.CTkFrame(main_frame, corner_radius=8)
right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

left_frame.grid_rowconfigure(1, weight=1)
center_frame.grid_rowconfigure(0, weight=1)
center_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=0)  # řádek pro logo
right_frame.grid_rowconfigure(1, weight=1)  # formulář
right_frame.grid_rowconfigure(2, weight=1)  # spodní panel

# Definování framů uvnitř kontejnerů
input_frame = ctk.CTkFrame(left_frame, corner_radius=8)
input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 5))

input_frame_label = ctk.CTkLabel(input_frame, text="Naměřené hodnoty", font=second_font)
input_frame_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

listbox_frame = ctk.CTkFrame(left_frame, corner_radius=8)
listbox_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

button_frame = ctk.CTkFrame(left_frame, corner_radius=8)
button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))

text_frame = ctk.CTkFrame(center_frame, corner_radius=8)
text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

text_frame_label = ctk.CTkLabel(text_frame, text="Výpočet nejistoty", font=main_font)
text_frame_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(10, 0), sticky="w")

logo_frame = ctk.CTkFrame(right_frame, corner_radius=8)
logo_frame.grid(row=0, column=0, sticky="new", padx=5, pady=(5, 0))

others_frame = ctk.CTkFrame(right_frame, corner_radius=8)
others_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5, 5))
others_frame.grid_columnconfigure(0, weight=1)
others_frame.grid_columnconfigure(1, weight=1)

count_frame = ctk.CTkFrame(right_frame, corner_radius=8)
count_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))

# Definování prvků programu

# Scrollbar
listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

text_scrollbar = tk.Scrollbar(listbox_frame)
text_scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

list_box = tk.Listbox(listbox_frame, font=main_font, background="#A3A3A3",
                      yscrollcommand=text_scrollbar.set, border=0, highlightbackground="#A3A3A3", highlightthickness=1)
list_box.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

text_scrollbar.config(command=list_box.yview)

# Input_entry_button
add_button = ctk.CTkButton(button_frame, text="Zadej", command=add_text, width=60, height=24,
                           font=second_font)
add_button.grid(row=0, column=0, padx=5, pady=(10, 5))

# Delete button
remove_button = ctk.CTkButton(button_frame, text="Odstranit", command=remove_text_item, width=60, height=24,
                              font=second_font)
remove_button.grid(row=0, column=1, padx=5, pady=(10, 5))

# Delete_all button
delete_all_button = ctk.CTkButton(button_frame, text="Odstraň vše", command=remove_all_text_item, width=120,
                                  height=24, font=second_font)
delete_all_button.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 10))

# Vstup naměřených hodnot
input_label_text = ctk.CTkLabel(input_frame, text="Zadej hodnoty", font=second_font)
input_label_text.grid(row=1, column=0, padx=5, pady=(5, 0))

input_entry_1 = ctk.CTkEntry(input_frame, width=110, font=second_font, justify="center")
input_entry_1.grid(row=2, column=0, padx=5, pady=5)
input_entry_1.bind("<Return>", add_text_enter)

# Vstup rozlišení měřidla
rozliseni_meridla = ctk.CTkLabel(text_frame, text="Zadej rozlišení měřidla", font=main_font)
rozliseni_meridla.grid(row=1, column=0, padx=5, pady=20, sticky="w")
default_rozliseni_meridla_color = rozliseni_meridla.cget("text_color")

input_rozliseni_entry = ctk.CTkEntry(text_frame, width=120, justify="center")
input_rozliseni_entry.grid(row=1, column=1, padx=5, pady=20, sticky="w")

# Výpočet nejistoty A - Label (text a výsledek)

nejistota_a_label = ctk.CTkLabel(text_frame, text="Nejistota typu A", font=second_font)
nejistota_a_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")

nejistota_a_label_2 = ctk.CTkLabel(text_frame, width=80, font=second_font, text="")
nejistota_a_label_2.grid(row=2, column=1, padx=5, pady=10, sticky="w")

# Složky nejistoty tybu B
nejistota_b_label = ctk.CTkLabel(text_frame, text="Složky nejistoty typu B", font=main_font)
nejistota_b_label.grid(row=3, column=0, padx=5, pady=10, sticky="w")

# Abbeho chyba
abbeho_chyba = ctk.CTkLabel(text_frame, text="Abbeho chyba", font=second_font)
abbeho_chyba.grid(row=4, column=0, padx=5, pady=10, sticky="w")

abbeho_chyba_label = ctk.CTkLabel(text_frame, width=80, font=second_font, text="")
abbeho_chyba_label.grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Vliv teploty
vliv_teploty = ctk.CTkLabel(text_frame, text="Vliv teploty 21 ± 1 °C", font=second_font)
vliv_teploty.grid(row=5, column=0, padx=5, pady=10, sticky="w")

vliv_teploty_label = ctk.CTkLabel(text_frame, width=80, font=second_font, text="")
vliv_teploty_label.grid(row=5, column=1, padx=5, pady=10, sticky="w")

# Chyba odečtu
chyba_odectu_text = ctk.CTkLabel(text_frame, text="Chyba odečtu", font=second_font)
chyba_odectu_text.grid(row=6, column=0, padx=5, pady=10, sticky="w")

chyba_odectu_label = ctk.CTkLabel(text_frame, width=80, font=second_font, text="")
chyba_odectu_label.grid(row=6, column=1, padx=5, pady=10, sticky="w")

# Kombinovaná nejistota A/B
kombinovana_nejistota = ctk.CTkLabel(text_frame, text="Kombinovaná nejistota A/B", font=second_font)
kombinovana_nejistota.grid(row=7, column=0, padx=5, pady=10, sticky="w")

kombinovana_nejistota_label = ctk.CTkLabel(text_frame, width=80, font=second_font, text="")
kombinovana_nejistota_label.grid(row=7, column=1, padx=5, pady=10, sticky="w")

# Rozšířená nejistota U
rozsirena_nejistota = ctk.CTkLabel(text_frame, text="Rozšířená nejistota U", font=main_font)
rozsirena_nejistota.grid(row=8, column=0, padx=5, pady=10, sticky="w")

rozsirena_nejistota_label = ctk.CTkLabel(text_frame, text="", width=80, font=second_font)
rozsirena_nejistota_label.grid(row=8, column=1, padx=5, pady=10, sticky="w")

# Výsledek měření
vysledek_mereni = ctk.CTkLabel(text_frame, text="Výsledek měření", font=main_font, text_color="#8B0013",
                               justify="center")
vysledek_mereni.grid(row=7, column=2, padx=5, pady=5)

vysledek_mereni_label_1 = ctk.CTkLabel(text_frame, width=160, height=40, font=second_font, text="",
                                       text_color="#8B0013")
vysledek_mereni_label_1.grid(row=8, column=2, padx=15)
# Logo (v samostatném horním frame, aby neroztahovalo sloupce formuláře)
logo_label = ctk.CTkLabel(logo_frame, width=GUI_LOGO_MAX_WIDTH, height=GUI_LOGO_MAX_HEIGHT, image=logo, text="")
logo_label.grid(row=0, column=0, padx=20, pady=5, sticky="n")

# Počet zadaných hodnot
pocet_zadanych = ctk.CTkLabel(others_frame, text="Počet zadaných hodnot", font=second_font,
                              text_color="#8B0013")
pocet_zadanych.grid(row=0, column=0, pady=10)
pocet_zadanych_hodnot = ctk.CTkLabel(others_frame, text="", text_color="#8B0013", font=("Helvetica", 20))
pocet_zadanych_hodnot.grid(row=1, column=0)

# Štítek výstrahy
vystraha = ctk.CTkLabel(others_frame, text="", text_color="#8B0013", font=second_font, wraplength=150)
vystraha.grid(row=2, column=0, pady=5)

# Informace o měřeném předmětu (levý sloupec)
info_nazev_label = ctk.CTkLabel(others_frame, text="Název dílu", font=second_font)
info_nazev_label.grid(row=4, column=0, padx=5, pady=(10, 0), sticky="w")
info_nazev_entry = ctk.CTkEntry(others_frame, width=160)
info_nazev_entry.grid(row=5, column=0, padx=5, pady=(0, 5), sticky="ew")

info_mat_label = ctk.CTkLabel(others_frame, text="Materiálové číslo", font=second_font)
info_mat_label.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="w")
info_mat_entry = ctk.CTkEntry(others_frame, width=160)
info_mat_entry.grid(row=7, column=0, padx=5, pady=(0, 5), sticky="ew")

info_nom_label = ctk.CTkLabel(others_frame, text="Nominální hodnota [mm]", font=second_font)
info_nom_label.grid(row=8, column=0, padx=5, pady=(5, 0), sticky="w")
info_nom_entry = ctk.CTkEntry(others_frame, width=160)
info_nom_entry.grid(row=9, column=0, padx=5, pady=(0, 5), sticky="ew")

info_tol_spod_label = ctk.CTkLabel(others_frame, text="Spodní tolerance [mm]", font=second_font)
info_tol_spod_label.grid(row=10, column=0, padx=5, pady=(5, 0), sticky="w")
info_tol_spod_entry = ctk.CTkEntry(others_frame, width=160)
info_tol_spod_entry.grid(row=11, column=0, padx=5, pady=(0, 5), sticky="ew")

info_tol_horn_label = ctk.CTkLabel(others_frame, text="Horní tolerance [mm]", font=second_font)
info_tol_horn_label.grid(row=12, column=0, padx=5, pady=(5, 0), sticky="w")
info_tol_horn_entry = ctk.CTkEntry(others_frame, width=160)
info_tol_horn_entry.grid(row=13, column=0, padx=5, pady=(0, 5), sticky="ew")

# Údaje pro protokol o měření (pravý sloupec)
info_protokol_label = ctk.CTkLabel(others_frame, text="Číslo protokolu", font=second_font)
info_protokol_label.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="w")
info_protokol_entry = ctk.CTkEntry(others_frame, width=160)
info_protokol_entry.grid(row=5, column=1, padx=5, pady=(0, 5), sticky="ew")

info_operator_label = ctk.CTkLabel(others_frame, text="Operátor měření", font=second_font)
info_operator_label.grid(row=6, column=1, padx=5, pady=(5, 0), sticky="w")
info_operator_entry = ctk.CTkEntry(others_frame, width=160)
info_operator_entry.grid(row=7, column=1, padx=5, pady=(0, 5), sticky="ew")

info_meridlo_label = ctk.CTkLabel(others_frame, text="Použité měřidlo", font=second_font)
info_meridlo_label.grid(row=8, column=1, padx=5, pady=(5, 0), sticky="w")
info_meridlo_entry = ctk.CTkEntry(others_frame, width=160)
info_meridlo_entry.grid(row=9, column=1, padx=5, pady=(0, 5), sticky="ew")

info_poznamka_label = ctk.CTkLabel(others_frame, text="Poznámka / akreditace", font=second_font)
info_poznamka_label.grid(row=10, column=1, padx=5, pady=(5, 0), sticky="w")
info_poznamka_entry = ctk.CTkEntry(others_frame, width=160)
info_poznamka_entry.grid(row=11, column=1, padx=5, pady=(0, 5), sticky="ew")

# Tlačítka ve spodním panelu
button = ctk.CTkButton(count_frame, text="Vypočítej", command=vypocitej, width=120)
button.grid(row=4, column=0, pady=(20, 5))

graf_button = ctk.CTkButton(count_frame, text="Graf", command=zobraz_graf, width=120)
graf_button.grid(row=5, column=0, pady=(0, 5))

export_pdf_button = ctk.CTkButton(count_frame, text="Protokol PDF", command=exportovat_protokol_pdf, width=120)
export_pdf_button.grid(row=6, column=0, pady=(0, 10))

# Zaškrtávací tlačítko

checkbutton_abbe_value = tk.BooleanVar(value=True)
checkbutton_abbe = ctk.CTkCheckBox(text_frame, text="Zahrnout\ndo výpočtu",
                                   variable=checkbutton_abbe_value, onvalue=True, offvalue=False)
checkbutton_abbe.grid(row=4, column=2, padx=5, pady=5)


checkbutton_teplota_value = tk.BooleanVar(value=True)
checkbutton_teplota = ctk.CTkCheckBox(text_frame, text="Zahrnout\ndo výpočtu",
                                      variable=checkbutton_teplota_value, onvalue=True, offvalue=False)
checkbutton_teplota.grid(row=5, column=2, padx=5, pady=5)

# Štítek s právy
prava = ctk.CTkLabel(count_frame, text="Copyright © 2024-2026 Sumixon", font=("Helvetica", 9))
prava.grid(row=7, column=0, padx=25)

# Zmáčknutí entru pro vložení hodnoty jen v poli vstupu
window.mainloop()

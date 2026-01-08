import math
import tkinter as tk
import customtkinter as ctk


# Definování stylů
main_color = "grey"
main_font = ("Helvetica", 16)
second_font = ("Helvetica", 14)

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
width = 900
height = 550
window.geometry(f"{width}x{height}")
window.minsize(width, height)
window.resizable(True, True)
window.title("Výpočet nejistoty měření posuvné měřítko")


# Logo
logo = tk.PhotoImage(file="img/sumixon130x50_black.png")



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

# Hlavní menu
hlavniMenu = tk.Menu(window)

# Vytvořit rozbalovací menu a přidat ho k hlavnímu menu
menuSoubor = tk.Menu(hlavniMenu, tearoff=0, bg=main_color)
menuSoubor.add_command(label="Otevřít")
menuSoubor.add_command(label="Uložit")
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
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)

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

others_frame = ctk.CTkFrame(right_frame, corner_radius=8)
others_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 5))

count_frame = ctk.CTkFrame(right_frame, corner_radius=8)
count_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

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

nejistota_a_label_2 = ctk.CTkLabel(text_frame, width=80, font=second_font)
nejistota_a_label_2.grid(row=2, column=1, padx=5, pady=10, sticky="w")

# Složky nejistoty tybu B
nejistota_b_label = ctk.CTkLabel(text_frame, text="Složky nejistoty typu B", font=main_font)
nejistota_b_label.grid(row=3, column=0, padx=5, pady=10, sticky="w")

# Abbeho chyba
abbeho_chyba = ctk.CTkLabel(text_frame, text="Abbeho chyba", font=second_font)
abbeho_chyba.grid(row=4, column=0, padx=5, pady=10, sticky="w")

abbeho_chyba_label = ctk.CTkLabel(text_frame, width=80, font=second_font)
abbeho_chyba_label.grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Vliv teploty
vliv_teploty = ctk.CTkLabel(text_frame, text="Vliv teploty 21 ± 1 °C", font=second_font)
vliv_teploty.grid(row=5, column=0, padx=5, pady=10, sticky="w")

vliv_teploty_label = ctk.CTkLabel(text_frame, width=80, font=second_font)
vliv_teploty_label.grid(row=5, column=1, padx=5, pady=10, sticky="w")

# Chyba odečtu
chyba_odectu_text = ctk.CTkLabel(text_frame, text="Chyba odečtu", font=second_font)
chyba_odectu_text.grid(row=6, column=0, padx=5, pady=10, sticky="w")

chyba_odectu_label = ctk.CTkLabel(text_frame, width=80, font=second_font)
chyba_odectu_label.grid(row=6, column=1, padx=5, pady=10, sticky="w")

# Kombinovaná nejistota A/B
kombinovana_nejistota = ctk.CTkLabel(text_frame, text="Kombinovaná nejistota A/B", font=second_font)
kombinovana_nejistota.grid(row=7, column=0, padx=5, pady=10, sticky="w")

kombinovana_nejistota_label = ctk.CTkLabel(text_frame, width=80, font=second_font)
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

vysledek_mereni_label_1 = ctk.CTkLabel(text_frame, width=160, height=40, font=second_font,
                                       text_color="#8B0013")
vysledek_mereni_label_1.grid(row=8, column=2, padx=15)
# Logo
logo_label = ctk.CTkLabel(others_frame, width=130, height=50, image=logo, text="")
logo_label.grid(row=0, column=0, padx=20, pady=0)

# Počet zadaných hodnot
pocet_zadanych = ctk.CTkLabel(others_frame, text="Počet zadaných hodnot", font=second_font,
                              text_color="#8B0013")
pocet_zadanych.grid(row=1, column=0, pady=10)
pocet_zadanych_hodnot = ctk.CTkLabel(others_frame, text="", text_color="#8B0013", font=("Helvetica", 20))
pocet_zadanych_hodnot.grid(row=2, column=0)

# Štítek výstrahy
vystraha = ctk.CTkLabel(others_frame, text="", text_color="#8B0013", font=second_font, wraplength=150)
vystraha.grid(row=3, column=0, pady=5)

# Tlačítko
button = ctk.CTkButton(count_frame, text="Vypočítej", command=vypocitej, width=120)
button.grid(row=4, column=0, pady=35)

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
prava = ctk.CTkLabel(count_frame, text="Copyright © 2024 Sumixon", font=("Helvetica", 9))
prava.grid(row=5, column=0, padx=25)

# Zmáčknutí entru pro vložení hodnoty jen v poli vstupu
window.mainloop()

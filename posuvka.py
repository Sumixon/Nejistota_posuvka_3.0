from tkinter import *
import math

# Definování stylů
main_color = "grey"
main_font = ("Helvetica", 12)
second_font = ("Helvetica", 10)

#  Okno
window = Tk()
width = 850
height = 450
window.config(width=width, height=height)
window.resizable(False, False)
window.title("Výpočet nejistoty měření posuvné měřítko")
window.config(bg=main_color)

# Logo
logo = PhotoImage(file="img/sumixon130x50_black.png")



# Funkce

def add_text_enter(event):
    vystraha["text"] = ""
    if input_entry_1.get() == "":
        vystraha["text"] = "Zadal jste prázdnou hodnotu."
    else:
        rozliseni_meridla.config(foreground="black")
        carka = input_entry_1.get()
        if carka.__contains__(","):
            oprava = carka.replace(",", ".")
            # Přidání úkolu do textového pole
            list_box.insert(END, oprava)
            input_entry_1.delete(0, END)
        else:
            list_box.insert(END, input_entry_1.get())
            input_entry_1.delete(0, END)


def add_text():
    vystraha["text"] = ""
    if input_entry_1.get() == "":
        vystraha["text"] = "Zadal jste prázdnou hodnotu."
    else:
        carka = input_entry_1.get()
        if carka.__contains__(","):
            oprava = carka.replace(",", ".")
            # Přidání úkolu do textového pole
            list_box.insert(END, oprava)
            input_entry_1.delete(0, END)
        else:
            list_box.insert(END, input_entry_1.get())
            input_entry_1.delete(0, END)


def remove_text_item():
    # Odstraní položku seznamu
    list_box.delete(ANCHOR)
    pocet_zadanych_hodnot["text"] = ""


def vypocitej():
    rozliseni_meridla.config(foreground="black")
    try:
        vystraha["text"] = ""
        seznam_vstupu_flout = list_box.get(0, END)
        seznam_vstupu = []
        for x in seznam_vstupu_flout:
            seznam_vstupu.append(float(x))

        # Výpočet součtu a průměru
        soucet = sum(seznam_vstupu)
        prumer = soucet / len(seznam_vstupu)
        # Vytvoření další proměné pro cyklus, kterým sečteme umocněné rozdíly proměných a průměru
        soucet_2 = 0
        for x in seznam_vstupu:
            soucet_2 = pow(x - prumer, 2) + soucet_2
        # Konečný výpočet nejistoty A
        sumax = soucet_2 / (len(seznam_vstupu) * (len(seznam_vstupu) - 1))
        nej_a = round(math.sqrt(sumax), 3)
        nejistota_a_label_2.config(text=nej_a)

        # Deklarace promněné rozlišení měřidla a výpočet chyby pro další postup
        carka = input_rozliseni_entry.get()
        if carka.__contains__(","):
            oprava = carka.replace(",", ".")
            rozliseni = float(oprava)
        else:
            rozliseni_vypocet = input_rozliseni_entry.get()
            rozliseni = float(rozliseni_vypocet)

        chyba_odectu = rozliseni / 2
        chyba_odectu_label["text"] = chyba_odectu

        # Deklarace abbeho chyby
        abbe = 0.033
        abbeho_chyba_label["text"] = abbe
        abbe_check = checkbutton_abbe_value.get()

        # Zkotroluj vzorec a funkčnost u teploty!
        # Deklarace teplotního vlivu
        teplota = round(11.5 * 0.000001 * prumer / pow(3, 1 / 3), 5)
        vliv_teploty_label["text"] = teplota
        teplota_check = checkbutton_teplota_value.get()

        # Deklarace a výpočet nejistoty B
        if abbe_check:
            abbe = abbe
        else:
            abbe = 0
        if teplota_check:
            teplota = teplota
        else:
            teplota = 0

        nej_b = math.sqrt(pow(abbe, 2) + pow(teplota, 2) + pow(chyba_odectu, 2))

        # Deklarace kombinované nejistoty
        komb_nej = round(math.sqrt(pow(nej_a, 2) + pow(nej_b, 2)), 3)
        kombinovana_nejistota_label["text"] = komb_nej

        # Deklarace a výpočet rozšířené nejistoty
        roz_nej_u = komb_nej * 2
        rozsirena_nejistota_label["text"] = roz_nej_u

        # Výpis výsledku
        prumer_pro_vysledek = round(prumer, 2)
        roz_nej_u_vysledek = round(roz_nej_u, 2)
        vysledek_mereni_label_1["text"] = f"{prumer_pro_vysledek} ± {roz_nej_u_vysledek} mm"
        pocet_zadanych_hodnot["text"] = len(seznam_vstupu)
    except:
        vystraha["text"] = "!!!Zadej rozlišení a minimálně dvě hodnoty!!!"
        rozliseni_meridla.config(foreground="#8B0013")
        vysledek_mereni_label_1["text"] = ""
        abbeho_chyba_label["text"] = ""
        kombinovana_nejistota_label["text"] = ""
        rozsirena_nejistota_label["text"] = ""
        chyba_odectu_label["text"] = ""
        vliv_teploty_label["text"] = ""


# Zmáčknutí entru pro vložení hodnoty
window.bind("<Return>", add_text_enter)

# Hlavní menu
hlavniMenu = Menu(window, background=main_color)

# Vytvořit rozbalovací menu a přidat ho k hlavnímu menu
menuSoubor = Menu(hlavniMenu, tearoff=0, bg=main_color)
menuSoubor.add_command(label="Otevřít")
menuSoubor.add_command(label="Uložit")
menuSoubor.add_separator()
menuSoubor.add_command(label="Ukončit", command=window.quit)
hlavniMenu.add_cascade(label="Soubor", menu=menuSoubor)

# Další rozbalovací menu
menuUpravy = Menu(hlavniMenu, tearoff=0, bg=main_color)
menuUpravy.add_command(label="Vyjmout")
menuUpravy.add_command(label="Kopírovat")
menuUpravy.add_command(label="Vložit")
hlavniMenu.add_cascade(label="Upravit", menu=menuUpravy)

menuNapoveda = Menu(hlavniMenu, tearoff=0, bg=main_color)
menuNapoveda.add_command(label="O aplikaci")
hlavniMenu.add_cascade(label="Nápověda", menu=menuNapoveda)

# Zobrazení menu
window.config(menu=hlavniMenu)

# Definování framů
input_frame = LabelFrame(window, text="Naměřené hodnoty", padx=1, pady=1)
input_frame.config(bg=main_color)
input_frame.place(x=5, y=5, width=140, height=130)

button_frame = LabelFrame(window, text="", padx=1, pady=1)
button_frame.config(bg=main_color)
button_frame.place(x=5, y=400, width=141, height=44)

listbox_frame = LabelFrame(window, text="", padx=1, pady=1)
listbox_frame.config(bg=main_color)
listbox_frame.place(x=5, y=150)

text_frame = LabelFrame(window, text="Výpočet nejistoty", padx=5, pady=5)
text_frame.config(bg="grey")
text_frame.place(x=155, y=5, width=500, height=440)

others_frame = LabelFrame(window, text="***", padx=5, pady=5)
others_frame.config(bg=main_color)
others_frame.place(x=665, y=5, width=180, height=230)

count_frame = LabelFrame(window, text="***", padx=5, pady=5)
count_frame.config(bg=main_color)
count_frame.place(x=665, y=305, width=180, height=140)

# Definování prvků programu

# Scrollbar
text_scrollbar = Scrollbar(listbox_frame)
text_scrollbar.grid(row=0, column=1, sticky=N + S)

# Text frame - obsah - pozor na nastavení yscrollcommand)
list_box = Listbox(listbox_frame, height=12, width=13, font=main_font, background="#A3A3A3",
                   yscrollcommand=text_scrollbar.set, border=0, highlightbackground="#A3A3A3", highlightthickness=1)
list_box.grid(row=0, column=0, sticky=E + N)

# Propojení Scrollbaru s listboxem, aby fungoval posuvník (vymaž závorky, které se tamdávají navíc)
text_scrollbar.config(command=list_box.yview)

# Input_entry_button
add_button = Button(button_frame, text="Zadej", borderwidth=2, font=second_font, bg=main_color, command=add_text)
add_button.grid(row=0, column=0, padx=7, pady=5)

# Delete button
remove_button = Button(button_frame, text="Odstranit", borderwidth=2, font=second_font, bg=main_color,
                       command=remove_text_item)
remove_button.grid(row=0, column=1, padx=5, pady=5, sticky=W)

# Vstup naměřených hodnot
input_label_text = Label(input_frame, text="Zadej hodnoty", font=second_font,
                         bg=main_color, padx=10, pady=10, wraplength=150)
input_label_text.grid(row=0, column=0)

input_entry_1 = Entry(input_frame, width=15, font=second_font, bg=main_color, justify=CENTER)
input_entry_1.grid(row=1, column=0, padx=5, pady=10)

# Vstup rozlišení měřidla
rozliseni_meridla = Label(text_frame, text="Zadej rozlišení měřidla", font=main_font, bg=main_color, padx=10, pady=1)
rozliseni_meridla.grid(row=0, column=0, padx=5, pady=20, sticky=W)

input_rozliseni_entry = Entry(text_frame, width=14, bg=main_color, border=2, justify=CENTER)
input_rozliseni_entry.grid(row=0, column=1, padx=5, pady=20, sticky=W)

# Výpočet nejistoty A - Label (text a výsledek)

nejistota_a_label = Label(text_frame, text="Nejistota typu A", font=second_font, bg=main_color, padx=10, pady=1)
nejistota_a_label.grid(row=1, column=0, padx=5, pady=10, sticky=W)

nejistota_a_label_2 = Label(text_frame, width=10, font=second_font, bg=main_color, highlightbackground="black",
                            highlightthickness=1, justify=CENTER)
nejistota_a_label_2.grid(row=1, column=1, padx=5, pady=10, sticky=W)

# Složky nejistoty tybu B
nejistota_b_label = Label(text_frame, text="Složky nejistoty typu B", font=main_font, bg=main_color, padx=10, pady=1)
nejistota_b_label.grid(row=2, column=0, padx=5, pady=10, sticky=W)

# Abbeho chyba
abbeho_chyba = Label(text_frame, text="Abbeho chyba", font=second_font, bg=main_color, padx=10, pady=1)
abbeho_chyba.grid(row=3, column=0, padx=5, pady=10, sticky=W)

abbeho_chyba_label = Label(text_frame, width=10, font=second_font, bg=main_color,
                           highlightbackground="black", highlightthickness=1)
abbeho_chyba_label.grid(row=3, column=1, padx=5, pady=10, sticky=W)

# Vliv teploty
vliv_teploty = Label(text_frame, text="Vliv teploty 21 ± 1 °C", font=second_font, bg=main_color, padx=10, pady=1)
vliv_teploty.grid(row=4, column=0, padx=5, pady=10, sticky=W)

vliv_teploty_label = Label(text_frame, width=10, font=second_font, bg=main_color,
                           highlightbackground="black", highlightthickness=1)
vliv_teploty_label.grid(row=4, column=1, padx=5, pady=10, sticky=W)

# Chyba odečtu
chyba_odectu_text = Label(text_frame, text="Chyba odečtu", font=second_font, bg=main_color, padx=10, pady=1)
chyba_odectu_text.grid(row=5, column=0, padx=5, pady=10, sticky=W)

chyba_odectu_label = Label(text_frame, width=10, font=second_font, bg=main_color,
                           highlightbackground="black", highlightthickness=1)
chyba_odectu_label.grid(row=5, column=1, padx=5, pady=10, sticky=W)

# Kombinovaná nejistota A/B
kombinovana_nejistota = Label(text_frame, text="Kombinovaná nejistota A/B", font=second_font, bg=main_color, padx=10,
                              pady=1)
kombinovana_nejistota.grid(row=6, column=0, padx=5, pady=10, sticky=W)

kombinovana_nejistota_label = Label(text_frame, width=10, font=second_font, bg=main_color,
                                    highlightbackground="black", highlightthickness=1)
kombinovana_nejistota_label.grid(row=6, column=1, padx=5, pady=10, sticky=W)

# Rozšířená nejistota U
rozsirena_nejistota = Label(text_frame, text="Rozsirena nejistota U", font=main_font, bg=main_color, padx=10, pady=1)
rozsirena_nejistota.grid(row=7, column=0, padx=5, pady=10, sticky=W)

rozsirena_nejistota_label = Label(text_frame, text=0.033, width=10, font=second_font, bg=main_color,
                                  highlightbackground="black", highlightthickness=2)
rozsirena_nejistota_label.grid(row=7, column=1, padx=5, pady=10, sticky=W)

# Výsledek měření
vysledek_mereni = Label(text_frame, text="Výsledek měření", font=main_font, bg=main_color, padx=10, pady=1,
                        foreground="#8B0013", justify=CENTER)
vysledek_mereni.grid(row=6, column=2, padx=5, pady=5)

vysledek_mereni_label_1 = Label(text_frame, width=20, height=2, font=second_font, bg=main_color,
                                highlightbackground="#8B0013", highlightthickness=2, foreground="#8B0013")
vysledek_mereni_label_1.grid(row=7, column=2, padx=15)
# Logo
logo_label = Label(others_frame, width=130, height=50, image=logo, bg=main_color)
logo_label.logo = logo
logo_label.grid(row=0, column=0, padx=20, pady=0)

# Počet zadaných hodnot
pocet_zadanych = Label(others_frame, text="Počet zadaných hodnot", bg=main_color, font=second_font,
                       highlightbackground="#8B0013", highlightthickness=1, foreground="#8B0013")
pocet_zadanych.grid(row=1, column=0, pady=10)
pocet_zadanych_hodnot = Label(others_frame, bg=main_color, foreground="#8B0013", font=("Helvetica,", 20))
pocet_zadanych_hodnot.grid(row=2, column=0)

# Štítek výstrahy
vystraha = Label(others_frame, bg=main_color, foreground="#8B0013", font=second_font, wraplength=150)
vystraha.grid(row=3, column=0, pady=5)

# Tlačítko
button = Button(count_frame, text="Vypočítej", bg=main_color, activebackground=main_color, command=vypocitej)
button.grid(row=4, column=0, pady=35)

# Zaškrtávací tlačítko

checkbutton_abbe_value = BooleanVar(value=True)
checkbutton_abbe = Checkbutton(text_frame, activebackground=main_color, highlightcolor=main_color,
                               highlightbackground=main_color, bg=main_color, text="Zahrnout\ndo výpočtu",
                               variable=checkbutton_abbe_value, state="normal", command="")
checkbutton_abbe.grid(row=3, column=2, padx=5, pady=5)


checkbutton_teplota_value = BooleanVar(value=True)
checkbutton_teplota = Checkbutton(text_frame, activebackground=main_color, highlightcolor=main_color,
                                  highlightbackground=main_color, bg=main_color, text="Zahrnout\ndo výpočtu",
                                  variable=checkbutton_teplota_value, command="")
checkbutton_teplota.grid(row=4, column=2, padx=5, pady=5)

# Štítek s právy
prava = Label(count_frame, text="Copyright © 2024 Sumixon", background=main_color, font=("Helvetica", 7))
prava.grid(row=5, column=0, padx=25)

window.mainloop()

import tkinter as tk
from tkinter import ttk
import random
import math
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# Version du programme
VERSION = "1.6.0"

# Variables globales
TEMPS_RENCONTRE = 14
TEMPS_ALLER_RETOUR_POKECENTRE = 23  # Valeur par défaut
PRIX_MEPO = 840
SHINY_RATES = {
    "standard": 1/30000,
    "donator": 1/27000,
    "donator_charm": 1/24300,
    "donator_link": 1/25650,
    "charm": 1/27000,
    "link": 1/28500
}

def simuler_rencontres(n_rencontres, type_rencontre='solo', restauration='pokecentre', shiny_rate_key="standard", temps_aller_retour=TEMPS_ALLER_RETOUR_POKECENTRE, prix_baie_mepo=PRIX_MEPO):
    shiny_chance = SHINY_RATES[shiny_rate_key]
    shinies_trouves = 0
    rencontres_shiny = []
    utilisations_doux_parfum = 30
    baies_mepo_utilisees = 0
    visites_pokecentre = 0
    temps_total = 0
    
    for i in range(1, n_rencontres + 1):
        if type_rencontre in ['horde3', 'horde5']:
            if utilisations_doux_parfum < 5:
                if restauration == 'pokecentre':
                    utilisations_doux_parfum = 30
                    visites_pokecentre += 1
                    temps_total += temps_aller_retour
                else:
                    baies_necessaires = math.ceil((30 - utilisations_doux_parfum) / 10)
                    baies_mepo_utilisees += baies_necessaires
                    utilisations_doux_parfum += baies_necessaires * 10
            utilisations_doux_parfum -= 5 if type_rencontre == 'horde5' else 3

        temps_total += TEMPS_RENCONTRE

        if type_rencontre == 'solo':
            if random.random() < shiny_chance:
                shinies_trouves += 1
                rencontres_shiny.append((i, temps_total))
        elif type_rencontre == 'horde3':
            for _ in range(3):
                if random.random() < shiny_chance:
                    shinies_trouves += 1
                    rencontres_shiny.append((i, temps_total))
                    break
        elif type_rencontre == 'horde5':
            for _ in range(5):
                if random.random() < shiny_chance:
                    shinies_trouves += 1
                    rencontres_shiny.append((i, temps_total))
                    break
    
    return shinies_trouves, rencontres_shiny, baies_mepo_utilisees, visites_pokecentre, temps_total

def calculer_temps(secondes_totales):
    heures = secondes_totales // 3600
    minutes = (secondes_totales % 3600) // 60
    secondes = secondes_totales % 60
    return heures, minutes, secondes

def afficher_resultats_gui(resultats, text_widget):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, f"Simulation de {resultats['n_rencontres']} rencontres en mode {resultats['type_rencontre']}\n\n")
    text_widget.insert(tk.END, f"Taux de shiny: 1/{int(1/SHINY_RATES[resultats['shiny_rate_key']])}\n")
    text_widget.insert(tk.END, f"Temps total : {resultats['heures']}h {resultats['minutes']}m {resultats['secondes']}s\n")
    text_widget.insert(tk.END, f"Nombre de shinies trouvés : {resultats['shinies_trouves']}\n\n")
    
    if resultats['type_rencontre'] in ['horde3', 'horde5']:
        if resultats['restauration'] == 'baies':
            text_widget.insert(tk.END, f"Nombre de baies Mépo utilisées : {resultats['baies_mepo_utilisees']}\n")
            text_widget.insert(tk.END, f"Prix d'une baie Mépo : {resultats['prix_baie_mepo']} pokéyens\n")
            text_widget.insert(tk.END, f"Coût total des baies Mépo : {resultats['cout_total_baies']} pokéyens\n")
        else:
            text_widget.insert(tk.END, f"Nombre de visites au Pokecentre : {resultats['visites_pokecentre']}\n")
    
    if resultats['shinies_trouves'] > 0:
        text_widget.insert(tk.END, "\nN° de rencontre avec shiny :\n")
        for rencontre, temps in resultats['rencontres_shiny']:
            heures_shiny, minutes_shiny, secondes_shiny = calculer_temps(temps)
            text_widget.insert(tk.END, f"- Rencontre n°{rencontre} (après {heures_shiny}h {minutes_shiny}m {secondes_shiny}s)\n")
    else:
        text_widget.insert(tk.END, "\nAucun shiny n'a été trouvé durant cette simulation.\n")
    text_widget.config(state=tk.DISABLED)

def lancer_simulation():
    try:
        n_rencontres = int(entry_rencontres.get())
        type_rencontre = var_type_rencontre.get()
        restauration = var_methode_restauration.get()
        shiny_rate_key = var_shiny_rate.get()
        temps_aller_retour = int(entry_temps_aller_retour.get())
        prix_baie_mepo = int(entry_prix_baie_mepo.get())
        
        shinies_trouves, rencontres_shiny, baies_mepo_utilisees, visites_pokecentre, temps_total = simuler_rencontres(n_rencontres, type_rencontre, restauration, shiny_rate_key, temps_aller_retour, prix_baie_mepo)
        
        heures, minutes, secondes = calculer_temps(temps_total)
        
        resultats = {
            'n_rencontres': n_rencontres,
            'type_rencontre': type_rencontre,
            'restauration': restauration,
            'shiny_rate_key': shiny_rate_key,
            'shinies_trouves': shinies_trouves,
            'rencontres_shiny': rencontres_shiny,
            'baies_mepo_utilisees': baies_mepo_utilisees,
            'visites_pokecentre': visites_pokecentre,
            'heures': heures,
            'minutes': minutes,
            'secondes': secondes,
            'prix_baie_mepo': prix_baie_mepo,
            'cout_total_baies': baies_mepo_utilisees * prix_baie_mepo,
            'temps_aller_retour': temps_aller_retour
        }
        
        afficher_resultats_gui(resultats, text_resultats)
    except ValueError:
        text_resultats.config(state=tk.NORMAL)
        text_resultats.delete('1.0', tk.END)
        text_resultats.insert(tk.END, "Erreur : Veuillez entrer des nombres valides pour tous les champs numériques.")
        text_resultats.config(state=tk.DISABLED)

# Création de la fenêtre principale avec un thème
root = ThemedTk(theme="arc")
root.title("ShinyHuntSim | SHS")
root.geometry("900x900")

# Définir l'icône de la fenêtre
root.iconbitmap('./assets/icon.ico')

style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
style.configure("TRadiobutton", background="#f0f0f0", font=("Helvetica", 10))
style.configure("TCheckbutton", background="#f0f0f0", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 12, "bold"))

# Création des widgets
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

left_frame = ttk.Frame(main_frame, padding="10")
left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

right_frame = ttk.Frame(main_frame, padding="10")
right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

# Ajout du GIF
gif_label = tk.Label(left_frame)
gif_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

def update_gif(index):
    frame = gif_frames[index]
    index = (index + 1) % len(gif_frames)
    gif_label.configure(image=frame)
    root.after(30, update_gif, index)  # 30ms pour environ 30 FPS

# Chargez votre GIF ici
gif = Image.open("./assets/gif.gif")
gif_frames = []
try:
    while True:
        gif_frames.append(ImageTk.PhotoImage(gif.copy()))
        gif.seek(len(gif_frames))
except EOFError:
    pass

update_gif(0)

ttk.Label(left_frame, text="Nombre de rencontres:").grid(column=0, row=1, sticky=tk.W, pady=5)
entry_rencontres = ttk.Entry(left_frame, width=15)
entry_rencontres.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

ttk.Label(left_frame, text="Type de rencontre:").grid(column=0, row=2, sticky=tk.W, pady=5)
var_type_rencontre = tk.StringVar(value="solo")
ttk.Radiobutton(left_frame, text="Solo", variable=var_type_rencontre, value="solo").grid(column=1, row=2, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Horde 3", variable=var_type_rencontre, value="horde3").grid(column=1, row=3, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Horde 5", variable=var_type_rencontre, value="horde5").grid(column=1, row=4, sticky=tk.W, pady=2)

ttk.Label(left_frame, text="Méthode de restauration:").grid(column=0, row=5, sticky=tk.W, pady=5)
var_methode_restauration = tk.StringVar(value="pokecentre")
ttk.Radiobutton(left_frame, text="Utilisation du Pokecentre", variable=var_methode_restauration, value="pokecentre").grid(column=1, row=5, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Utilisation des baies Mépo", variable=var_methode_restauration, value="baies").grid(column=1, row=6, sticky=tk.W, pady=2)

ttk.Label(left_frame, text="Prix d'une baie Mépo:").grid(column=0, row=7, sticky=tk.W, pady=5)
entry_prix_baie_mepo = ttk.Entry(left_frame, width=15)
entry_prix_baie_mepo.insert(0, PRIX_MEPO)
entry_prix_baie_mepo.grid(column=1, row=7, sticky=(tk.W, tk.E), pady=5)

ttk.Label(left_frame, text="Temps aller-retour Pokecentre (s):").grid(column=0, row=8, sticky=tk.W, pady=5)
entry_temps_aller_retour = ttk.Entry(left_frame, width=15)
entry_temps_aller_retour.insert(0, str(TEMPS_ALLER_RETOUR_POKECENTRE))
entry_temps_aller_retour.grid(column=1, row=8, sticky=(tk.W, tk.E), pady=5)

ttk.Label(left_frame, text="Taux de shiny:").grid(column=0, row=9, sticky=tk.W, pady=5)
var_shiny_rate = tk.StringVar(value="standard")
ttk.Radiobutton(left_frame, text="Standard (1/30000)", variable=var_shiny_rate, value="standard").grid(column=1, row=9, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Donator (1/27000)", variable=var_shiny_rate, value="donator").grid(column=1, row=10, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Donator + Shiny Charm (1/24300)", variable=var_shiny_rate, value="donator_charm").grid(column=1, row=11, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Donator + Linking up Shiny Charm (1/25650)", variable=var_shiny_rate, value="donator_link").grid(column=1, row=12, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Shiny Charm (sans Donator) (1/27000)", variable=var_shiny_rate, value="charm").grid(column=1, row=13, sticky=tk.W, pady=2)
ttk.Radiobutton(left_frame, text="Linking up Shiny Charm (sans Donator) (1/28500)", variable=var_shiny_rate, value="link").grid(column=1, row=14, sticky=tk.W, pady=2)

ttk.Button(left_frame, text="Lancer la simulation", command=lancer_simulation).grid(column=0, row=15, columnspan=2, sticky=(tk.W, tk.E), pady=20)

text_resultats = tk.Text(right_frame, wrap=tk.WORD, width=50, height=30, font=("Helvetica", 10))
text_resultats.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
text_resultats.config(state=tk.DISABLED)

scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=text_resultats.yview)
scrollbar.grid(column=1, row=0, sticky=(tk.N, tk.S))
text_resultats.configure(yscrollcommand=scrollbar.set)

# Ajout du numéro de version
version_label = ttk.Label(root, text=f"by ek0onsec | Version {VERSION}", font=("Helvetica", 8))
version_label.grid(row=1, column=0, pady=(0, 10))

# Configuration du redimensionnement
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
left_frame.columnconfigure(1, weight=1)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

# Lancement de la boucle principale
root.mainloop()
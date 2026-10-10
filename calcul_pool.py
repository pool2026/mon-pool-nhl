python
import requests
import pandas as pd
from datetime import datetime

# 1. Charger les choix
choix = pd.read_csv('mes_choix.csv')

# 2. Récupérer les données de la NHL
url_joueurs = "https://nhle.com"
url_gardiens = "https://nhle.com"

# Note: Pour les équipes, on utilise l'API des classements par division
url_equipes = "https://nhle.com"

res_j = requests.get(url_joueurs).json().get('skaters', [])
res_g = requests.get(url_gardiens).json().get('goalies', [])
res_e = requests.get(url_equipes).json().get('standings', [])

total_pool = 0
details = []

# 3. Calculer les points
for _, ligne in choix.iterrows():
    nom = ligne['Nom']
    type_c = ligne['Type']
    pts = 0
    
    if type_c == 'Patineur':
        stats = next((x for x in res_j if x.get('skaterName', {}).get('default') == nom), None)
        if stats:
            pts = stats.get('goals', 0) + stats.get('assists', 0)
    elif type_c == 'Gardien':
        stats = next((x for x in res_g if x.get('goalieName', {}).get('default') == nom), None)
        if stats:
            pts = stats.get('wins', 0) * 2
    elif type_c == 'Équipe':
        # Extraction du nom abrégé ou complet pour l'équipe
        stats = next((x for x in res_e if nom in x.get('teamName', {}).get('default', '')), None)
        if stats:
            pts = stats.get('wins', 0) * 2
            
    total_pool += pts
    details.append(f"{nom} : {pts} pts")

# 4. Écrire le rapport hebdomadaire
date_du_jour = datetime.now().strftime("%Y-%m-%d")
rapport = f"### Mise à jour du {date_du_jour}\n**SCORE TOTAL : {total_pool} POINTS**\n\n" + "\n".join(details) + "\n\n"

with open("historique_scores.md", "a", encoding="utf-8") as f:
    f.write(rapport)

print(f"Calcul terminé avec succès. Total : {total_pool} points.")

  # Air Quality & Population Analysis

## Contexte du projet
Ce projet analyse la qualité de l'air en relation avec la population dans la région Île-de-France. Il s'appuie sur des données publiques, incluant des mesures environnementales (NO₂, O₃, PM10) et des données démographiques communales. Le traitement est réalisé en SQL et Python, avec une visualisation finale sur Power BI.

## Objectifs du projet
- Nettoyer, enrichir et fusionner les données pollution/population
- Mesurer les dépassements des seuils OMS pour :
  - Dioxyde d’azote (NO₂)
  - Ozone troposphérique (O₃)
  - Particules fines (PM10)
- Identifier les zones et périodes les plus touchées
- Calculer des indicateurs de pollution par habitant
- Visualiser les résultats sur un tableau de bord Power BI

## Contenu
- Chargement et traitement des données de qualité de l'air
- Intégration des données de population
- Visualisations des concentrations de polluants par département et commune
- Analyse des corrélations entre densité de population et pollution

## Prérequis
- Python 3.8+
- PostgreSQL
- Power BI Desktop
- Librairies Python : `sqlalchemy`, `psycopg2`, `pandas`, `matplotlib`, `seaborn`, `python-dotenv`

## Visualisations
Des graphiques ont été générés en Python et Power BI pour illustrer les concentrations de polluants, la densité de population, et les croisements entre ces dimensions.

## Fichiers

- `AirQualityPopulation.ipynb` : Notebook Jupyter contenant le traitement des données
- `AirQualityPopulation.py` : Script Python exporté du notebook
- `AirQualityPopulation.sql` : Requêtes SQL pour les traitements en base
- `AirQualityPopulation.pbix` : Tableau de bord interactif Power BI
- `QualiteAir.csv` : Données brutes de pollution atmosphérique (Echantillons de 5000 lignes)
- `population.csv` : Données démographiques par commune
- `.env` : Identifiants de connexion PostgreSQL (pas publié GitHub)
- `requirements.txt` : Bibliothèques Python nécessaires
- `README.md` : Documentation du projet

## Auteur
**Moussa DIABY**  
Projet réalisé avec Python, SQL, PostgreSQL et Power BI.

## Remarques
Ce projet n'est qu'un traitement de base dans le cadre d’un exercice personnel.

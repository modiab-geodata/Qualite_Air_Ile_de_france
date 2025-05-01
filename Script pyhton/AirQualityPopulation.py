# Installer les bibliothèques nécessaires
'''
pip install sqlalchemy 
pip install psycopg2 
pip install pandas  
pip install matplotlib
pip install seaborn

'''

# Importer les bibliothèques nécessaires
import os
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Importer le fichier sur la qualité de l'air en ile de france

chemin_Qualite_Air = "C:/Users/diaby/OneDrive/Bureau/Data_Pipline/QualiteAir.csv" # Définir le chmin vers le fichier csv
df = pd.read_csv(chemin_Qualite_Air, sep=";") # Lire le fichier
df.sample(10) # Afficher 10 lignes aléatoires du DataFrame

# Analyse exploratoire du DataFrame
df.info()
df.isnull().sum()
df.describe()
doublon = df.duplicated()
doublon
df.head()

# Séparer la colonne 'Geo Point 2D' contenant les coordonnées géographiques en 2 colonnes distinctes : latitude et longitude
df[['latitude', 'longitude']] = df['Geo Point 2D'].str.split(',', expand=True) 
df

# Supprimer les colonnes inutiles du DataFrame : 'geom', 'Annee Jointure' et 'Geo Point 2D'
df.drop(['geom','Annee Jointure', 'Geo Point 2D'], axis=1, inplace=True) # l'argument inplace permet d'appliquer l'opération directement dans le DataFrame d'origine sans crée de copie
df

# Renommer les colonnes du DataFrame pour des noms plus clairs
df = df.rename(columns = {
    'Date' : 'date',
    'Code Insee' : 'code_insee',
    'NO2' : 'dioxyde_azote_no2',
    'O3' : 'ozone_o3',
    'PM10' : 'particule_fines_pm10',
    'commune' : 'nom_commune',
    'departement' : 'nom_departement'
})
df

# Quelques visualisations

# Calculer la moyenne de dioxyde_azote_no2 par département

df_moyenne_no2_departement = df.groupby('nom_departement')['dioxyde_azote_no2'].mean().reset_index()

# Visualiser les résultats
plt.figure(figsize=(12, 8))
sns.barplot(x='nom_departement', y='dioxyde_azote_no2', data=df_moyenne_no2_departement)
plt.xticks(rotation=90)
plt.title("Concentration moyenne de dioxyde d'azote par département")
plt.xlabel("Département")
plt.ylabel("Concentration moyenne de NO2")
plt.show()

# Afficher les résultats sous forme de tableau
df_moyenne_no2_departement

#  Calculer la moyenne de ozone_o3 par département

df_moyenne_ozone_o3_departement = df.groupby('nom_departement')['ozone_o3'].mean().reset_index()

# Visualiser les résultats
plt.figure(figsize=(12, 8))
sns.barplot(x='nom_departement', y='ozone_o3', data=df_moyenne_ozone_o3_departement)
plt.xticks(rotation=90)
plt.title("Concentration moyenne de l'ozone par département")
plt.xlabel("Département")
plt.ylabel("Concentration moyenne de O3")
plt.show()

# Afficher les résultats sous forme de tableau
df_moyenne_ozone_o3_departement

# Calculer la moyenne de particules en suspension par département

df_moyenne_particule_fines_pm10_departement = df.groupby('nom_departement')['particule_fines_pm10'].mean().reset_index()

# Visualiser les résultats
plt.figure(figsize=(12, 8))
sns.barplot(x='nom_departement', y='particule_fines_pm10', data=df_moyenne_particule_fines_pm10_departement)
plt.xticks(rotation=90)
plt.title("Concentration moyenne de particules fines PM10 en suspension par département")
plt.xlabel("Département")
plt.ylabel("Concentration moyenne de PM10")
plt.show()

# Afficher les résultats sous forme de tableau
df_moyenne_particule_fines_pm10_departement

# Injesction du DataFrame dans une base de données PostgreSQL

# Créer un fichier .env afin d'y stocker les informations de connexion de la base de données postgreSQL

# Chemin complet vers ton fichier .env
chemin_env_air = "C:/Users/diaby/OneDrive/Bureau/Data_Pipline/.env"
charger_env(chemin_env_air=chemin_env_air)

# Maintenant, récupèrer les variables
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
db = os.getenv("PG_DB")

# Définir l'URL de connexion
DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db}'

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Injecter le DataFrame dans la base de données PostgreSQL
df.to_sql('pollution', engine, if_exists='replace', index=False)
print("DataFrame chargé dans la table 'pollution_data' avec succès !")

# Importer le fichier sur la population
chemin_population = "C:/Users/diaby/OneDrive/Bureau/Data_Pipline/population.csv" 
df = pd.read_csv(chemin_population, sep=";", encoding="latin1") 
df.sample(10)  # Afficher 10 lignes aléatoires du DataFrame

# Analyse exploratoire du DataFrame
df.dtypes
df.isnull().sum()
df.info()
df.describe()

# Suppression des lignes contenant des valeurs nulles dans la colonne 'p_pop'.
# On aurait aussi pu choisir une autre méthode d'imputation pour traiter ces valeurs manquantes.
df = df.dropna(subset=["p_pop"])
df

# Renommer les colonnes du DataFrame pour des noms plus clairs

df = df.rename(columns = {
    'codgeo' : 'code_geo',
    'libgeo' : 'nom_commune',
    'an' : 'annee_population',
    'p_pop' : 'nombre_population'
})
df

# Supprimer les colonnes inutiles du DataFrame : 'annee_population'
df.drop(['annee_population'], axis=1, inplace=True) # l'argument inplace permet d'appliquer l'opération directement dans la dataFrame d'origine sans crée de copie
df

# Chemin complet vers ton fichier .env
chemin_env_air = "C:/Users/diaby/OneDrive/Bureau/Data_Pipline/.env"
charger_env(chemin_env_air=chemin_env_air)

# Maintenant, récupèrer les variables
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
db = os.getenv("PG_DB")

# Définir l'URL de connexion
DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db}'

# Créer l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Injecter le DataFrame dans la base de données PostgreSQL
df.to_sql('pollution', engine, if_exists='replace', index=False)
print("DataFrame chargé dans la table 'pollution_data' avec succès !")

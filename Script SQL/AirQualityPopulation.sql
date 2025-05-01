-- EXPLORATION INITIALE
SELECT * FROM public.pollution_data LIMIT 10;
SELECT * FROM public.population_data LIMIT 10;
SELECT COUNT(*) FROM public.pollution_data;
SELECT COUNT(*) FROM public.population_data;

-- INDEX POUR OPTIMISER LES REQUÊTES
CREATE INDEX idx_colonnes ON public.pollution_data (date, code_insee);

-- SAUVEGARDE DES TABLES ORIGINALES
CREATE TABLE IF NOT EXISTS public.pollution_data_old AS SELECT * FROM public.pollution_data;
CREATE TABLE IF NOT EXISTS public.population_data_old AS SELECT * FROM public.population_data;

-- AJOUT DE COLONNES annee ET mois
ALTER TABLE public.pollution_data ADD COLUMN annee INT, ADD COLUMN mois INT;
UPDATE public.pollution_data SET annee = EXTRACT(YEAR FROM date::date), mois = EXTRACT(MONTH FROM date::date);

-- BIEN TYPER DONNEES LES TYPIE
SELECT date,
       CAST(code_insee AS TEXT) AS code_insee,
       CAST(dioxyde_azote_no2 AS INT) AS dioxyde_azote_no2,
       CAST(ozone_o3 AS INT) AS ozone_o3,
       CAST(particule_fines_pm10 AS INT) AS particule_fines_pm10,
       nom_commune,
       nom_departement,
       latitude,
       longitude,
       annee,
       mois
FROM public.pollution_data;

-- RECREATION DE LA TABLE AVEC LES BONS TYPAGES
DROP TABLE IF EXISTS public.pollution_data_new;
CREATE TABLE public.pollution_data_new AS
SELECT date,
       CAST(code_insee AS TEXT) AS code_insee,
       CAST(dioxyde_azote_no2 AS INT) AS dioxyde_azote_no2,
       CAST(ozone_o3 AS INT) AS ozone_o3,
       CAST(particule_fines_pm10 AS INT) AS particule_fines_pm10,
       nom_commune,
       nom_departement,
       latitude,
       longitude,
       annee,
       mois
FROM public.pollution_data;

DROP TABLE IF EXISTS public.pollution_data;
CREATE TABLE public.pollution_data AS SELECT * FROM public.pollution_data_new;
DROP TABLE public.pollution_data_new;

-- JOINTURE AVEC LA TABLE POPULATION
CREATE TABLE IF NOT EXISTS public.pollution_population AS
SELECT p.*, pop.nombre_population
FROM public.pollution_data p
LEFT JOIN public.population_data pop ON p.code_insee = pop.code_geo;

-- VERIFICATION
SELECT * FROM public.pollution_population LIMIT 10;

-- ANALYSES
-- 1. Moyennes annuelles des particules et par commune
SELECT annee, code_insee, nom_commune,
       ROUND(AVG(dioxyde_azote_no2), 0) AS avg_dioxyde_azote_no2,
       ROUND(AVG(ozone_o3), 0) AS avg_ozone_o3,
       ROUND(AVG(particule_fines_pm10), 0) AS avg_pm10
FROM public.pollution_population
GROUP BY annee, code_insee, nom_commune;

-- 2. Moyennes annuelles des particules et par département
SELECT annee, code_insee, nom_departement,
       ROUND(AVG(dioxyde_azote_no2), 0) AS avg_dioxyde_azote_no2,
       ROUND(AVG(ozone_o3), 0) AS avg_ozone_o3,
       ROUND(AVG(particule_fines_pm10), 0) AS avg_pm10
FROM public.pollution_population
GROUP BY annee, code_insee, nom_departement;

-- 3. Année la plus polluée par département (NO2)
SELECT DISTINCT ON (nom_departement)
       code_insee, annee, nom_departement,
       MAX(dioxyde_azote_no2) AS max_no2
FROM public.pollution_population
GROUP BY code_insee, annee, nom_departement
ORDER BY nom_departement, max_no2 DESC;

-- 4. Min/Max/Moy de PM10 par commune, an et mois
SELECT code_insee, annee, mois, nom_commune,
       MIN(particule_fines_pm10) AS min_pm10,
       MAX(particule_fines_pm10) AS max_pm10,
       ROUND(AVG(particule_fines_pm10), 0) AS avg_pm10
FROM public.pollution_population
GROUP BY code_insee, annee, mois, nom_commune;

-- 5. Classement des communes par pollution PM10
SELECT code_insee, nom_commune, annee, mois, particule_fines_pm10,
       RANK() OVER (PARTITION BY code_insee ORDER BY particule_fines_pm10 DESC) AS rang_pollution
FROM public.pollution_population;

-- 6. Communes dépassant les seuils de l'OMS
		--NO2  = 10µg/m³
		--O3   = 60µg/m³
		--PM10 = 15µg/m³
		
SELECT DISTINCT ON (nom_commune)
       code_insee, annee, mois, nom_commune,
       dioxyde_azote_no2, ozone_o3, particule_fines_pm10
FROM public.pollution_population
WHERE dioxyde_azote_no2 > 10 AND ozone_o3 > 60 AND particule_fines_pm10 > 15;

-- CALCUL DES INDICATEURS
ALTER TABLE public.pollution_population
ADD COLUMN taux_pollution_habitant_no2 FLOAT,
ADD COLUMN taux_pollution_habitant_o3 FLOAT,
ADD COLUMN taux_pollution_habitant_mp10 FLOAT,
ADD COLUMN depassement_seuil_osm_no2 VARCHAR,
ADD COLUMN depassement_seuil_osm_o3 VARCHAR,
ADD COLUMN depassement_seuil_osm_pm10 VARCHAR;

UPDATE public.pollution_population
SET taux_pollution_habitant_no2 = ROUND(CASE WHEN nombre_population > 0 THEN dioxyde_azote_no2 / nombre_population::NUMERIC ELSE NULL END, 2),
    taux_pollution_habitant_o3 = ROUND(CASE WHEN nombre_population > 0 THEN ozone_o3 / nombre_population::NUMERIC ELSE NULL END, 2),
    taux_pollution_habitant_mp10 = ROUND(CASE WHEN nombre_population > 0 THEN particule_fines_pm10 / nombre_population::NUMERIC ELSE NULL END, 2),
    depassement_seuil_osm_no2 = CASE WHEN dioxyde_azote_no2 > 10 THEN 'Oui' ELSE 'Non' END,
    depassement_seuil_osm_o3 = CASE WHEN ozone_o3 > 60 THEN 'Oui' ELSE 'Non' END,
    depassement_seuil_osm_pm10 = CASE WHEN particule_fines_pm10 > 15 THEN 'Oui' ELSE 'Non' END;

-- Requête finale
SELECT * 
FROM public.pollution_population

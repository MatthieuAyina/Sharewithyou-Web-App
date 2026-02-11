-- Configuration de l'environnement de travail
CREATE OR REPLACE WAREHOUSE WH_LAB WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60;
CREATE DATABASE IF NOT EXISTS DB_LAB;
CREATE SCHEMA IF NOT EXISTS DB_LAB.CHAT_APP;

-- Création de la table de persistance (Partie D)
CREATE TABLE IF NOT EXISTS DB_LAB.CHAT_APP.CONVERSATIONS (
    TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    MODEL STRING,
    ROLE STRING,
    CONTENT STRING
);

-- Test de la fonction Cortex en SQL pur (Demande du professeur)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2', 
    'Bonjour, es-tu opérationnel ?'
);


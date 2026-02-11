# Sharewithyou-Web-App

# 🤝 Projet : Share with you - Assistant IA sur Snowflake

Ce projet est un application web intelligente développée dans Snowflake.

## ✨ Fonctionnalités
- **Interface Conversationnelle** : Chat interactif avec avatars personnalisés.
- **Intelligence Artificielle** : Utilisation des LLM via `SNOWFLAKE.CORTEX`.
- **Mémoire Contextuelle** : Gestion de l'historique des échanges.
- **Persistance SQL** : Sauvegarde automatique de chaque message dans une table Snowflake.

## 🛠️ Choix Techniques
- **Langage** : Python (Streamlit).
- **Appel LLM** : Requêtes SQL via Snowpark pour une meilleure stabilité sur les comptes Trial.
- **Modèle de prédilection** : `mistral-large2` pour sa pertinence en français.

## 🧠 Questions de Validation
1. **Modèle utilisé** : Mistral-Large2, sélectionné pour sa précision et son intégration native.
2. **Gestion de l'historique** : Filtrage dynamique des rôles (System/User/Assistant) pour respecter la séquence exigée par Cortex.
3. **Sécurité** : Les données restent confinées dans l'infrastructure Snowflake, garantissant une confidentialité totale.

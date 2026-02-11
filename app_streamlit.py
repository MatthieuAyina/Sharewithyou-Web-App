import streamlit as st
from snowflake.snowpark.context import get_active_session
import snowflake.cortex as cortex

# Accès à la session Snowflake
session = get_active_session()

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Share with you", page_icon="🤝", layout="centered")

# --- 2. FONCTION DE PERSISTANCE (PARTIE D) ---
def save_message(role, content, model):
    """Enregistre le message dans Snowflake"""
    try:
        # On échappe les apostrophes pour le SQL
        clean_content = content.replace("'", "''")
        query = f"""
            INSERT INTO DB_LAB.CHAT_APP.CONVERSATIONS (ROLE, CONTENT, MODEL)
            VALUES ('{role}', '{clean_content}', '{model}')
        """
        session.sql(query).collect()
    except Exception as e:
        st.error(f"Erreur d'enregistrement : {e}")

# --- 3. GESTION DE L'ÉTAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🤝 Share with you")
    st.divider()
    model_choice = st.selectbox("Modèle LLM", ["mistral-large2"])
    temp_choice = st.slider("Température", 0.0, 1.5, 0.7)
    
    if st.button("🗑️ Effacer la discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. INTERFACE PRINCIPALE ---
st.title("Share with you")
st.markdown("*Je suis ravi de vous voir. Posez-moi vos questions, partagez vos idées, ou explorons vos données ensemble dans cet espace sécurisé.*")
st.divider()

# Affichage de l'historique
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "🤝"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
# --- 6. LOGIQUE DE CHAT (VERSION SQL SNOWPARK COMPLÈTE) ---
if prompt := st.chat_input("Dites-moi quelque chose..."):
    
    # 1. Gestion du message utilisateur (Session + Affichage)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # 2. Sauvegarde dans la table SQL (Partie D)
    save_message("user", prompt, model_choice)

    # 3. Génération de la réponse assistant
    with st.chat_message("assistant", avatar="🤝"):
        with st.spinner("Share with you réfléchit..."):
            try:
                import json
                
                # --- NETTOYAGE DE LA SÉQUENCE DES MESSAGES ---
                # On force le rôle 'system' en premier pour Cortex
                messages_clean = [{"role": "system", "content": "Tu es l'assistant IA 'Share with you'."}]
                
                # On ajoute les messages user/assistant en alternance stricte
                for msg in st.session_state.messages:
                    if msg["role"] in ["user", "assistant"] and msg["content"]:
                        messages_clean.append({"role": msg["role"], "content": msg["content"]})
                
                # --- PRÉPARATION DE LA REQUÊTE SQL (Demande du professeur) ---
                # Conversion de la liste Python en chaîne JSON sécurisée pour SQL
                history_json = json.dumps(messages_clean).replace("'", "''")
                
                sql_query = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{model_choice}', 
                        PARSE_JSON('{history_json}'), 
                        {{'temperature': {temp_choice}}}
                    ) AS RESP
                """
                
                # Exécution de la requête via Snowpark
                sql_result = session.sql(sql_query).collect()
                raw_response = sql_result[0]['RESP']
                
                # --- EXTRACTION DU TEXTE DEPUIS LE JSON REÇU ---
                # Snowflake retourne un objet JSON, on extrait le message final
                json_data = json.loads(raw_response)
                final_text = json_data["choices"][0]["messages"]
                
                # 4. Affichage et sauvegarde de la réponse assistant
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                save_message("assistant", final_text, model_choice)
                
            except Exception as e:
                # Affiche l'erreur technique (ex: Trial account limitation)
                st.error(f"Erreur d'appel SQL Cortex : {e}")

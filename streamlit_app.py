import streamlit as st
import requests
import json
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Bot Multiagente - LangGraph Demo",
    page_icon="🤖",
    layout="centered"
)

# Título
st.title("🤖 Bot Multiagente - LangGraph Demo")
st.markdown("*Powered by Qwen3:8B + LangGraph*")

# URL de la API
API_URL = "http://localhost:8000/chat"

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtener respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    bot_response = response.json()["answer"]
                    st.markdown(bot_response)
                    
                    # Agregar respuesta del bot al historial
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Error de conexión: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    **Funcionalidades:**
    - 💬 Chat conversacional
    - 🌤️ Consulta del clima
    - 🖼️ Generación de imágenes
    - 🔀 Decisión automática de herramientas
    
    **Ejemplos:**
    - "¿Cómo está el clima en Madrid?"
    - "Genera una imagen de un gato"
    - "Hola, ¿cómo estás?"
    """)
    
    if st.button("🗑️ Limpiar chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Estado de la API:**")
    
    try:
        health_response = requests.get("http://localhost:8000/docs", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API conectada")
        else:
            st.error("❌ API no responde")
    except:
        st.error("❌ API no disponible")
        st.markdown("Asegúrate de ejecutar: `python -m uvicorn src.app:app --reload --port 8000`")
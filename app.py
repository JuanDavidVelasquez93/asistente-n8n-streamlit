import streamlit as st
import requests

# URL de tu webhook de n8n (ajústala)
N8N_WEBHOOK_URL = "https://sistecredito.app.n8n.cloud/mcp/MCP"  # <-- cámbiala

st.title("💬 Asistente Empresarial")
st.markdown("Pregunta lo que quieras al agente conectado a la base de datos.")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu pregunta..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar a n8n
    try:
        response = requests.post(N8N_WEBHOOK_URL, json={"chatInput": prompt})
        result = response.json().get("output", "❌ El agente no respondió correctamente.")
    except Exception as e:
        result = f"❌ Error al contactar el agente: {e}"

    # Mostrar respuesta
    st.session_state.messages.append({"role": "assistant", "content": result})
    with st.chat_message("assistant"):
        st.markdown(result)

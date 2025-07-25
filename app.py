import streamlit as st
import requests
import json

# URL del webhook de n8n (ajústala si cambia)
N8N_WEBHOOK_URL = "https://sistecredito.app.n8n.cloud/mcp/MCP"

st.set_page_config(page_title="Asistente Empresarial")
st.title("💬 Asistente Empresarial")
st.markdown("Pregunta lo que quieras al agente conectado a la base de datos.")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta..."):
    # Agregar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar a n8n
    try:
        response = requests.post(N8N_WEBHOOK_URL, json={"chatInput": prompt})

        # Intentar parsear el JSON, incluso si viene como string
        raw = response.text
        try:
            data = json.loads(raw)
            if isinstance(data, str):  # doble parsing si aún es string
                data = json.loads(data)
        except Exception:
            data = response.json()

        # Extraer respuesta del agente
        respuesta = data.get("respuesta")
        empleados = data.get("empleados", [])

        # Construir respuesta para el chat
        if respuesta:
            result_md = f"✅ **{respuesta}**"
        else:
            result_md = "❌ El agente no respondió correctamente."

        # Mostrar detalles de empleados si existen
        if empleados:
            for emp in empleados:
                nombre = emp.get("nombre", "Nombre no disponible")
                valor = emp.get("valor_credito", "N/A")
                fecha = emp.get("fecha", "Sin fecha")
                result_md += f"\n\n🧑‍💼 **{nombre}**\n- 💰 Crédito: {valor}\n- 🗓 Fecha: {fecha}"

    except Exception as e:
        result_md = f"❌ Error al contactar el agente: {e}"

    # Mostrar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": result_md})
    with st.chat_message("assistant"):
        st.markdown(result_md)

import streamlit as st
import requests
import json

# URL del webhook de n8n (ajústala si cambia)
N8N_WEBHOOK_URL = "https://sistecredito.app.n8n.cloud/mcp/MCP"

st.set_page_config(page_title="Asistente Empresarial")
st.title("💬 Asistente Empresarial de información de clientes")
st.markdown("Pregunta lo que quieras al agente csobre creditos.")

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
        headers = {
            "Accept": "application/json, text/plain",
            "Content-Type": "application/json"
        }
        response = requests.post(N8N_WEBHOOK_URL, json={"chatInput": prompt}, headers=headers)

        # Intentar parsear el JSON, incluso si viene como string anidado
        raw = response.text
        try:
            data = json.loads(raw)
            if isinstance(data, str):
                data = json.loads(data)
        except Exception:
            data = response.json()

        # Normalizar si viene dentro de "output"
        if isinstance(data, dict) and "output" in data:
            data = data["output"]

        # Procesar respuesta en distintos formatos
        if isinstance(data, dict):
            if "respuesta" in data and isinstance(data["respuesta"], str):
                result_md = f"✅ **{data['respuesta']}**"
                # Mostrar otros campos como bloques JSON
                for k, v in data.items():
                    if k != "respuesta":
                        result_md += f"\n\n🔹 **{k.capitalize()}**:\n```json\n{json.dumps(v, indent=2, ensure_ascii=False)}\n```"
            else:
                result_md = f"📄 Respuesta JSON:\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        elif isinstance(data, str):
            result_md = f"💬 {data}"
        else:
            result_md = f"📎 Respuesta sin formato:\n```{data}```"

    except Exception as e:
        result_md = f"❌ Error al contactar el agente: {e}"

    # Mostrar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": result_md})
    with st.chat_message("assistant"):
        st.markdown(result_md)

import streamlit as st

# --- ESTILO DA SIDEBAR ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #0D4920;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-testid="stRadio"] {
        margin-bottom: 0.25rem !important;
    }
    div[data-testid="stRadio"] > label {
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("EcoGuide ChatBot")

# Opções: Chat + FAQs
options = ["Chat"] + [
    "What are the greenhouse gases?",
    "How are indigenous people being affected by climate change?",
    "What should be the percent reduction in global passenger car fleet emissions by 2025?",
    "What are emission factors, and how are they determined?",
    "What is the main problematic greenhouse gas and what are its causes?"
]
selected_option = st.sidebar.radio("Escolha uma opção:", options)

# --- RESPOSTAS FIXAS ---
responses = {
    "What are the greenhouse gases?": "Greenhouse gases include CO₂, CH₄, N₂O, and fluorinated gases. They trap heat in the atmosphere.",
    "How are indigenous people being affected by climate change?": "Indigenous communities face loss of land, biodiversity, and cultural heritage due to rising temperatures and extreme events.",
    "What should be the percent reduction in global passenger car fleet emissions by 2025?": "A 45% reduction from 2020 levels is recommended to align with climate goals.",
    "What are emission factors, and how are they determined?": "Emission factors represent the average emission rate of a pollutant for a specific source, determined through empirical studies and lab testing.",
    "What is the main problematic greenhouse gas and what are its causes?": "CO₂ is the most impactful greenhouse gas, mainly from burning fossil fuels for energy and transport."
}

# --- MAIN UI HEADER ---
st.markdown("## EcoGuide ChatBot")
st.caption("Respostas rápidas sobre clima e sustentabilidade")

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MODO FAQ ---
# --- CHAT MODE ONLY ---
if selected_option == "Chat":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ Show file uploader BEFORE first message in Chat
    if "has_sent_message" not in st.session_state:
        st.markdown("### Upload Documents")
        uploaded_file = st.file_uploader("Select a file", type=["txt", "pdf", "docx"])
        if uploaded_file is not None:
            st.success(f"File uploaded successfully: **{uploaded_file.name}**")

    # Input box
    user_input = st.chat_input("Type your message...")

    if user_input and "last_user_input" not in st.session_state:
        st.session_state.last_user_input = user_input
        st.session_state.has_sent_message = True  # ✅ mark as sent

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        bot_reply = f"(simulated) You said: {user_input}"
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

import streamlit as st
from groq import Groq

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="EduBot - Data Science Assistant", page_icon="🤖")

st.title("🤖 EduBot: Asisten Belajar Data Science")
st.caption("Chatbot interaktif berbasis Groq API & LLM (Llama 3)")

# Input API Key di Sidebar
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Groq API Key:", type="password")
    st.markdown("[Dapatkan Groq API Key Gratis](https://console.groq.com/)")

# Inisialisasi Riwayat Chat (st.session_state)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah EduBot, asisten belajar Data Science yang ramah, santai, dan cerdas. Tugasmu adalah membantu pengguna memahami konsep Python, AI, dan Machine Learning dengan contoh sederhana."}
    ]

# Tampilkan Riwayat Chat di Layar
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Prompt Input Pengguna
if prompt := st.chat_input("Tanyakan sesuatu tentang Data Science..."):
    if not api_key:
        st.error("Silakan masukkan Groq API Key kamu di sidebar sebelah kiri!")
        st.stop()

    # Simpan input pengguna ke session_state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Panggil Groq API
    client = Groq(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content

        # Simpan dan tampilkan respons bot
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
      

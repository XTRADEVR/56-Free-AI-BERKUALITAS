import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="56 AI Tools - Bisa Klik", layout="wide")

st.markdown("""
<style>
    .stLinkButton>button { width: 100%; border-radius: 12px; background: #1f2937; border: 1px solid #374151; }
    .stLinkButton>button:hover { background: #dc2626; color: white; border-color: #dc2626; }
</style>
""", unsafe_allow_html=True)

st.title("🔴 56 FREE AI TOOLS - Klik Langsung Kebuka")

# --- FIX API KEY BIAR GAK ERROR ---
# 1. Coba ambil dari Secrets dulu (yang di Manage App)
# 2. Kalau gak ada, ambil dari input sidebar
api_key = st.secrets.get("GEMINI_API_KEY", "") if "GEMINI_API_KEY" in st.secrets else ""

with st.sidebar:
    st.subheader("🔑 API Key")
    input_key = st.text_input("Gemini API Key", value=api_key, type="password")
    if input_key:
        api_key = input_key
    st.info("Cara set Secrets biar permanen:\nManage app > Settings > Secrets > paste:\nGEMINI_API_KEY = \"...\"")
    menu = st.radio("Menu", ["💬 AI Chat", "🌐 56 Tools"])

# --- DATA 56 TOOLS + LINK ASLI ---
tools = {
    "1 AI IMAGE": [("DALL-E 3", "https://openai.com/dall-e-3"), ("Midjourney", "https://midjourney.com"), ("Leonardo AI", "https://leonardo.ai"), ("Ideogram", "https://ideogram.ai")],
    "2 AI VIDEO": [("Runway", "https://runwayml.com"), ("Pika Labs", "https://pika.art"), ("Luma AI", "https://lumalabs.ai"), ("CapCut", "https://capcut.com")],
    "3 AI WRITING": [("ChatGPT", "https://chatgpt.com"), ("Claude", "https://claude.ai"), ("Gemini", "https://gemini.google.com"), ("Perplexity", "https://perplexity.ai")],
    "4 RESEARCH": [("Elicit", "https://elicit.com"), ("Consensus", "https://consensus.app"), ("ChatPDF", "https://chatpdf.com")],
    "5 PRODUCTIVITY": [("Notion AI", "https://notion.so"), ("Otter.ai", "https://otter.ai"), ("Taskade", "https://taskade.com"), ("Supernormal", "https://supernormal.com")],
}

if menu == "🌐 56 Tools":
    search = st.text_input("Cari tools...", placeholder="Ketik: Runway, Midjourney, ChatGPT")
    for kategori, daftar in tools.items():
        st.subheader(kategori)
        cols = st.columns(4)
        for i, (nama, link) in enumerate(daftar):
            if not search or search.lower() in nama.lower():
                with cols[i % 4]:
                    # INI YANG BIKIN BISA DI-KLIK
                    st.link_button(f"🔗 {nama}", link, use_container_width=True)
        st.divider()

else:
    st.subheader("💬 Tanya AI - Gemini 3.5 Flash Lite")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    if prompt := st.chat_input("Ask about AI tools... Contoh: Tool video"):
        if not api_key:
            st.error("Set GEMINI_API_KEY di Secrets dulu king -> Manage app > Settings > Secrets")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash-lite")
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                res = model.generate_content(prompt)
                st.write(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})

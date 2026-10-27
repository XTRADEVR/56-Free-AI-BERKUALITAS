import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="56 AI Tools Hub - 2026", layout="wide", page_icon="🤖")

# --- CSS LUXURY RED KAYAK POSTER LU ---
st.markdown("""
<style>
.stApp { background: #0a0000; }
.tool-card { background: rgba(255,255,255,0.06); backdrop-filter: blur(12px); border: 1px solid rgba(255,80,80,0.2); border-radius: 16px; padding: 12px; text-align: center; transition: 0.2s; }
.tool-card:hover { background: rgba(255,80,80,0.15); transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- GEMINI 3.5 FLASH LITE CONFIG ---
# Pakai secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash-lite") # ini nama API untuk 3.5 lite
except:
    model = None

st.title("🔴 56 FREE AI TOOLS - Every Creator Should Use in 2026")
col1, col2 = st.columns([2, 1])

with col1:
    # Tampilkan poster lu
    st.image("https://raw.githubusercontent.com/DasBersama/ai-streamlit-hub-pro/main/poster.jpg", use_container_width=True, caption="Poster asli 56 tools - klik kategori di kanan")
    st.info("💡 Taruh file poster lu ini namanya `poster.jpg` di root GitHub biar kebaca. Atau gue udah pake link placeholder.")

# --- DATABASE 56 TOOLS DARI POSTER LU ---
tools_data = {
    "1 AI IMAGE": ["DALL-E 3", "Midjourney", "Leonardo AI", "Ideogram", "Recraft AI", "Adobe Firefly", "Playground AI", "Bing Image", "Canva AI", "Freepik AI", "Lexica", "NightCafe", "Craiyon", "Fotor AI", "PicLumen", "DeepAI"],
    "2 AI VIDEO": ["Runway", "Pika Labs", "Kling AI", "Luma AI", "Haiper", "CapCut AI", "Veo 3", "Synthesia", "Descript", "InVideo AI", "FlexClip", "Opus Clip", "Filmora AI", "PixVerse", "Steve AI", "Wisecut"],
    "3 AI WRITING": ["ChatGPT", "Claude", "Gemini", "Perplexity", "Notion AI", "Copy.ai", "Writesonic", "Anyword", "Jasper AI", "Rytr", "Wordtune", "QuillBot", "Grammarly", "Sudowrite", "Frase", "ContentBot"],
    "4 SOCIAL MEDIA": ["Predis.ai", "Later AI", "Ocoya", "Buffer AI", "Metricool", "Vista Social", "Lately", "Hootsuite AI", "Taplio", "SocialBee", "Typefully", "TweetHunter", "Brand24", "Peech", "Postwise", "FeedHive"],
    "5 RESEARCH": ["Elicit", "Consensus", "Scispace", "ChatPDF", "Scholary", "ResearchRabbit", "Connected Papers", "Semantic Scholar", "TLDR This", "Humata AI", "Explainpaper", "Paperpal"],
    "6 PRODUCTIVITY": ["Notion AI", "ClickUp AI", "Trello AI", "Coda AI", "Motion", "Otter.ai", "SaneBox", "Reclaim AI", "Zapier AI", "Make", "Phind", "Taskade", "Do Anything Machine", "MindPal", "Mem AI", "Supernormal"],
}

with col2:
    st.subheader("💬 Tanya AI tentang 56 Tools ini")
    st.caption("Model: gemini-3.5-flash-lite - chat tersimpan")
    
    if "chat" not in st.session_state:
        st.session_state.chat = []
    
    # Search tools
    search = st.text_input("Cari tool...", placeholder="Contoh: Runway, Midjourney")
    
    # Tampilkan tools
    for kategori, tools in tools_data.items():
        if search.lower() in kategori.lower() or any(search.lower() in t.lower() for t in tools):
            st.markdown(f"**{kategori}**")
            cols = st.columns(4)
            for i, t in enumerate(tools):
                if not search or search.lower() in t.lower():
                    with cols[i % 4]:
                        st.markdown(f'<div class="tool-card">{t}</div>', unsafe_allow_html=True)
    
    st.divider()
    # Chat AI
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    
    if prompt := st.chat_input("Ask about AI tools... Contoh: Tool video"):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            if model:
                try:
                    # Kasih konteks 56 tools ke AI
                    context = f"Kamu adalah ahli 56 AI tools ini: {tools_data}. Jawab pertanyaan user: {prompt}"
                    res = model.generate_content(context)
                    st.write(res.text)
                    st.session_state.chat.append({"role": "assistant", "content": res.text})
                except Exception as e:
                    st.error(f"Model error, coba lagi. {e}")
            else:
                st.error("Set GEMINI_API_KEY di Secrets dulu king")

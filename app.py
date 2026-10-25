import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="56 FREE AI TOOLS 2026", page_icon="🤖", layout="wide")

# --- CSS MERAH LUXURY ---
st.markdown("""
<style>
.stApp { background: radial-gradient(800px 400px at 50% 0%, #7a0a0a, #0a0000); background-color: #0a0000; }
.title-box { background: linear-gradient(180deg, #ff0f0f, #7a0000); border: 2px solid #ff3d3d; border-radius: 18px; padding: 18px 24px; text-align: center; box-shadow: 0 0 30px rgba(255,0,0,0.6); }
.category-box { background: linear-gradient(180deg, rgba(255,20,20,0.18), rgba(60,0,0,0.9)); border: 1.5px solid #ff2a2a; border-radius: 16px; padding: 12px; margin-bottom: 14px; }
.tool-link { background: rgba(0,0,0,0.6); border: 1px solid rgba(255,60,60,0.3); border-radius: 10px; padding: 8px 4px; text-align: center; margin-bottom: 8px; }
.tool-link a { color: white !important; text-decoration: none !important; font-size: 11px; font-weight: 600; }
.tool-link:hover { background: rgba(255,20,20,0.5); }
.center-box { background: linear-gradient(180deg, #ff1a1a, #4a0000); border: 2px solid #ff4444; border-radius: 16px; padding: 16px; text-align: center; }
div[data-testid="stChatMessage"] { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,60,60,0.3); border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

# --- SIMPAN API KEY & CHAT (GAK ILANG) ---
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR SIMPAN KEY ---
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.caption("Chat akan tersimpan di sini")
    
    api_input = st.text_input("Enter your Gemini API Key", type="password", value=st.session_state.gemini_key, placeholder="AIza...")
    
    if api_input:
        st.session_state.gemini_key = api_input
        st.success("Key tersimpan ✅")
    
    st.markdown("Dapet gratis di: [aistudio.google.com](https://aistudio.google.com/app/apikey)")
    st.divider()
    
    if st.button("🗑️ Hapus Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.write(f"💬 Chat tersimpan: {len(st.session_state.chat_history)} pesan")

    # Tampilkan chat history di sidebar biar tetep kelihatan
    if st.session_state.chat_history:
        st.markdown("---")
        for chat in st.session_state.chat_history[-6:]:
            with st.chat_message(chat["role"]):
                st.write(chat["content"][:200])

# --- DATA 56 TOOLS ---
TOOLS = {
  "1 AI IMAGE GENERATION": {"DALL·E 3":"https://openai.com/dall-e-3","Midjourney":"https://midjourney.com","Leonardo AI":"https://leonardo.ai","Ideogram":"https://ideogram.ai","Recraft AI":"https://recraft.ai","Adobe Firefly":"https://firefly.adobe.com","Playground AI":"https://playground.com","Bing Image Creator":"https://www.bing.com/images/create","Canva AI":"https://www.canva.com/ai-image-generator/","Freepik AI":"https://www.freepik.com/ai","Lexica":"https://lexica.art","NightCafe":"https://creator.nightcafe.studio","Craiyon":"https://www.craiyon.com","Fotor AI":"https://www.fotor.com/ai-image-generator/","PicLumen":"https://piclumen.com","DeepAI":"https://deepai.org"},
  "2 AI VIDEO CREATION": {"Runway":"https://runwayml.com","Pika Labs":"https://pika.art","Kling AI":"https://klingai.com","Luma AI":"https://lumalabs.ai","Haiper":"https://haiper.ai","CapCut AI":"https://www.capcut.com/tools/ai-video-maker","Veo 3":"https://deepmind.google/models/veo/","Synthesia":"https://www.synthesia.io","Descript":"https://www.descript.com","InVideo AI":"https://invideo.io","FlexClip":"https://www.flexclip.com","Opus Clip":"https://www.opus.pro","Filmora AI":"https://filmora.wondershare.com","PixVerse":"https://pixverse.ai","Steve AI":"https://www.steve.ai","Wisecut":"https://www.wisecut.video"},
  "3 AI WRITING & CONTENT": {"ChatGPT":"https://chat.openai.com","Claude":"https://claude.ai","Gemini":"https://gemini.google.com","Perplexity":"https://www.perplexity.ai","Notion AI":"https://www.notion.so/product/ai","Copy.ai":"https://www.copy.ai","Writesonic":"https://writesonic.com","Anyword":"https://anyword.com","Jasper AI":"https://www.jasper.ai","Rytr":"https://rytr.me","Wordtune":"https://www.wordtune.com","QuillBot":"https://quillbot.com","Grammarly":"https://www.grammarly.com","Sudowrite":"https://www.sudowrite.com","Frase":"https://www.frase.io","ContentBot":"https://contentbot.ai"},
  "4 AI SOCIAL MEDIA TOOLS": {"Predis.ai":"https://predis.ai","Later AI":"https://later.com","Ocoya":"https://www.ocoya.com","Buffer AI":"https://buffer.com","Metricool":"https://metricool.com","Vista Social":"https://vistasocial.com","Lately":"https://www.lately.ai","Hootsuite AI":"https://www.hootsuite.com","Taplio":"https://taplio.com","SocialBee":"https://socialbee.com","Typefully":"https://typefully.com","TweetHunter":"https://tweethunter.io","Brand24":"https://brand24.com","Peech":"https://www.peech-ai.com","Postwise":"https://postwise.ai","FeedHive":"https://www.feedhive.com"},
  "5 AI RESEARCH & STUDY": {"Elicit":"https://elicit.com","Consensus":"https://consensus.app","Scispace":"https://typeset.io","ChatPDF":"https://www.chatpdf.com","Scholarcy":"https://www.scholarcy.com","ResearchRabbit":"https://www.researchrabbit.ai","Connected Papers":"https://www.connectedpapers.com","Semantic Scholar":"https://www.semanticscholar.org","TLDR This":"https://tldrthis.com","Humata AI":"https://www.humata.ai","Explainpaper":"https://www.explainpaper.com","Paperpal":"https://paperpal.com"},
  "6 AI PRODUCTIVITY & AUTOMATION": {"Notion AI":"https://www.notion.so/product/ai","ClickUp AI":"https://clickup.com/ai","Trello AI":"https://trello.com","Coda AI":"https://coda.io","Motion":"https://www.usemotion.com","Otter.ai":"https://otter.ai","SaneBox":"https://www.sanebox.com","Reclaim AI":"https://reclaim.ai","Zapier AI":"https://zapier.com","Make":"https://make.com","Phind":"https://www.phind.com","Taskade":"https://www.taskade.com","Do Anything Machine":"https://www.doanything.ai","MindPal":"https://mindpal.space","Mem AI":"https://mem.ai","Supernormal":"https://www.supernormal.com"}
}

# HEADER
st.markdown("""<div class="title-box"><div style="font-size:62px; font-weight:900; color:white"><span style="font-size:84px">56</span> FREE AI TOOLS</div><div style="font-size:16px; font-weight:700">EVERY CONTENT CREATOR SHOULD USE IN 2026</div><div style="margin-top:6px; font-size:11px; background:rgba(0,0,0,0.5); display:inline-block; padding:4px 12px; border-radius:20px; letter-spacing:2px">POWERFUL • EASY TO USE • GAME CHANGERS</div></div>""", unsafe_allow_html=True)
st.write("")

# GRID KAYA POSTER
col_left, col_center, col_right = st.columns([1.2, 0.8, 1.2])
with col_left:
  for cat in ["1 AI IMAGE GENERATION","3 AI WRITING & CONTENT","5 AI RESEARCH & STUDY"]:
    st.markdown(f'<div class="category-box"><div style="font-weight:800; font-size:13px; margin-bottom:10px; color:#ffaaaa">{cat}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(tool,link) in enumerate(TOOLS[cat].items()):
        with cols[i%4]:
            st.markdown(f'<div class="tool-link"><a href="{link}" target="_blank">{tool}</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
  st.markdown("""<div class="center-box"><div style="font-size:78px; font-weight:900">56</div><div style="font-size:18px; font-weight:800; background:white; color:#7a0000; border-radius:6px; padding:2px">AI TOOLS</div><div style="margin-top:10px; background:white; color:#7a0000; font-weight:900; border-radius:8px; padding:8px">100% FREE</div><div style="text-align:left; margin-top:14px; font-size:11px">⏰ SAVE TIME<br>💡 BOOST CREATIVITY<br>🚀 INCREASE PRODUCTIVITY<br>🏆 IMPROVE QUALITY<br>📈 STAY AHEAD</div></div>""", unsafe_allow_html=True)

with col_right:
  for cat in ["2 AI VIDEO CREATION","4 AI SOCIAL MEDIA TOOLS","6 AI PRODUCTIVITY & AUTOMATION"]:
    st.markdown(f'<div class="category-box"><div style="font-weight:800; font-size:13px; margin-bottom:10px; color:#ffaaaa">{cat}</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(tool,link) in enumerate(TOOLS[cat].items()):
        with cols[i%4]:
            st.markdown(f'<div class="tool-link"><a href="{link}" target="_blank">{tool}</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- CHAT SECTION DENGAN GEMINI (FIX NotFound) ---
st.subheader("💬 Tanya AI tentang 56 Tools ini")
st.caption("Chat tersimpan, gak ilang kalau refresh. Model: gemini-1.5-flash")

# Tampilkan history chat utama
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

prompt = st.chat_input("Ask about AI tools... Contoh: Tool video terbaik buat pemula apa?")

if prompt:
    if not st.session_state.gemini_key:
        st.error("👈 Masukkin API Key dulu di sidebar kiri!")
        st.stop()
    
    st.session_state.chat_history.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        genai.configure(api_key=st.session_state.gemini_key)
        # FIX UTAMA: ganti dari gemini-pro ke 1.5-flash
        model = genai.GenerativeModel("gemini-1.5-flash")
        context = f"Kamu ahli 56 AI Tools. List tools: {list(TOOLS.keys())}. Jawab singkat membantu. User tanya: {prompt}"
        response = model.generate_content(context)
        
        st.session_state.chat_history.append({"role":"assistant","content":response.text})
        with st.chat_message("assistant"):
            st.write(response.text)
            
    except Exception as e:
        err = str(e)
        if "NotFound" in err or "404" in err:
            st.error("Model error, tapi udah gue fix ke gemini-1.5-flash. Coba lagi.")
        elif "API_KEY" in err:
            st.error("API Key salah / expired. Bikin baru di aistudio.google.com")
        else:
            st.error(f"Error: {err}")

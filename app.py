import json
import os
import time
import uuid
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Konfigurasi dasar
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Free AI Tools 2026",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).with_name("chat_data.json")

DEFAULT_MODEL = "gemini-3.5-flash-lite"
OLD_MODELS = {"gemini-2.5-flash-lite"}  # sudah tidak tersedia -> otomatis dimigrasi

MODEL_OPTIONS = [
    DEFAULT_MODEL,
    "gemini-2.5-flash",
    "Lainnya (ketik manual)",
]

# ---------------------------------------------------------------------------
# Data tools: (nama, url)
# ---------------------------------------------------------------------------
CATEGORIES = [
    (
        1,
        "AI IMAGE GENERATION",
        [
            ("DALL-E 3", "https://openai.com/dall-e-3"),
            ("Midjourney", "https://www.midjourney.com"),
            ("Leonardo AI", "https://leonardo.ai"),
            ("Ideogram", "https://ideogram.ai"),
            ("Recraft AI", "https://www.recraft.ai"),
            ("Adobe Firefly", "https://firefly.adobe.com"),
            ("Playground AI", "https://playground.com"),
            ("Bing Image Creator", "https://www.bing.com/images/create"),
            ("Canva AI", "https://www.canva.com/ai-image-generator/"),
            ("Freepik AI", "https://www.freepik.com/ai"),
            ("Lexica", "https://lexica.art"),
            ("NightCafe", "https://creator.nightcafe.studio"),
            ("Craiyon", "https://www.craiyon.com"),
            ("Fotor AI", "https://www.fotor.com"),
            ("PicLumen", "https://www.piclumen.com"),
            ("DeepAI", "https://deepai.org"),
        ],
    ),
    (
        2,
        "AI VIDEO CREATION",
        [
            ("Runway", "https://runwayml.com"),
            ("Pika Labs", "https://pika.art"),
            ("Kling AI", "https://klingai.com"),
            ("Luma AI", "https://lumalabs.ai"),
            ("Haiper", "https://haiper.ai"),
            ("CapCut AI", "https://www.capcut.com"),
            ("Veo 3", "https://deepmind.google/models/veo/"),
            ("Synthesia", "https://www.synthesia.io"),
            ("Descript", "https://www.descript.com"),
            ("InVideo AI", "https://invideo.io"),
            ("FlexClip", "https://www.flexclip.com"),
            ("Opus Clip", "https://www.opus.pro"),
            ("Filmora AI", "https://filmora.wondershare.com"),
            ("PixVerse", "https://pixverse.ai"),
            ("Steve AI", "https://www.steve.ai"),
            ("Wisecut", "https://www.wisecut.video"),
        ],
    ),
    (
        3,
        "AI WRITING & CONTENT",
        [
            ("ChatGPT", "https://chatgpt.com"),
            ("Claude", "https://claude.ai"),
            ("Gemini", "https://gemini.google.com"),
            ("Perplexity", "https://www.perplexity.ai"),
            ("Notion AI", "https://www.notion.so/product/ai"),
            ("Copy.ai", "https://www.copy.ai"),
            ("Writesonic", "https://writesonic.com"),
            ("Anyword", "https://anyword.com"),
            ("Jasper AI", "https://www.jasper.ai"),
            ("Rytr", "https://rytr.me"),
            ("Wordtune", "https://www.wordtune.com"),
            ("QuillBot", "https://quillbot.com"),
            ("Grammarly", "https://www.grammarly.com"),
            ("Sudowrite", "https://www.sudowrite.com"),
            ("Frase", "https://www.frase.io"),
            ("ContentBot", "https://contentbot.ai"),
        ],
    ),
    (
        4,
        "AI SOCIAL MEDIA TOOLS",
        [
            ("Predis.ai", "https://predis.ai"),
            ("Later AI", "https://later.com"),
            ("Ocoya", "https://www.ocoya.com"),
            ("Buffer AI", "https://buffer.com/ai-assistant"),
            ("Metricool", "https://metricool.com"),
            ("Vista Social", "https://vistasocial.com"),
            ("Lately", "https://www.lately.ai"),
            ("Hootsuite AI", "https://www.hootsuite.com"),
            ("Taplio", "https://taplio.com"),
            ("SocialBee", "https://socialbee.com"),
            ("Typefully", "https://typefully.com"),
            ("TweetHunter", "https://tweethunter.io"),
            ("Brand24", "https://brand24.com"),
            ("Peech", "https://peech.studio"),
            ("Postwise", "https://postwise.ai"),
            ("FeedHive", "https://www.feedhive.com"),
        ],
    ),
    (
        5,
        "AI RESEARCH & STUDY",
        [
            ("Elicit", "https://elicit.com"),
            ("Consensus", "https://consensus.app"),
            ("Scispace", "https://scispace.com"),
            ("ChatPDF", "https://www.chatpdf.com"),
            ("Scholarcy", "https://www.scholarcy.com"),
            ("ResearchRabbit", "https://www.researchrabbit.ai"),
            ("Connected Papers", "https://www.connectedpapers.com"),
            ("Semantic Scholar", "https://www.semanticscholar.org"),
            ("TLDR This", "https://tldrthis.com"),
            ("Humata AI", "https://www.humata.ai"),
            ("Explainpaper", "https://www.explainpaper.com"),
            ("Paperpal", "https://paperpal.com"),
        ],
    ),
    (
        6,
        "AI PRODUCTIVITY & AUTOMATION",
        [
            ("Notion AI", "https://www.notion.so/product/ai"),
            ("ClickUp AI", "https://clickup.com/ai"),
            ("Trello AI", "https://trello.com"),
            ("Coda AI", "https://coda.io/product/ai"),
            ("Motion", "https://www.usemotion.com"),
            ("Otter.ai", "https://otter.ai"),
            ("SaneBox", "https://www.sanebox.com"),
            ("Reclaim AI", "https://reclaim.ai"),
            ("Zapier AI", "https://zapier.com/ai"),
            ("Make", "https://www.make.com"),
            ("Phind", "https://www.phind.com"),
            ("Taskade", "https://www.taskade.com"),
            ("Do Anything Machine", "https://www.doanythingmachine.com"),
            ("MindPal", "https://mindpal.space"),
            ("Mem AI", "https://get.mem.ai"),
            ("Supernormal", "https://www.supernormal.com"),
        ],
    ),
]

BONUS = [
    ("Cleanvoice AI", "https://cleanvoice.ai"),
    ("Bardeen AI", "https://www.bardeen.ai"),
    ("Tome", "https://tome.app"),
    ("Gamma App", "https://gamma.app"),
    ("Miro AI", "https://miro.com/ai/"),
    ("Wave.video", "https://wave.video"),
    ("SlidesAI", "https://www.slidesai.io"),
    ("Synthesia AI", "https://www.synthesia.io"),
    ("Lumen5", "https://lumen5.com"),
]

BENEFITS = [
    ("⏱️", "SAVE TIME", "Automate repetitive tasks and get more done."),
    ("💡", "BOOST CREATIVITY", "Generate ideas, content & designs in seconds."),
    ("🚀", "INCREASE PRODUCTIVITY", "Streamline workflows and stay organized."),
    ("🏅", "IMPROVE QUALITY", "Create high-quality content with AI assistance."),
    ("📈", "STAY AHEAD", "Leverage AI tools and stay ahead in 2026."),
]


def total_tools() -> int:
    names = {n for _, _, tools in CATEGORIES for n, _ in tools}
    names |= {n for n, _ in BONUS}
    return len(names)


# ---------------------------------------------------------------------------
# Penyimpanan (API key + riwayat chat) di chat_data.json
# ---------------------------------------------------------------------------
def default_db() -> dict:
    return {"api_key": "", "model": MODEL_OPTIONS[0], "current": None, "chats": {}}


def load_db() -> dict:
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            base = default_db()
            base.update(data)
            if base.get("model") in OLD_MODELS:
                base["model"] = DEFAULT_MODEL
            return base
        except Exception:
            pass
    return default_db()


def save_db() -> None:
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(st.session_state.db, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(DATA_FILE)


if "db" not in st.session_state:
    st.session_state.db = load_db()
db = st.session_state.db


def new_chat() -> str:
    cid = uuid.uuid4().hex[:10]
    db["chats"][cid] = {"title": "Chat baru", "created": time.time(), "messages": []}
    db["current"] = cid
    save_db()
    return cid


if not db["current"] or db["current"] not in db["chats"]:
    if db["chats"]:
        db["current"] = max(db["chats"], key=lambda k: db["chats"][k]["created"])
    else:
        new_chat()


def get_api_key() -> str:
    if db.get("api_key"):
        return db["api_key"]
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")


# ---------------------------------------------------------------------------
# Gaya (CSS) - tema merah
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 20% 0%, #6e0000 0%, transparent 45%),
        radial-gradient(circle at 90% 30%, #4a0000 0%, transparent 50%),
        linear-gradient(160deg, #1c0000 0%, #3b0000 50%, #120000 100%);
    background-attachment: fixed;
    color: #fff;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2a0000, #140000);
    border-right: 1px solid #ff2a2a55;
}
h1, h2, h3, h4, p, label, span, li, div { color: #fff; }
.block-container { padding-top: 1.5rem; max-width: 1250px; }

.hero {
    border: 2px solid #ff3030; border-radius: 22px; padding: 18px 10px 14px;
    text-align: center; margin-bottom: 18px;
    background: linear-gradient(180deg, #5a0000aa, #2a0000cc);
    box-shadow: 0 0 28px #ff1a1a66, inset 0 0 22px #ff1a1a33;
}
.hero .big {
    font-size: clamp(2.2rem, 6vw, 4.4rem); font-weight: 900; line-height: 1.05;
    letter-spacing: 1px; text-shadow: 0 0 18px #ff4040aa;
}
.hero .big b { color: #fff; font-size: 1.25em; }
.hero .sub { font-weight: 700; letter-spacing: 2px; opacity: .95; margin-top: 4px; }
.hero .chips { margin-top: 10px; display: inline-block; padding: 5px 22px;
    border: 1px solid #ff3030; border-radius: 10px; background: #1a0000;
    font-weight: 700; letter-spacing: 2px; font-size: .85rem; }

.cat {
    border: 1.5px solid #ff2a2a; border-radius: 18px; padding: 12px 12px 10px;
    margin-bottom: 16px;
    background: linear-gradient(180deg, #4a0000bb, #220000dd);
    box-shadow: 0 0 18px #ff1a1a44, inset 0 0 14px #ff1a1a22;
}
.cat-title { display: flex; align-items: center; gap: 10px; font-weight: 800;
    letter-spacing: 1.5px; margin-bottom: 10px; font-size: 1rem; }
.cat-title .num { display: inline-flex; width: 28px; height: 28px; border-radius: 50%;
    background: #e00000; align-items: center; justify-content: center;
    box-shadow: 0 0 10px #ff3030; font-weight: 900; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
a.tile {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 5px; padding: 9px 4px 7px; text-decoration: none !important;
    background: #0d0d0dcc; border: 1px solid #ffffff22; border-radius: 12px;
    transition: all .15s ease; min-height: 78px;
}
a.tile:hover { transform: translateY(-3px); border-color: #ff4040;
    box-shadow: 0 0 14px #ff3030aa; background: #1d0000; }
a.tile img { width: 34px; height: 34px; border-radius: 8px; background: #fff; padding: 3px; }
a.tile span { font-size: .68rem; color: #fff; text-align: center; line-height: 1.1; font-weight: 600; }

.bonus-title { text-align: center; font-weight: 800; letter-spacing: 2px; margin: 4px 0 8px; }
.bonus .grid { grid-template-columns: repeat(9, 1fr); }
.free-box { border: 1.5px solid #ff2a2a; border-radius: 18px; padding: 14px; margin-bottom: 16px;
    background: linear-gradient(180deg, #4a0000bb, #220000dd); text-align: center;
    box-shadow: 0 0 18px #ff1a1a44; }
.free-box .pill { display: inline-block; background: #b30000; border-radius: 10px;
    padding: 6px 28px; font-weight: 900; letter-spacing: 2px; margin-bottom: 12px; }
.benefit { display: flex; gap: 10px; text-align: left; margin: 9px 0; align-items: flex-start; }
.benefit .ic { font-size: 1.4rem; }
.benefit b { display: block; letter-spacing: 1px; font-size: .85rem; }
.benefit small { opacity: .85; }
.save-pin { text-align: center; border: 1.5px solid #ff2a2a; border-radius: 14px;
    padding: 10px; font-weight: 800; letter-spacing: 2px; background: #2a0000cc; }

[data-testid="stChatMessage"] {
    background: #3a0000aa; border: 1px solid #ff2a2a44; border-radius: 14px;
}
[data-testid="stChatInput"] textarea { color: #fff !important; }
.stButton > button {
    background: #8f0000; color: #fff; border: 1px solid #ff3030; border-radius: 10px;
}
.stButton > button:hover { background: #c40000; border-color: #fff; color: #fff; }
.stTabs [data-baseweb="tab"] { font-weight: 700; }
input, textarea { color: #fff !important; }
@media (max-width: 700px) { .bonus .grid { grid-template-columns: repeat(3, 1fr); } }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Komponen HTML direktori
# ---------------------------------------------------------------------------
def tile_html(name: str, url: str) -> str:
    host = urlparse(url).netloc
    icon = f"https://www.google.com/s2/favicons?domain={host}&sz=64"
    return (
        f'<a class="tile" href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
        f'<img src="{icon}" alt="" loading="lazy"><span>{escape(name)}</span></a>'
    )


def category_html(num: int, title: str, tools: list) -> str:
    tiles = "".join(tile_html(n, u) for n, u in tools)
    return (
        f'<div class="cat"><div class="cat-title"><span class="num">{num}</span>'
        f"{escape(title)}</div><div class=\"grid\">{tiles}</div></div>"
    )


def render_directory() -> None:
    count = total_tools()
    st.markdown(
        f'<div class="hero"><div class="big"><b>{count}</b> FREE AI TOOLS</div>'
        '<div class="sub">EVERY CONTENT CREATOR SHOULD USE IN 2026</div>'
        '<div class="chips">POWERFUL &nbsp;•&nbsp; EASY TO USE &nbsp;•&nbsp; GAME CHANGERS</div></div>',
        unsafe_allow_html=True,
    )

    query = st.text_input("🔎 Cari tool", placeholder="mis. video, canva, research ...").strip().lower()

    def filtered(tools):
        if not query:
            return tools
        return [(n, u) for n, u in tools if query in n.lower()]

    left, right = st.columns(2, gap="medium")
    for num, title, tools in CATEGORIES:
        subset = filtered(tools)
        if not subset:
            continue
        target = left if num in (1, 3, 5) else right
        with target:
            st.markdown(category_html(num, title, subset), unsafe_allow_html=True)

    bonus = filtered(BONUS)
    if bonus:
        tiles = "".join(tile_html(n, u) for n, u in bonus)
        st.markdown(
            '<div class="cat bonus"><div class="bonus-title">BONUS TOOLS YOU\'LL LOVE</div>'
            f'<div class="grid">{tiles}</div></div>',
            unsafe_allow_html=True,
        )

    benefits = "".join(
        f'<div class="benefit"><span class="ic">{i}</span><div><b>{escape(t)}</b>'
        f"<small>{escape(d)}</small></div></div>"
        for i, t, d in BENEFITS
    )
    st.markdown(
        f'<div class="free-box"><div class="pill">100% FREE</div>{benefits}</div>'
        '<div class="save-pin">🔖 SAVE THIS PIN FOR LATER — BOOST YOUR CONTENT CREATION WITH AI</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Chat Gemini
# ---------------------------------------------------------------------------
def build_system_prompt() -> str:
    catalog = "; ".join(
        f"{title.title()}: " + ", ".join(n for n, _ in tools)
        for _, title, tools in CATEGORIES
    )
    return (
        "Kamu adalah asisten AI yang cerdas, hangat, jujur, dan teliti, dengan gaya berpikir "
        "seperti Claude.\n\n"
        "Prinsip:\n"
        "- Balas dalam bahasa yang dipakai pengguna (default Bahasa Indonesia yang natural).\n"
        "- Pahami maksud sebenarnya di balik pertanyaan, lalu jawab langsung ke intinya; "
        "jangan bertele-tele dan jangan memberi basa-basi berlebihan.\n"
        "- Untuk masalah rumit, pikirkan langkah demi langkah dan jelaskan alasannya dengan "
        "ringkas. Untuk pertanyaan sederhana, jawab singkat.\n"
        "- Jujur soal ketidakpastian: katakan 'saya tidak yakin' bila memang tidak yakin, "
        "dan jangan mengarang fakta, angka, kutipan, atau tautan.\n"
        "- Berani meluruskan dengan sopan bila ada asumsi yang keliru, tanpa menggurui.\n"
        "- Gunakan format Markdown seperlunya (daftar, tabel, blok kode) agar mudah dibaca; "
        "hindari format berlebihan untuk obrolan santai.\n"
        "- Ajukan paling banyak satu pertanyaan klarifikasi, dan hanya jika benar-benar perlu.\n"
        "- Tolak dengan sopan permintaan yang berbahaya, dan tawarkan alternatif yang aman.\n\n"
        "Konteks aplikasi: pengguna sedang memakai direktori tool AI gratis untuk content creator. "
        "Bila relevan, kamu boleh merekomendasikan tool dari daftar ini (tanpa mengarang tool lain "
        "yang tidak kamu yakini): " + catalog + ". Fitur dan paket gratis tool bisa berubah, "
        "sarankan pengguna mengecek situs resminya."
    )


def stream_reply(api_key: str, model: str, messages: list):
    client = genai.Client(api_key=api_key)
    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]
    config = types.GenerateContentConfig(
        system_instruction=build_system_prompt(),
        temperature=0.7,
    )
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=config
    ):
        if chunk.text:
            yield chunk.text


def sidebar() -> None:
    with st.sidebar:
        st.markdown("## 🔥 Pengaturan")

        key_in = st.text_input(
            "Gemini API Key",
            value=db.get("api_key", ""),
            type="password",
            help="Disimpan lokal di chat_data.json. Dapatkan di aistudio.google.com/apikey",
        )
        if key_in != db.get("api_key", ""):
            db["api_key"] = key_in.strip()
            save_db()
            st.toast("API key tersimpan ✅")

        current_model = db.get("model", MODEL_OPTIONS[0])
        idx = MODEL_OPTIONS.index(current_model) if current_model in MODEL_OPTIONS else len(MODEL_OPTIONS) - 1
        choice = st.selectbox("Model", MODEL_OPTIONS, index=idx)
        if choice == MODEL_OPTIONS[-1]:
            custom = st.text_input(
                "Nama model",
                value="" if current_model in MODEL_OPTIONS else current_model,
                placeholder="mis. gemini-3.5-flash-lite",
            ).strip()
            new_model = custom or MODEL_OPTIONS[0]
        else:
            new_model = choice
        if new_model != db.get("model"):
            db["model"] = new_model
            save_db()

        st.divider()
        if st.button("➕ Chat baru", use_container_width=True):
            new_chat()
            st.rerun()

        st.markdown("#### 💬 Riwayat chat")
        ordered = sorted(db["chats"].items(), key=lambda kv: kv[1]["created"], reverse=True)
        for cid, chat in ordered:
            c1, c2 = st.columns([5, 1])
            label = ("▶ " if cid == db["current"] else "") + chat["title"][:28]
            if c1.button(label, key=f"open_{cid}", use_container_width=True):
                db["current"] = cid
                save_db()
                st.rerun()
            if c2.button("🗑", key=f"del_{cid}"):
                del db["chats"][cid]
                if db["current"] == cid:
                    db["current"] = None
                save_db()
                st.rerun()


def render_chat() -> None:
    chat = db["chats"][db["current"]]
    st.markdown(f"### 💬 {escape(chat['title'])}")

    if not get_api_key():
        st.info("Masukkan Gemini API Key di sidebar untuk mulai chat.")

    for m in chat["messages"]:
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.markdown(m["content"])

    prompt = st.chat_input("Tanya apa saja... (minta ide konten, rekomendasi tool, dll.)")
    if not prompt:
        return

    api_key = get_api_key()
    if not api_key:
        st.error("API key belum diisi.")
        return

    chat["messages"].append({"role": "user", "content": prompt})
    if len(chat["messages"]) == 1:
        chat["title"] = prompt.strip().replace("\n", " ")[:40] or "Chat baru"
    save_db()

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(api_key, db["model"], chat["messages"]))
        except Exception as e:  # noqa: BLE001
            reply = None
            st.error(f"Gagal memanggil Gemini: {e}")

    if reply:
        chat["messages"].append({"role": "assistant", "content": reply})
        save_db()
        st.rerun()
    else:
        # batalkan pesan user terakhir agar riwayat tetap rapi saat error
        chat["messages"].pop()
        save_db()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
sidebar()
tab_dir, tab_chat = st.tabs(["🧰 Direktori AI Tools", "💬 Chat AI (Gemini)"])
with tab_dir:
    render_directory()
with tab_chat:
    render_chat()

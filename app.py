import streamlit as st
import google.generativeai as genai

# Data
data = {
  "title": "56 Free AI Tools Every Content Creator Should Use in 2026",
  "subtitle": "Powerful • Easy to Use • Game Changers",
  "categories": [
    {"id": 1, "name": "AI Image Generation", "tools": ["DALL-E 3", "Midjourney", "Leonardo AI", "Ideogram", "Recraft AI", "Adobe Firefly", "Playground AI", "Bing Image Creator", "Canva AI", "Freepik AI", "Lexica", "NightCafe", "Craiyon", "Fotor AI", "PicLumen", "DeepAI"]},
    {"id": 2, "name": "AI Video Creation", "tools": ["Runway", "Pika Labs", "Kling AI", "Luma AI", "Haiper", "CapCut AI", "Veo 3", "Synthesia", "Descript", "InVideo AI", "FlexClip", "Opus Clip", "Filmora AI", "PixVerse", "Steve AI", "Wisecut"]},
    {"id": 3, "name": "AI Writing & Content", "tools": ["ChatGPT", "Claude", "Gemini", "Perplexity", "Notion AI", "Copy.ai", "Writesonic", "Anyword", "Jasper AI", "Rytr", "Wordtune", "QuillBot", "Grammarly", "Sudowrite", "Frase", "ContentBot"]},
    {"id": 4, "name": "AI Social Media Tools", "tools": ["Predis.ai", "Later AI", "Ocoya", "Buffer AI", "Metricool", "Vista Social", "Lately", "Hootsuite AI", "Taplio", "SocialBee", "Typefully", "TweetHunter", "Brand24", "Peech", "Postwise", "FeedHive"]},
    {"id": 5, "name": "AI Research & Study", "tools": ["Elicit", "Consensus", "Scispace", "ChatPDF", "Scholarcy", "ResearchRabbit", "Connected Papers", "Semantic Scholar", "TLDR This", "Humata AI", "Explainpaper", "Paperpal"]},
    {"id": 6, "name": "AI Productivity & Automation", "tools": ["Notion AI", "ClickUp AI", "Trello AI", "Coda AI", "Motion", "Otter.ai", "SaneBox", "Reclaim AI", "Zapier AI", "Make", "Phind", "Taskade", "Do Anything Machine", "MindPal", "Mem AI", "Supernormal"]},
    {"id": 7, "name": "Bonus Tools You'll Love", "tools": ["Cleanvoice AI", "Bardeen AI", "Tome", "Gamma App", "Miro AI", "Wave.video", "SlidesAI", "Synthesia AI", "Lumen5"]}
  ]
}

# Streamlit App Configuration
st.set_page_config(page_title="56 Free AI Tools 2026", layout="wide")

st.title(data["title"])
st.subheader(data["subtitle"])

# Dashboard Layout
cols = st.columns(3)
for i, category in enumerate(data["categories"]):
    with cols[i % 3]:
        st.write(f"### {category['name']}")
        for tool in category["tools"]:
            st.write(f"- {tool}")

st.divider()

# Chat Assistant (Sidebar)
st.sidebar.title("AI Assistant")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    if prompt := st.chat_input("Ask about AI tools..."):
        st.session_state.messages.append({"role": "user", "text": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "text": response.text})
else:
    st.sidebar.warning("Please enter your Gemini API Key to chat.")

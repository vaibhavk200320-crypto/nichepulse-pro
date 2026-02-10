import streamlit as st
import feedparser
import urllib.parse

# ---------------- 1. PAGE SETUP & STYLING ----------------
st.set_page_config(
    page_title="NichePulse Pro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, professional look
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - dark theme */
    .main {
        background: #1a1a1a;
        background-attachment: fixed;
    }
    
    
    
    /* Sidebar styling - lighter gray */
    [data-testid="stSidebar"] {
        background: #1e1e1e;
        border-right: 1px solid #3a3a3a;
    }
    
    [data-testid="stSidebar"] * {
        color: #e8e8e8 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: #b8b8b8 !important;
        font-weight: 500;
    }
    
    /* Header styling - light text */
    h1 {
        color: #e8e8e8;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h2, h3, h4 {
        color: #d4d4d4;
    }
    
    /* Metrics cards - dark */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #e8e8e8;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] {
        background: #383838;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Buttons - dark theme */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: 1px solid #4a4a4a;
        background: #454545;
        color: #e8e8e8;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        background: #525252;
        border-color: #5a5a5a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* News cards - dark */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: #383838;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border-color: #5a5a5a;
        background: #404040;
    }
    
    /* Text input - dark */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #4a4a4a;
        background: #383838;
        color: #e8e8e8;
        padding: 0.75rem 1rem;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #6a6a6a;
        background: #404040;
        box-shadow: 0 0 0 3px rgba(100, 100, 100, 0.2);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #808080;
    }
    
    .stTextInput label {
        color: #b8b8b8 !important;
    }
    
    /* Link buttons in cards - gray theme */
    .stLinkButton>a {
        background: #525252 !important;
        color: #e8e8e8 !important;
        border: 1px solid #5a5a5a !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
    }
    
    .stLinkButton>a:hover {
        transform: translateY(-2px);
        background: #606060 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Alert boxes - dark */
    .stAlert {
        border-radius: 10px;
        border: 1px solid #4a4a4a;
        background: #383838;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        color: #e8e8e8;
    }
    
    /* Info box in sidebar */
    [data-testid="stSidebar"] .stAlert {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
    }
    
    /* Divider - dark */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #4a4a4a, transparent);
    }
    
    /* Caption text - gray */
    .caption {
        color: #a0a0a0;
        font-size: 14px;
    }
    
    /* All text elements */
    p, span, div {
        color: #d4d4d4;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Expander - dark */
    .streamlit-expanderHeader {
        background: #383838;
        border-radius: 8px;
        font-weight: 600;
        color: #e8e8e8;
    }
    
    .streamlit-expanderHeader:hover {
        background: #404040;
    }
    
    /* Login page specific - dark */
    .login-container {
        background: #2d2d2d;
        padding: 3rem;
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        max-width: 500px;
        margin: 0 auto;
        border: 1px solid #4a4a4a;
    }
    
    /* Pro plan card - dark gray */
    .pro-card {
        background: #383838;
        border: 1px solid #4a4a4a;
        padding: 2rem;
        border-radius: 12px;
        color: #e8e8e8;
        margin: 1rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .pro-card h2, .pro-card h3 {
        color: #f0f0f0;
    }
    
    .pro-card ul li {
        color: #d4d4d4;
    }
    
    /* Article headline - light text */
    .article-headline {
        font-size: 16px;
        font-weight: 600;
        color: #e8e8e8;
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }
    
    /* Article meta - gray text */
    .article-meta {
        display: flex;
        gap: 1rem;
        align-items: center;
        color: #a0a0a0;
        font-size: 13px;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: #383838 !important;
        color: #e8e8e8 !important;
        border: 1px solid #4a4a4a !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #6a6a6a !important;
        background: #404040 !important;
    }
    
    /* Select boxes */
    [data-baseweb="select"] {
        background: #383838;
    }
    
    [data-baseweb="select"] > div {
        background: #383838 !important;
        border-color: #4a4a4a !important;
        color: #e8e8e8 !important;
    }
    
    /* Slider */
    [data-testid="stSlider"] {
        color: #b8b8b8;
    }
    
    .stSlider [role="slider"] {
        background: #6a6a6a;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------- 2. CONSTANTS & CACHING ----------------
FREE_LIMIT = 10

@st.cache_data(ttl=600)
def fetch_news(url):
    return feedparser.parse(url)

# ---------------- 3. SESSION STATE ----------------
if "search_count" not in st.session_state:
    st.session_state.search_count = 0
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "notify_clicks" not in st.session_state:
    st.session_state.notify_clicks = 0

# ---------------- 4. AUTHENTICATION GATE ----------------
if not st.session_state.user_email:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
header {display: none;}
#MainMenu {display: none;}
footer {display: none;}
section.main > div:first-child {
    padding-top: 0rem;
}
</style>
""", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("# 📡 NichePulse Pro")
        st.markdown("### Your intelligent niche research companion")
        st.caption("Monitor trending topics, track emerging stories, and stay ahead of the curve.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Email Address", placeholder="journalist@news.com", label_visibility="collapsed", key="login_email")
        
        if st.button("🚀 Start Researching", use_container_width=True):
            if "@" in email and "." in email:
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("⚠️ Please enter a valid email address.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("🔒 Your email is only used for account identification. We respect your privacy.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------- 5. SIDEBAR (Settings) ----------------
with st.sidebar:
    st.markdown("# ⚙️ Settings")
    st.info(f"👤 **{st.session_state.user_email}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🌍 Region & Time")
    region = st.selectbox("News Region", ["en-IN", "en-US", "en-GB", "en-CA", "en-AU"], 
                          format_func=lambda x: {
                              "en-IN": "🇮🇳 India",
                              "en-US": "🇺🇸 United States",
                              "en-GB": "🇬🇧 United Kingdom",
                              "en-CA": "🇨🇦 Canada",
                              "en-AU": "🇦🇺 Australia"
                          }[x])
    
    timeframe = st.selectbox("Time Range", ["anytime", "1h", "24h", "7d", "30d"],
                            format_func=lambda x: {
                                "anytime": "📅 Any time",
                                "1h": "🕐 Last hour",
                                "24h": "📆 Last 24 hours",
                                "7d": "📊 Last 7 days",
                                "30d": "📈 Last 30 days"
                            }[x])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Display")
    num_articles = st.slider("Articles to show", 4, 30, 10)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------------- 6. HEADER & METRICS ----------------
st.markdown("# 📰 NichePulse Pro")
st.caption("Real-time niche monitoring powered by Google News")
st.markdown("---")

col1, col2, col3 = st.columns(3)
remaining = FREE_LIMIT - st.session_state.search_count

with col1:
    st.markdown("### 🔍 Searches")
    st.progress(st.session_state.search_count / FREE_LIMIT)
    st.caption(f"{remaining} of {FREE_LIMIT} remaining")

with col2:
    st.markdown("### ⏰ Time Range")
    timeframe_display = {
        "anytime": "📅 Any time",
        "1h": "🕐 Last hour",
        "24h": "📆 Last 24 hours",
        "7d": "📊 Last 7 days",
        "30d": "📈 Last 30 days"
    }
    st.caption(timeframe_display.get(timeframe, "Any time"))

with col3:
    region_name = {"IN": "India", "US": "USA", "GB": "UK", "CA": "Canada", "AU": "Australia"}[region.split("-")[1]]
    st.markdown("### 🌍 Region")
    st.caption(region_name)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- 7. MAIN LOGIC ----------------
# 1️⃣ INPUT (keep this as-is)
niche = st.text_input(
    "🔍 What niche are we monitoring today?",
    placeholder="e.g. AI Regulation, Local Elections"
)

# 2️⃣ STOP if empty (prevents rerun bugs)
if not niche:
    st.stop()

# 3️⃣ Detect NEW search
is_new_search = niche.lower().strip() != st.session_state.last_query.lower().strip()

# 4️⃣ 🔒 PAYWALL — PUT YOUR PAY CODE HERE
if is_new_search and st.session_state.search_count >= FREE_LIMIT:
    st.error("🚫 You've reached today's free search limit")

    st.markdown("""
    ## 🚀 Upgrade to Pro
    You've used all **10 free searches today**.

    **Pro includes**
    - Unlimited searches
    - Advanced region filters
    - Priority features
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.button("💎 Pro • ₹139 / month", use_container_width=True)
    with c2:
        st.button("🎁 3 months • ₹399", use_container_width=True)

    if st.button("🔔 Notify me when Pro launches", use_container_width=True):
        st.success(f"We’ll notify {st.session_state.user_email}")

    st.stop()  # ⛔ NOTHING below should run

# 5️⃣ COUNT SEARCH (ONLY AFTER PAYWALL)
if is_new_search:
    st.session_state.search_count += 1
    st.session_state.last_query = niche

# 6️⃣ NOW build query & fetch articles
query = niche
encoded = urllib.parse.quote(query)
hl, gl = region.split("-")
rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

feed = fetch_news(rss_url)


with st.spinner(f"🔍 Scanning for '{niche}'..."):
        feed = fetch_news(rss_url)

        if feed.entries:
            total_found = len(feed.entries)
            shown = min(total_found, num_articles)

            st.success(f"📰 Found **{total_found}** articles • Showing {shown}")
            st.markdown("<br>", unsafe_allow_html=True)

            col_count = 2 if shown > 1 else 1
            cols = st.columns(col_count)

            for i, item in enumerate(feed.entries[:shown]):
                with cols[i % col_count]:
                    with st.container(border=True):
                        parts = item.title.rsplit(" - ", 1)
                        headline = parts[0]
                        source = parts[1] if len(parts) > 1 else "Unknown Source"
                        pub_date = item.published[:16] if hasattr(item, 'published') else "Unknown date"

                        st.markdown(
                            f'<div style="font-weight:600;font-size:16px;">{headline}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<div style="opacity:0.8;">📍 {source} • 🕒 {pub_date}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown("<br>", unsafe_allow_html=True)

                        st.link_button("📖 Read Full Article", item.link, use_container_width=True)
                        st.button("✨ Summarize (Pro)", key=f"sum_{i}", disabled=True)
        else:
            st.warning("🔍 No articles found. Try broader keywords or a different region.")

# ---------------- 8. FOOTER / FEEDBACK ----------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

with st.expander("💬 Share Feedback & Feature Requests"):
    st.markdown("We'd love to hear from you! What features would make NichePulse Pro more valuable?")
    f_text = st.text_area("Your feedback", placeholder="I'd love to see...", label_visibility="collapsed")
    if st.button("📤 Send Feedback", use_container_width=True):
        st.success("✅ Thank you! Your feedback helps us improve NichePulse Pro.")
        st.balloons()

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Made with ❤️ by NichePulse Pro • Version 2.0")




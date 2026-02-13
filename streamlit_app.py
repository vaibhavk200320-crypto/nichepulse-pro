import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, timezone, timedelta

from rapidfuzz import fuzz


def trending_score(group):
    """
    Calculates mentions per hour for a grouped story
    """
    first_seen = min(item["published"] for item in group["sources"])
    hours_alive = max(
        (datetime.now(timezone.utc) - first_seen).total_seconds() / 3600,
        0.25  # prevent division by zero / very small values
    )

    return round(len(group["sources"]) / hours_alive, 2)



def clean_headline(text):
    return text.lower().strip()

def group_articles(articles, threshold=80):
    groups = []

    for art in articles:
        clean_title = clean_headline(art["title"])
        matched = False

        for g in groups:
            score = fuzz.token_set_ratio(clean_title, g["clean_title"])
            if score >= threshold:
                g["sources"].append(art)
                matched = True
                break

        if not matched:
            groups.append({
                "clean_title": clean_title,
                "sources": [art]
            })

    return groups

from datetime import datetime, timezone

def trending_score(group):
    first_seen = min(item["published"] for item in group["sources"])
    
    hours_alive = max(
        (datetime.now(timezone.utc) - first_seen).total_seconds() / 3600,
        0.25  # prevents divide-by-zero
    )

    return round(len(group["sources"]) / hours_alive, 2)

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
    st.stop()

# ---------------- 5. SIDEBAR (Settings) ----------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    timeframe = st.selectbox(
        "Timeframe",
        ["Last 1 hour", "Last 6 hours", "Last 24 hours", "Last 7 days"]
    )

    st.markdown("### Display")
    num_articles = st.slider("Articles to show", 4, 30, 10)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.markdown("### 🌍 Region & Time")
    region = st.selectbox("News Region", ["en-IN", "en-US", "en-GB", "en-CA", "en-AU"], 
                          format_func=lambda x: {
                              "en-IN": "🇮🇳 India",
                              "en-US": "🇺🇸 United States",
                              "en-GB": "🇬🇧 United Kingdom",
                              "en-CA": "🇨🇦 Canada",
                              "en-AU": "🇦🇺 Australia"
                          }[x])

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
    st.caption(timeframe)

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
        st.success(f"We'll notify {st.session_state.user_email}")

    st.stop()  # ⛔ NOTHING below should run

# 5️⃣ COUNT SEARCH (ONLY AFTER PAYWALL)
if is_new_search:
    st.session_state.search_count += 1
    st.session_state.last_query = niche

# 6️⃣ BUILD QUERY & FETCH
query = niche
encoded = urllib.parse.quote(query)
hl, gl = region.split("-")
rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

with st.spinner(f"🔍 Scanning for '{niche}'..."):
    feed = fetch_news(rss_url)

# 7️⃣ FILTER ONLY FRESH NEWS
TIME_RANGES = {
    "Last 1 hour": 1,
    "Last 6 hours": 6,
    "Last 24 hours": 24,
    "Last 7 days": 168,
}

MAX_AGE_HOURS = TIME_RANGES.get(timeframe, 24)

fresh_articles = []
now = datetime.now(timezone.utc)

for e in feed.entries:
    if not hasattr(e, "published_parsed"):
        continue

    published = datetime(*e.published_parsed[:6], tzinfo=timezone.utc)

    if now - published > timedelta(hours=MAX_AGE_HOURS):
        continue

    fresh_articles.append({
        "title": e.title,
        "link": e.link,
        "source": e.source.title if hasattr(e, "source") else "Unknown",
        "published": published
    })

if not fresh_articles:
    st.warning(f"🕒 No fresh news in the selected timeframe ({timeframe}).")
    st.stop()

# 8️⃣ GROUP FRESH NEWS ONLY
groups = group_articles(fresh_articles)

groups = sorted(
    groups,
    key=lambda g: trending_score(g),
    reverse=True
)

high_priority = []
low_priority = []

for g in groups:
    score = trending_score(g)

    # Low signal logic
    if len(g["sources"]) == 1 and score < 0.5:
        low_priority.append(g)
    else:
        high_priority.append(g)


if not groups:
    st.warning("🕒 No fresh stories for this time range.")
    st.stop()

# 🔥 Sort by trending score
groups = sorted(
    groups,
    key=lambda g: trending_score(g),
    reverse=True
)

high_priority = []
low_priority = []

for g in groups:
    score = trending_score(g)

    if len(g["sources"]) == 1 and score < 0.5:
        low_priority.append(g)
    else:
        high_priority.append(g)

tab1, tab2 = st.tabs(["🔥 Trending", "⚪ Low Signal"])

# 🔥 Trending Tab
with tab1:
    if not high_priority:
        st.info("No trending stories right now.")
    else:
        cols = st.columns(2)

        for i, g in enumerate(high_priority[:num_articles]):
            main = g["sources"][0]
            source_count = len(g["sources"])
            score = trending_score(g)

            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"**{main['title']}**")

                    if score >= 2:
                        st.caption(f"🔥 Trending • {score} mentions/hr")
                    elif score >= 0.8:
                        st.caption(f"📈 Rising • {score} mentions/hr")
                    else:
                        st.caption(f"🟢 Developing • {score} mentions/hr")

                    st.caption(
                        f"📍 {main['source']} • 🕒 {main['published'].strftime('%H:%M')}"
                    )

                    st.link_button(
                        "Read Article",
                        main["link"],
                        use_container_width=True
                    )

                    if source_count > 1:
                        with st.expander(f"View {source_count - 1} more sources"):
                            for extra in g["sources"][1:]:
                                st.markdown(
                                    f"- [{extra['source']}]({extra['link']})"
                                )

# ⚪ Low Signal Tab
with tab2:
    if not low_priority:
        st.info("No low-signal stories.")
    else:
        for g in low_priority:
            main = g["sources"][0]
            st.markdown(f"• {main['title']}")




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
st.caption("Made with ❤️ by NichePulse Pro • Version 2")





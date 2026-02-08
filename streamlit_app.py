import streamlit as st
import feedparser
import urllib.parse

# ---------------- 1. PAGE SETUP & STYLING ----------------
st.set_page_config(
    page_title="NichePulse Pro",
    page_icon="📡",
    layout="wide"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; }
    .st-expander { border: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- 2. CONSTANTS & CACHING ----------------
FREE_LIMIT = 10

@st.cache_data(ttl=600)  # Remembers results for 10 mins to save speed/API calls
def fetch_news(url):
    return feedparser.parse(url)

# ---------------- 3. SESSION STATE ----------------
if "search_count" not in st.session_state:
    st.session_state.search_count = 0
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# ---------------- 4. AUTHENTICATION GATE ----------------
if not st.session_state.user_email:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.header("📡 NichePulse Pro")
        st.caption("Enter your email to access the research dashboard.")
        email = st.text_input("Email Address", placeholder="journalist@news.com")
        if st.button("Start Researching"):
            if "@" in email and "." in email:
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Please enter a valid email.")
    st.stop()

# ---------------- 5. SIDEBAR (Settings) ----------------
with st.sidebar:
    st.title("📡 Settings")
    st.info(f"User: {st.session_state.user_email}")
    
    st.divider()
    region = st.selectbox("Region", ["en-US", "en-IN", "en-GB", "en-CA", "en-AU"])
    timeframe = st.selectbox("Recency", ["anytime", "1h", "24h", "7d", "30d"])
    num_articles = st.slider("Articles per view", 4, 30, 10)
    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- 6. HEADER & METRICS ----------------
st.title("📰 NichePulse Pro")
st.markdown("---")

col1, col2, col3 = st.columns(3)
remaining = FREE_LIMIT - st.session_state.search_count

col1.metric("Searches Used", f"{st.session_state.search_count} / {FREE_LIMIT}")
col2.metric("Current Region", region.split("-")[1])
col3.metric("Account Type", "Free Beta" if remaining > 0 else "Limit Reached")

# ---------------- 7. SEARCH INPUT ----------------
niche = st.text_input("🔍 What niche are we monitoring today?", placeholder="e.g. 'Solid State Batteries' or 'Local Elections'")

# ---------------- 8. MAIN LOGIC ----------------
if niche:
    # Check Limit
    if st.session_state.search_count >= FREE_LIMIT:
        st.error("🚨 **Search Limit Reached.** Upgrade to Pro for unlimited daily searches.")
        if st.button("Get Notified for Pro Launch"):
            st.toast("We've added you to the waitlist!", icon="📧")
    else:
        # Build Query with recency filter
        query = niche
        if timeframe != "anytime":
            query += f" when:{timeframe}"
            
        encoded = urllib.parse.quote(query)
        hl, gl = region.split("-")
        rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

        with st.spinner(f"Scanning for '{niche}'..."):
            feed = fetch_news(rss_url)
            
            # Count only if it's a new search term
            if niche.lower() != st.session_state.last_query.lower():
                st.session_state.search_count += 1
                st.session_state.last_query = niche

            if feed.entries:
                # Layout results in a clean 2-column grid
                grid = st.columns(2)
                for i, item in enumerate(feed.entries[:num_articles]):
                    with grid[i % 2]:
                        with st.container(border=True):
                            # Advanced Parsing: rsplit from right keeps hyphenated headlines intact
                            parts = item.title.rsplit(" - ", 1)
                            headline = parts[0]
                            source = parts[1] if len(parts) > 1 else "Unknown Source"
                            
                            st.markdown(f"**{headline}**")
                            st.caption(f"📍 {source} | 🕒 {item.published[:16]}")
                            st.link_button("Read Source", item.link, use_container_width=True)
            else:
                st.warning("No articles found for this specific query. Try a broader keyword.")

# ---------------- 9. FOOTER / FEEDBACK ----------------
st.divider()
with st.expander("💬 Feedback & Feature Requests"):
    f_text = st.text_area("What else do you need for your niche research?")
    if st.button("Send Feedback"):
        st.success("Feedback received! We're building this for you.")



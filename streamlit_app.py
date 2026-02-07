import streamlit as st
import feedparser
import urllib.parse

# ---------------- SESSION STATE INIT ----------------
if "search_count" not in st.session_state:
    st.session_state.search_count = 0

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "notify_clicks" not in st.session_state:
    st.session_state.notify_clicks = 0

FREE_LIMIT = 10


# ---------------- CONFIG ----------------
st.set_page_config(page_title="NichePulse Pro", page_icon="📡", layout="wide")

# ---------------- FREE USAGE TRACKING ----------------
# ---------------- FREE USAGE TRACKING ----------------
if "search_count" not in st.session_state:
    st.session_state.search_count = 0

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

FREE_LIMIT = 10


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📡 NichePulse Pro")
    if st.session_state.user_email:
        st.success(f"Logged in: {st.session_state.user_email}")
        if st.button("Logout"):
            st.session_state.user_email = None
            st.session_state.search_count = 0
            st.rerun()
    st.divider()
    brand_name = st.text_input("Brand Identity", "NichePulse AI")
    num_articles = st.slider("Articles per search", 5, 20, 10)
    language = st.selectbox("Region", ["en-IN", "en-US", "hi-IN"])

# ---------------- LOGIN BLOCK ----------------
if not st.session_state.user_email:
    st.title(f"🚀 {brand_name}")
    st.subheader("Real-time Niche News Discovery")
    
    with st.expander("🔐 Login to continue", expanded=True):
        email = st.text_input("Enter your email")
        if st.button("Continue"):
            if "@" in email:
                st.session_state.user_email = email
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Please enter a valid email")
    st.stop() # Stops the rest of the app from running until login

# ---------------- MAIN UI ----------------
st.title(f"🚀 {brand_name}")
st.progress(st.session_state.search_count / FREE_LIMIT)
st.caption(f"{FREE_LIMIT - st.session_state.search_count} free searches remaining")

niche = st.text_input(
    "🔍 Search niche or topic",
    placeholder="e.g. AI, Electric Vehicles, Local Elections"
)



# ---------------- SEARCH LOGIC ----------------
if niche.strip():

    # ----- LIMIT CHECK -----
    if st.session_state.search_count >= FREE_LIMIT:
        st.error("🚀 Free limit reached")

        st.markdown("""
        ### Pro access required
        You’ve used all **10 free searches**.

        **Pro includes:**
        - Unlimited niche & local searches
        - No daily limits
        - Faster discovery
        """)

        if st.button("🔔 Notify me when Pro launches"):
            st.session_state.notify_clicks += 1
            st.success("✅ Thanks! You’ll be notified.")

        st.caption(f"📧 Notification will be sent to: {st.session_state.user_email}")

        # ---- REVIEW BOX ----
        st.divider()
        st.subheader("💬 Help us improve")

        review = st.text_area(
            "What would make this tool more useful for you?",
            placeholder="Example: more local sources, filters, alerts..."
        )

        if st.button("Submit feedback"):
            if review.strip():
                st.success("🙏 Thanks for your feedback!")
            else:
                st.warning("Please write something before submitting.")

        st.stop()

    # ----- SAFE COUNT (new keyword only) -----
    if niche != st.session_state.last_query:
        st.session_state.search_count += 1
        st.session_state.last_query = niche

    # ----- FETCH NEWS -----
    encoded = urllib.parse.quote(niche)
    hl, gl = language.split("-")

    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

    with st.spinner("Fetching trending articles..."):
        feed = feedparser.parse(rss_url)

        if feed.entries:
            cols = st.columns(2)
            for idx, item in enumerate(feed.entries[:num_articles]):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.subheader(item.title.split("-")[0])
                        st.caption(f"{item.source.title} | {item.published[:16]}")
                        st.link_button("Read Article", item.link, use_container_width=True)
        else:
            st.warning("No articles found. Try a different keyword.")


    # ---- REVIEW BOX (INSIDE LIMIT VIEW) ----
    st.divider()
    st.subheader("💬 Help us improve")

    review = st.text_area(
        "What would make this tool more useful for you?",
        placeholder="Example: more local sources, filters, alerts..."
    )

    if st.button("Submit feedback"):
        if review.strip():
            st.success("🙏 Thanks for your feedback!")
        else:
            st.warning("Please write something before submitting.")

    st.stop()



    # ----- SAFE COUNT (new query only) -----
    if niche != st.session_state.last_query:
        st.session_state.search_count += 1
        st.session_state.last_query = niche

    # ----- FETCH NEWS -----
    encoded = urllib.parse.quote(niche)
    hl, gl = language.split("-")

    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

    with st.spinner("Fetching trending articles..."):
        feed = feedparser.parse(rss_url)

        if feed.entries:
            cols = st.columns(2)
            for idx, item in enumerate(feed.entries[:num_articles]):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.subheader(item.title.split("-")[0])
                        st.caption(f"{item.source.title} | {item.published[:16]}")
                        st.link_button("Read Article", item.link, use_container_width=True)
        else:
            st.warning("No articles found. Try a different keyword.")


   
    # 2. Limit Protection (Soft Paywall)
if st.session_state.search_count >= FREE_LIMIT:
    st.error("🚀 Free limit reached")

    st.markdown("""
    ### Pro access required
    You’ve used all **10 free searches**.

    **Pro includes:**
    - Unlimited niche & local searches
    - No daily limits
    - Faster discovery

    💡 Pro access is launching soon.
    """)

    if st.button("🔔 Notify me when Pro launches"):
        st.session_state.notify_clicks += 1
        st.success("✅ Thanks! You’ll be notified.")

    st.caption(f"📧 Notification will be sent to: {st.session_state.user_email}")

    st.stop()


    # 3. Execution
    if niche.strip():
       
        st.session_state.last_query = niche

    
    encoded = urllib.parse.quote(niche)
    hl = language.split('-')[0]
    gl = language.split('-')[1] if '-' in language else "IN"
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={gl}:{hl}"

    with st.spinner("Fetching trending articles..."):
        feed = feedparser.parse(rss_url)
        if feed.entries:
            cols = st.columns(2)
            for idx, item in enumerate(feed.entries[:num_articles]):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.subheader(item.title.split("-")[0])
                        st.caption(f"🏢 {item.source.title} | 📅 {item.published[:16]}")
                        st.link_button("Read Article", item.link, use_container_width=True)
        else:
            st.warning("No articles found. Try a different niche.")

        
# ---------------- BOTTOM: FEEDBACK & INTEREST ----------------

st.divider()

st.subheader("💬 Help us improve NichePulse")

# Review / Feedback
review = st.text_area(
    "What would make this tool more useful for you?",
    placeholder="Example: more local sources, filters, alerts, summaries..."
)

if st.button("Submit feedback"):
    if review.strip():
        st.success("🙏 Thanks for your feedback!")
    else:
        st.warning("Please write something before submitting.")

st.divider()

# Notify interest (only show if user hit limit earlier)
st.subheader("🚀 Pro Access")

st.markdown("""
Pro access is launching soon.

**Pro will include:**
- Unlimited searches
- No usage limits
- Faster discovery
""")

if st.button("🔔 Notify me when Pro launches"):
    st.session_state.notify_clicks += 1
    st.success("✅ Thanks! You’re on the early access list.")

st.caption(f"📧 We’ll notify: {st.session_state.user_email}")


st.caption(f"🔥 Pro interest clicks: {st.session_state.notify_clicks}")


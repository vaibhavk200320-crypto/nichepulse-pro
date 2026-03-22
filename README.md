# 📡 NichePulse Pro

> **Real-time niche topic monitoring powered by Google News**

NichePulse Pro is a Streamlit web app that helps journalists, researchers, and content creators track trending stories across any niche — in real time. Enter any topic, pick your region and timeframe, and instantly see which stories are gaining momentum, ranked by velocity.

---

## 🌐 Live Demo

👉 [Open NichePulse Pro](https://nichepulse-pro-zgsivr8nargja7ubtgko8q.streamlit.app/)

---

## ✨ Features

- 🔍 **Niche Search** — Monitor any topic or keyword using live Google News RSS feeds
- 🔥 **Trending Score** — Stories are ranked by *mentions per hour*, so you always see what's gaining traction fastest
- 📰 **Smart Story Grouping** — Duplicate and near-duplicate headlines are grouped using fuzzy matching (RapidFuzz), so you see unique stories instead of noise
- ⏱️ **Time Filters** — Filter results by Last 1 Hour, 6 Hours, 24 Hours, or 7 Days
- 🌍 **Multi-Region Support** — Switch between India 🇮🇳, USA 🇺🇸, UK 🇬🇧, Canada 🇨🇦, and Australia 🇦🇺
- 🗂️ **Two-Tab View** — Separate **Trending** and **Low Signal** tabs to distinguish breaking stories from slow-moving ones
- 💬 **Feedback Panel** — Built-in feedback form for feature requests
- 🔒 **Email Auth Gate** — Lightweight email-based login for user identification
- 🚀 **Freemium Paywall** — 10 free searches per session with an upgrade prompt for Pro

---

## 🖥️ Demo

| Trending Tab | Low Signal Tab |
|---|---|
| 🔥 Stories with 2+ mentions/hr | ⚪ Single-source, slow-moving items |
| 📈 Rising stories (0.8–2/hr) | Listed for completeness |
| 🟢 Developing stories (<0.8/hr) | |

---

## 🚀 Getting Started

### Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/your-username/nichepulse-pro.git
cd nichepulse-pro
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 📦 Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | UI framework |
| [feedparser](https://feedparser.readthedocs.io) | Google News RSS parsing |
| [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) | Fuzzy headline deduplication |
| Python `urllib` | URL encoding for search queries |

---

## 📁 Project Structure

```
nichepulse-pro/
├── streamlit_app.py       # Main application
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Configuration

| Constant | Default | Description |
|---|---|---|
| `FREE_LIMIT` | `10` | Max free searches per session |
| `ttl` (cache) | `600s` | News feed cache duration |
| Fuzzy threshold | `80` | Minimum similarity score to group headlines |

---

## 🛣️ Roadmap

- [ ] Email notifications for breaking stories
- [ ] Unlimited searches (Pro tier)
- [ ] Advanced region + language filters
- [ ] Export results to CSV
- [ ] Scheduled monitoring / alerts

---

## 💬 Feedback

Use the in-app feedback panel or open a GitHub Issue. Feature requests are welcome!

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">Made with ❤️ by NichePulse Pro • Version 2</p>

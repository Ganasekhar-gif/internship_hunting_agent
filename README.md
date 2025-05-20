# 🤖 Internship Hunting Agent 🚀

An intelligent automation system to **search**, **filter**, and **notify** users about the most relevant tech internships and open-source programs from multiple platforms using **Python**, **Web Scraping**, and **LLaMA 3 AI Agent**.  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup%20%7C%20Requests-yellowgreen)
![AI Agent](https://img.shields.io/badge/AI-Agent%20%7C%20LLaMA3-green)
![Email](https://img.shields.io/badge/Email-Alerts-orange)
![Automation](https://img.shields.io/badge/Automation-Cron%20%7C%20CLI-informational)

---

## 🧠 Features

- 🔍 Scrapes internship and open-source listings from:
  - [LinkedIn](https://www.linkedin.com)
  - [Internshala](https://internshala.com)
  - [Naukri](https://naukri.com)
  - [AngelList](https://angel.co)
  - [HackerEarth](https://hackerearth.com)
  - [YCombinator](https://www.ycombinator.com)
  - GSoC, MLH Fellowship, KWoC, DWoC, Code4GovTech, and more
- 💡 Intelligent filtering using **LLaMA 3 AI** with a natural language query
- ✉️ Sends the most relevant jobs directly to your inbox
- 🔁 Avoids duplicate alerts using persistent JSON tracking
- ⚙️ Simple CLI interface with `--auto` flag for headless filtering
- 🔐 Environment variable support with `.env` file for email credentials

---

## 📸 Demo

```bash
python main.py --auto --query "remote data science internships"
```

✅ Scraped from 10+ platforms  
✅ Filtered via LLaMA 3 based on your preferences  
✅ Sent top picks to your inbox  
✅ Saved results to `data/filtered_jobs.json`

---

## 📂 Project Structure

```
internship_hunting_agent/
├── scrapers/                   # Scrapers for each platform
│   ├── linkedin.py
│   ├── internshala.py
│   └── ...
├── data/                       # Stores filtered results
├── seen_jobs.json             # Tracks already seen job links
├── send_email.py              # Email utility to send alerts
├── agent.py                   # LLaMA 3 filtering logic
├── main.py                    # Entry point with CLI support
├── .env                       # Email credentials (not committed)
├── requirements.txt           # Project dependencies
└── README.md                  # You’re here!
```

---

## ⚙️ Setup & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ganasekhar-gif/internship_hunting_agent.git
   cd internship_hunting_agent
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file with your email config**:
   ```env
   GROQ_API_KEY=your API key
   GROQ_MODEL=your LLM model
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   RECEIVER_EMAIL=your_email@gmail.com
   ```

5. **Run the agent**:
   ```bash
   python main.py --auto --query "remote AI internships"
   ```

---

## 🌟 Highlights

- ✅ AI-powered job filtering for **highly relevant results**
- ✅ Automates tedious internship searching with a single command
- ✅ Real-world project built using **scraping, automation, and AI**
- ✅ Ideal for students, early professionals & open-source contributors
- ✅ Extendable architecture for more platforms and notification methods

---

## 💡 Future Enhancements

- 🌐 Web-based dashboard (Flask/Streamlit)
- 📅 Weekly curated email newsletter
- 📊 Dashboard for job analytics & trends
- 🤖 Telegram/Discord bot integration

---

## 📈 Real-World Impact

This project empowers students and professionals by saving **hours of manual internship hunting**, filtering out noise, and delivering high-quality, relevant opportunities. By integrating AI, it understands your intent and curates listings just for **you**.

---

## 🙋‍♂️ Author

**Ganasekhar Kalla**  
3rd Year ECE @ NIT Nagaland  
📫 [LinkedIn](https://www.linkedin.com/in/ganasekhark) | [GitHub](https://github.com/Ganasekhar-gif)

---

## ⭐️ Support & Contribution

If you find this useful, consider giving it a ⭐️ and sharing it with your peers.  
Pull requests and suggestions are welcome!

> Empower your internship search with automation and AI.

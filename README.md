<div align="center">

# 💧 HydraAgent

### Agentic AI for Smart Hydration Monitoring 

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **HydraAgent** is not just a water tracker.
> It is an **autonomous AI agent** that perceives your hydration behavior,
> reasons over your intake data, and acts by delivering intelligent,
> personalized health guidance — in real time.

<br/>

![HydraAgent Banner](https://img.shields.io/badge/🤖_Agentic_AI-Perception_→_Reasoning_→_Action-0d6efd?style=for-the-badge)

</div>

---

## 🌟 What Makes HydraAgent "Agentic"?

Most hydration apps just **store numbers**.
HydraAgent does something fundamentally different — it runs an **AI agent loop**:

```

╔══════════════════════════════════════════════════════════════╗
║                    🤖 HydraAgent Loop                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   👤 User logs water intake                                 ║
║         │                                                    ║
║         ▼                                                    ║
║   📡 PERCEIVE — Agent receives user_id and intake_ml        ║
║         │                                                    ║
║         ▼                                                    ║
║   🧠 REASON  — LLaMA 3.1 analyzes hydration context         ║
║         │      • How much water has been consumed?           ║
║         │      • Is the daily goal being met?                ║
║         │      • What is the next best action?               ║
║         │                                                    ║
║         ▼                                                    ║
║   ⚡ ACT     — Agent provides personalized guidance          ║
║         │      • Hydration status assessment                 ║
║         │      • Actionable next steps                       ║
║         │      • Health-aware suggestions                    ║
║         │                                                    ║
║         ▼                                                    ║
║   💾 MEMORY  — SQLite stores intake history for context      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

This **Perception → Reasoning → Action → Memory** loop is the foundation of agentic AI — and HydraAgent implements it fully for smart hydration monitoring.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Autonomous AI Agent** | `WaterIntakeAgent` powered by LLaMA 3.1 8B via Groq |
| 📊 **Live Dashboard** | Beautiful real-time UI with wave animations & bar charts |
| 📅 **Week / Month / Year** | Full historical hydration tracking across all time ranges |
| ⚡ **Instant AI Analysis** | Real-time agent feedback on every intake log |
| 💾 **Persistent Memory** | SQLite stores full history — agent context grows over time |
| 🎯 **Smart Goal Tracking** | Daily 2,500ml goal with streak detection |
| 🔒 **Secure by Design** | API keys in `.env`, never committed to version control |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      HydraAgent System                  │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Frontend │───▶│   FastAPI    │───▶│ WaterIntake  │  │
│  │Dashboard │    │   api.py     │    │   Agent 🤖    │  │
│  │  (.html) │◀───│              │◀───│  (agent.py)  │  │
│  └──────────┘    └──────┬───────┘    └───────┬───────┘  │
│                         │                    │          │
│                  ┌──────▼───────┐    ┌───────▼───────┐  │
│                  │   SQLite DB  │    │  Groq API     │  │
│                  │ database.py  │    │ LLaMA 3.1 8B  │  │
│                  │ (memory)     │    │ (reasoning)   │  │
│                  └──────────────┘    └───────────────┘  │
│                                                         │
│                  ┌──────────────┐                       │
│                  │  logger.py   │  (observability)      │
│                  └──────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
HydraAgent/
├── src/
│   ├── 🤖 agent.py                       # Core AI agent — WaterIntakeAgent
│   ├── 🌐 api.py                         # FastAPI — routes & agent orchestration
│   ├── 🗄  database.py                   # SQLite — agent memory & history
│   ├── 📋 logger.py                      # Structured logging & observability
│   ├── 🎨 water_tracker_dashboard.html   # Live frontend dashboard
│   └── 📄 app.log                        # Agent activity logs
├── .env                                  # 🔐 Secret keys (NEVER commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Quickstart

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/hydra-agent.git
cd hydra-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Create .env in the root folder
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 4. Start HydraAgent
```bash
cd src
uvicorn api:app --reload
```

### 5. Open the dashboard
```
http://localhost:8000
```

---

## 🚀 API Reference

### `POST /log-intake` — Trigger the agent
```bash
curl -X POST http://localhost:8000/log-intake \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_01", "intake_ml": 500}'
```

**Agent Response:**
```json
{
  "message": "Water intake logged successfully",
  "analysis": "You've consumed 500ml — 20% of your 2,500ml daily goal.
                Your hydration level is low. I recommend drinking 250ml
                every 60 minutes for the next 4 hours to reach your target.
                Proper hydration improves cognitive function by up to 30%."
}
```

### `GET /history/{user_id}` — Retrieve agent memory
```bash
curl http://localhost:8000/history/user_01
```

---

## 🛠 Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| 🤖 **AI Agent** | LLaMA 3.1 8B (Groq) | Reasoning & decision-making |
| 🌐 **Backend** | FastAPI + Python 3.10+ | Agent orchestration & API |
| 🗄 **Memory** | SQLite | Persistent agent history |
| 🎨 **Frontend** | HTML / CSS / JS | Real-time dashboard |
| 📋 **Observability** | Python logging | Agent activity tracking |
| 🔐 **Security** | python-dotenv | Secret management |

---

## 🔮 Roadmap — Future Agentic Capabilities

- [ ] 🔄 **Multi-turn memory** — Agent remembers and references past week's patterns
- [ ] 📅 **Proactive agent** — Scheduled reminders triggered autonomously by the agent
- [ ] 🧩 **Multi-agent system** — Separate specialized agents for analysis, coaching & alerts
- [ ] 📈 **Predictive reasoning** — Agent forecasts end-of-day hydration based on current pace
- [ ] 🌡 **Context-aware agent** — Adjusts goals based on weather, activity & health data
- [ ] 💬 **Conversational agent** — Chat directly with HydraAgent for hydration advice

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 🔒 Security

- **Never commit your `.env` file** — it is blocked by `.gitignore`
- Rotate your Groq API key if accidentally exposed
- Database files (`*.db`) are excluded from version control

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**Built with 💧 + 🤖 — HydraAgent**

*Agentic AI for Smart Hydration Monitoring*

</div>

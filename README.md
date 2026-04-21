<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=T.W.I.N.K.U%20AI&fontSize=90&fontAlignY=35&desc=The%20Ultimate%20Prompt-Powered%20Desktop%20Assistant&descAlignY=60&descAlign=50" alt="TWINKU Banner" />

  <h1>🚀 T.W.I.N.K.U - The AI Desktop Maestro</h1>

  <p>
    <strong>Control your entire Windows ecosystem with your voice, advanced vision, and flawless AI logic.</strong><br>
    <em>Built for the Prompt Wars Hackathon — Where words become system commands!</em>
  </p>

  <p>
    <a href="https://github.com/mihir0804/T.W.I.N.K.U_AI_ASSISTANT"><img src="https://img.shields.io/badge/🏆-Prompt_Wars_Hackathon-FFD700?style=for-the-badge&logo=hackaday" alt="Prompt Wars" /></a>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
    <a href="https://reactjs.org"><img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" /></a>
    <a href="https://microsoft.com/windows"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" /></a>
  </p>
</div>

---

## ⚡ Why T.W.I.N.K.U. Will Win Prompt Wars

In the realm of AI, **prompts are the new source code**. T.W.I.N.K.U isn't just a chatbot; it's an intricate orchestration of **Prompt Engineering, Tool Calling, and System APIs**. 

We didn't just ask the AI to "chat"; we *prompted* it to become an operating system kernel proxy. Through carefully crafted zero-shot and few-shot system prompts, T.W.I.N.K.U securely translates natural language into executable CMD, PowerShell, and UI manipulation commands with zero latency. 

**This is the ultimate intersection of Prompt Engineering and System Automation.**

---

## 🔥 Legendary Features

### 👁️ Computer Vision & Context Awareness
- **Screen Analysis:** TWINKU looks at your screen and knows what you're doing. It can read text, detect errors, and contextually assist without you saying a word.
- **Document Reading:** Point it at a document, and it extracts the data flawlessly.

### 🎙️ Zero-Latency Voice Control
- **Offline Wake Word:** Lightning-fast activation. No more holding buttons.
- **Bidi WebSocket Streaming:** Uses Google's Generative AI over WebSockets for real-time conversational flow and sub-50ms audio chunk streaming. 

### 💻 Deep Windows Integration
- **Universal App Opener:** Win32, UWP, or obscure legacy apps—TWINKU finds and opens them using intelligent alias matching and Start Menu scans.
- **System Automation:** Play media, send WhatsApp messages, create files, manage folders, and convert images to PDF completely hands-free.

### 🧠 Persistent Memory
- Conversations and preferences are securely logged to a local SQLite Database. TWINKU remembers your workspace and learns your habits.

### 🎨 Stunning UI (Jarvis-UI)
- A gorgeous, responsive React + Vite frontend interface featuring beautiful waveform visualizers and real-time conversation display, making you feel like Tony Stark.

---

## 🏗️ Architecture & Tech Stack

| Component | Technology Used |
|-----------|-----------------|
| **AI Brain** | Gemini AI via Bidirectional WebSockets |
| **Backend Core** | Python (asyncio, sounddevice, speech_recognition) |
| **Frontend UI** | React, Vite, Tailwind/Vanilla CSS |
| **System Tools** | PowerShell (`Start-Process`), CMD, Win32 APIs |
| **Memory** | Local SQLite (`twinku_memory.db`) |

---

## 🚀 Quick Start & Installation

Want JARVIS on your PC right now? Here is how to summon T.W.I.N.K.U.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mihir0804/T.W.I.N.K.U_AI_ASSISTANT.git
cd T.W.I.N.K.U_AI_ASSISTANT
```

### 2️⃣ Backend Setup (Python)
```powershell
# Navigate to the Python Core
cd ai0/ai0

# Install dependencies
pip install -r requirements.txt # (Ensure you have pyaudio, websockets, sounddevice, etc.)

# Set your API Key in .env
# RUN THE SYSTEM!
python main.py
```
*(Pro tip: Use `start_twinku.bat` or `start_twinku_silent.pyw` for a seamless launch!)*

### 3️⃣ Frontend Setup (React)
```powershell
# Open a new terminal and navigate to the UI folder
cd jarvis-ui

# Install Node modules
npm install

# Start the beautiful UI
npm run dev
```

---

## 🛡️ The "Prompt" Behind the Magic

T.W.I.N.K.U utilizes an advanced `ARIA_PROMPT` structured to enforce JSON-based tool calling. It binds the LLM's vast knowledge directly to Python functions. 

When you say, *"TWINKU, my code is broken,"* the AI:
1. Triggers the `analyze_screen` vision tool.
2. Identifies the IDE and the stack trace.
3. Streams the solution directly via voice while writing the corrected code.

**Pure prompt perfection.**

---

<div align="center">
  <h3>Built with ❤️ for the Prompt Wars</h3>
  <p>If T.W.I.N.K.U blew your mind, give this repo a ⭐!</p>
</div>

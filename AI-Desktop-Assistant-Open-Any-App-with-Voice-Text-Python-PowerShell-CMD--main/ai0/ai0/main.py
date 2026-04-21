# main.py — TWINKU Edition (Wake Word, Fast Response, Media Tools & STABILITY FIXED)

import asyncio
import base64
import json
import numpy as np
import sounddevice as sd
import websockets
import speech_recognition as sr  # ✅ Offline Wake Word Library
from prompt import ARIA_PROMPT
from app import open_app, play_media, send_whatsapp_message, create_file, create_folder, images_to_pdf, APP_ALIASES
from twinku_websocket import TwinkuBroadcaster
from twinku_memory import log_conversation, recall_memory, save_preference
from twinku_documents import read_document
from twinku_vision import (
    init_vision_system,
    analyze_screen,
    detect_errors_on_screen,
    read_text_on_screen
)
import webbrowser
import datetime
# ── Config ────────────────────────────────────────────────
API_KEY = "AIzaSyD7sBkvhl6NtAlXpSZ2OJJEVC7hZVe2mak" # ⚠️ REPLACE WITH YOUR NEW SECURE KEY
WS_URL  = ("wss://generativelanguage.googleapis.com/ws/"
           "google.ai.generativelanguage.v1beta."
           "GenerativeService.BidiGenerateContent")

MIC_RATE = 16000
SPK_RATE = 24000

# 🟢 STABILITY FIX: Send audio in 50ms chunks so Google doesn't block us for spamming
FRAMES   = int(MIC_RATE * 50 / 1000) 

# ── Tool Declarations ─────────────────────────────────────
OPEN_APP_TOOL = {
    "name": "open_app",
    "description": "Open any application/software on the Boss's PC.",
    "parameters": {
        "type": "object",
        "properties": {
            "app_name": {"type": "string"}
        },
        "required": ["app_name"]
    }
}

PLAY_MEDIA_TOOL = {
    "name": "play_media",
    "description": "Play a specific song, artist, or video on YouTube or Spotify.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "platform": {"type": "string", "enum": ["youtube", "spotify"]}
        },
        "required": ["query", "platform"]
    }
}

SEND_WHATSAPP_TOOL = {
    "name": "send_whatsapp_message",
    "description": "Send a WhatsApp message.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {"type": "string", "description": "The message body to send"}
        },
        "required": ["message"]
    }
}

CREATE_FILE_TOOL = {
    "name": "create_file",
    "description": "Create a new file with optional content at a specific location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location_hint": {"type": "string", "description": "Where to create the file (e.g. 'C drive', 'downloads', 'desktop')"},
            "filename": {"type": "string", "description": "The name of the file to create, including extension (e.g. 'Project NEO.txt')"},
            "content": {"type": "string", "description": "Optional text content to write inside the file"}
        },
        "required": ["location_hint", "filename"]
    }
}

CREATE_FOLDER_TOOL = {
    "name": "create_folder",
    "description": "Create a new folder/directory at a specific location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location_hint": {"type": "string", "description": "Where to create the folder (e.g. 'C drive', 'downloads', 'desktop')"},
            "foldername": {"type": "string", "description": "The name of the new folder"}
        },
        "required": ["location_hint", "foldername"]
    }
}

IMAGES_TO_PDF_TOOL = {
    "name": "images_to_pdf",
    "description": "Combine all images in a specified folder into a single PDF file.",
    "parameters": {
        "type": "object",
        "properties": {
            "location_hint": {"type": "string", "description": "The folder containing the images (e.g. 'downloads', 'desktop')"},
            "output_pdf_name": {"type": "string", "description": "The name of the resulting PDF file (e.g. 'Travel Memories')"}
        },
        "required": ["location_hint", "output_pdf_name"]
    }
}

RECALL_MEMORY_TOOL = {
    "name": "recall_memory",
    "description": "Search the Boss's past conversations and preferences database. Use this strictly when asked to recall past facts, preferences, or conversation details.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search term to look for in memory."}
        },
        "required": ["query"]
    }
}

SAVE_PREFERENCE_TOOL = {
    "name": "save_preference",
    "description": "Store a user preference or hard fact into the database. Use this when the Boss explicitly tells you to remember a particular rule or preference.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "The type of preference (e.g. 'PDF Setting', 'Favorite Color')"},
            "fact": {"type": "string", "description": "The rule or fact to remember."}
        },
        "required": ["category", "fact"]
    }
}

READ_DOCUMENT_TOOL = {
    "name": "read_document",
    "description": "Read the text contents of a PDF, DOCX, or TXT document on the Boss's PC. This extracts the raw text up to 10k characters which you should then analyze and use to answer the Boss's query.",
    "parameters": {
        "type": "object",
        "properties": {
            "location_hint": {"type": "string", "description": "The folder containing the document (e.g. 'downloads', 'C drive', 'desktop')"},
            "filename": {"type": "string", "description": "The name of the file to read (e.g. 'budget.pdf', 'report')"}
        },
        "required": ["location_hint", "filename"]
    }
}

ANALYZE_SCREEN_TOOL = {
    "name": "analyze_screen",
    "description": "Capture and analyze what's currently on the Boss's screen using visual AI. Can answer questions like 'what's on my screen?', 'describe what you see', 'is there an error?'",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Question about the screen (e.g. 'What's on the screen?', 'Describe what you see')"
            },
            "save_screenshot": {
                "type": "boolean",
                "description": "Whether to save the screenshot (default: false)"
            }
        },
        "required": ["query"]
    }
}

DETECT_SCREEN_ERROR_TOOL = {
    "name": "detect_screen_error",
    "description": "Scan the screen specifically for error messages, warnings, or issues. Use when Boss asks if there's an error or what's wrong.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

READ_SCREEN_TEXT_TOOL = {
    "name": "read_screen_text",
    "description": "Extract and read all visible text from the screen (OCR). Use when Boss asks you to read what's on screen.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

# ── Setup ─────────────────────────────────────────────────
SETUP = {
    "setup": {
        "model": "models/gemini-2.5-flash-native-audio-preview-12-2025",
        "generation_config": {
            "temperature": 0.7,
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {"voice_name": "Aoede"}
                }
            }
        },
        "input_audio_transcription":  {},
        "output_audio_transcription": {},
        "system_instruction": {"parts": [{"text": ARIA_PROMPT}]},
        "tools": [{"functionDeclarations": [
            OPEN_APP_TOOL, PLAY_MEDIA_TOOL, SEND_WHATSAPP_TOOL, 
            CREATE_FILE_TOOL, CREATE_FOLDER_TOOL, IMAGES_TO_PDF_TOOL, 
            RECALL_MEMORY_TOOL, SAVE_PREFERENCE_TOOL, READ_DOCUMENT_TOOL,
            ANALYZE_SCREEN_TOOL, DETECT_SCREEN_ERROR_TOOL, READ_SCREEN_TEXT_TOOL
        ]}]
    }
}

def enc(x):
    return json.dumps(x).encode()

# ── Offline Wake Word Function ────────────────────────────
def wait_for_wake_word(broadcaster=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n" + "="*45)
        print("💤 TWINKU is sleeping. Say 'Twinku' or 'Wake up' to call her...")
        print("="*45)
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            if broadcaster:
                broadcaster.broadcast("idle", "💤 Sleeping... Say 'Twinku'")
            try:
                # Listen in short 1-second bursts offline
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                text = r.recognize_google(audio).lower()
                
                # Triggers to wake up
                if "twinku" in text or "twinkle" in text or "wake up" in text or "tinku" in text:
                    print("\n✨ Wake word detected! Booting systems for the Boss...")
                    
                    hour = datetime.datetime.now().hour
                    if 5 <= hour < 12:
                        greeting = "Good morning, Boss!"
                    elif 12 <= hour < 17:
                        greeting = "Good afternoon, Boss!"
                    elif 17 <= hour < 21:
                        greeting = "Good evening, Boss!"
                    else:
                        greeting = "Working late, Boss? I'm here to help."
                        
                    if broadcaster:
                        broadcaster.broadcast("speaking", f"{greeting} Opening JARVIS interface...")
                        
                    # Auto-open JARVIS UI locally
                    jarvis_url = "http://localhost:5173"
                    try:
                        webbrowser.open(jarvis_url)
                        print(f"🌐 Opening JARVIS UI: {jarvis_url}")
                    except Exception as e:
                        print(f"⚠️ Could not auto-open browser: {e}")

                    return
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception:
                pass

# ── Transcripts & App Extraction ──────────────────────────
def get_user_transcript(msg: dict) -> str:
    sc = msg.get("serverContent", {})
    t = sc.get("inputTranscription", {})
    if isinstance(t, dict) and t.get("text", "").strip():
        return t["text"].strip()
    t2 = sc.get("inputTranscript", "")
    if isinstance(t2, str) and t2.strip():
        return t2.strip()
    return ""

def extract_app_name(transcript: str) -> str | None:
    text = transcript.lower().strip()
    TRIGGERS = ["open", "launch", "start", "run", "kholo", "chalao", "shuru karo"]
    KNOWN_APPS = sorted(list(APP_ALIASES.keys()), key=len, reverse=True)
    triggered_text = None
    for trigger in TRIGGERS:
        if trigger in text:
            after = text.split(trigger, 1)[-1].strip()
            for filler in ["please", "kar", "karo", "do", "na", "boss", "twinku"]:
                after = after.replace(filler, "").strip()
            triggered_text = after
            break
    if not triggered_text:
        return None
    for app in KNOWN_APPS:
        if app in triggered_text:
            return app
    words = triggered_text.split()
    return words[0] if words else None


# ── Main TWINKU class ───────────────────────────────────────
class TWINKU:
    def __init__(self):
        self.running = True
        self.session_active = False # Controls the active conversation
        self._ws = None
        self.tool_active = False # Prevents 1008 Policy Violation during tools
        self.mic_muted = False
        
        self.broadcaster = TwinkuBroadcaster()
        self.broadcaster.on_message_callback = self.handle_ws_message
        self.broadcaster.start()
        
        # Initialize Vision System
        try:
            init_vision_system(API_KEY)
            print("👁️ Twinku Vision initialized natively.")
        except Exception as e:
            print(f"⚠️ Twinku Vision failed to initialize: {e}")
        
    def handle_ws_message(self, data):
        if data.get("action") == "toggle_mic":
            # JS state=True means mic-on -> mic_muted=False
            self.mic_muted = not data.get("state", True)
            state_str = "OFF" if self.mic_muted else "ON"
            print(f"\n🎤 UI COMMAND: Microphone successfully toggled {state_str}")

    async def start(self):
        while self.running:
            # 1. Stay offline and wait for wake word
            wait_for_wake_word(self.broadcaster)
            
            # 2. Wake word heard! Start live session
            self.session_active = True
            try:
                await self._session()
            except Exception as e:
                print(f"[TWINKU] Connection dropped: {e}")
                await asyncio.sleep(1)

    async def _session(self):
        self.broadcaster.broadcast("listening", "Connecting to Twinku Core...")
        async with websockets.connect(
            f"{WS_URL}?key={API_KEY}",
            max_size=None,
            ping_interval=20,
            ping_timeout=30,
        ) as ws:
            self._ws = ws
            await ws.send(enc(SETUP))
            await ws.recv()
            print("✅ TWINKU is online and listening to you, Boss.")
            self.broadcaster.broadcast("listening", "Listening to Boss...")

            import queue as _queue
            audio_q   = _queue.Queue()
            play_stop = asyncio.Event()

            def _play_thread():
                BUF = int(SPK_RATE * 0.04)
                buf = np.array([], dtype=np.float32)
                stream = sd.OutputStream(
                    samplerate=SPK_RATE, channels=1,
                    dtype="float32", blocksize=BUF, latency="low" 
                )
                stream.start()
                while not play_stop.is_set():
                    try:
                        chunk = audio_q.get(timeout=0.05) 
                        if chunk is None:
                            continue
                        buf = np.concatenate([buf, chunk])
                        while len(buf) >= BUF:
                            stream.write(buf[:BUF])
                            buf = buf[BUF:]
                    except _queue.Empty:
                        pass
                stream.stop(); stream.close()

            import threading
            play_t = threading.Thread(target=_play_thread, daemon=True)
            play_t.start()

            try:
                await asyncio.gather(
                    self._send_audio(ws),
                    self._recv(ws, audio_q),
                )
            finally:
                self.session_active = False
                play_stop.set()
                audio_q.put(None)
                play_t.join(timeout=2.0)

    async def _send_audio(self, ws):
        with sd.InputStream(
            samplerate=MIC_RATE, channels=1,
            dtype="int16", blocksize=FRAMES, latency="low"
        ) as mic:
            while self.running and self.session_active:
                pcm, _ = mic.read(FRAMES)
                if self.tool_active:
                    await asyncio.sleep(0.01)
                    continue

                if getattr(self, "mic_muted", False):
                    pcm = np.zeros_like(pcm)

                await ws.send(enc({
                    "realtimeInput": {
                        "audio": {
                            "mimeType": "audio/pcm;rate=16000",
                            "data": base64.b64encode(pcm.tobytes()).decode()
                        }
                    }
                }))
                await asyncio.sleep(0.001)

    async def _recv(self, ws, audio_q):
        while self.running and self.session_active:
            try:
                raw = await ws.recv()
                msg = json.loads(raw)
            except websockets.exceptions.ConnectionClosed:
                break

            # ✅ STABILITY FIX: Deep search for Tool Calls + Pause Audio (1008 Error Fix)
            calls_list = msg.get("toolCall", {}).get("functionCalls", [])
            calls = list(calls_list)
            
            # 2. Check inside the model's text turn (Google sometimes hides it here)
            for part in msg.get("serverContent", {}).get("modelTurn", {}).get("parts", []):
                if "functionCall" in part:
                    calls.append(part["functionCall"])

            if calls:
                self.tool_active = True

            # Process any found tool calls
            function_responses = []
            processed_ids = set()

            for call in calls:
                call_id = call.get("id", "")
                if call_id in processed_ids:
                    continue
                processed_ids.add(call_id)
                
                name = call.get("name", "")
                args = call.get("args", {})
                result = ""

                if name == "open_app":
                    app_name = args.get("app_name", "")
                    print(f"🔧 Action: Opening App -> '{app_name}'")
                    self.broadcaster.broadcast("speaking", f"Right away Boss, opening {app_name}...")
                    result = open_app(app_name)
                elif name == "play_media":
                    query = args.get("query", "")
                    platform = args.get("platform", "youtube")
                    print(f"🔧 Action: Playing Media -> '{query}' on {platform}")
                    self.broadcaster.broadcast("speaking", f"Playing {query} on {platform}...")
                    result = play_media(query, platform)
                elif name == "send_whatsapp_message":
                    message_text = args.get("message", "")
                    print(f"🔧 Action: Open WhatsApp to send -> '{message_text}'")
                    self.broadcaster.broadcast("speaking", f"Opening WhatsApp with your message Boss...")
                    result = send_whatsapp_message(message_text)
                elif name == "create_file":
                    loc = args.get("location_hint", "")
                    fname = args.get("filename", "")
                    content = args.get("content", "")
                    print(f"🔧 Action: Create File -> '{fname}' at '{loc}'")
                    self.broadcaster.broadcast("speaking", f"Creating file {fname} for you Boss...")
                    result = create_file(loc, fname, content)
                elif name == "create_folder":
                    loc = args.get("location_hint", "")
                    fname = args.get("foldername", "")
                    print(f"🔧 Action: Create Folder -> '{fname}' at '{loc}'")
                    self.broadcaster.broadcast("speaking", f"Creating folder {fname} for you Boss...")
                    result = create_folder(loc, fname)
                elif name == "images_to_pdf":
                    loc = args.get("location_hint", "")
                    out_pdf = args.get("output_pdf_name", "")
                    print(f"🔧 Action: Images to PDF -> '{out_pdf}' from '{loc}'")
                    self.broadcaster.broadcast("speaking", f"Combining your images into {out_pdf} Boss...")
                    result = images_to_pdf(loc, out_pdf)
                elif name == "recall_memory":
                    query = args.get("query", "")
                    print(f"🔧 Action: Recall Memory -> '{query}'")
                    self.broadcaster.broadcast("speaking", f"Searching my memory for {query}...")
                    result = recall_memory(query)
                elif name == "save_preference":
                    category = args.get("category", "")
                    fact = args.get("fact", "")
                    print(f"🔧 Action: Save Preference -> [{category}] '{fact}'")
                    self.broadcaster.broadcast("speaking", f"Saving that to my memory Boss...")
                    result = save_preference(category, fact)
                elif name == "read_document":
                    loc = args.get("location_hint", "")
                    fname = args.get("filename", "")
                    print(f"🔧 Action: Read Document -> '{fname}' at '{loc}'")
                    self.broadcaster.broadcast("speaking", f"Reading the contents of {fname} for you, Boss...")
                    result = read_document(loc, fname)
                elif name == "analyze_screen":
                    query = args.get("query", "Describe what is on my screen.")
                    save = args.get("save_screenshot", False)
                    print(f"🔧 Action: Analyze Screen -> '{query}'")
                    self.broadcaster.broadcast("speaking", "Looking at your screen, Boss... 👀")
                    result = analyze_screen(query, save)
                elif name == "detect_screen_error":
                    print("🔧 Action: Detect Screen Error")
                    self.broadcaster.broadcast("speaking", "Scanning your screen for errors... 🔍")
                    err = detect_errors_on_screen()
                    if err["has_error"]:
                        result = f"I detected an error:\n{err['message']}"
                    else:
                        result = "No errors detected on your screen, Boss!"
                elif name == "read_screen_text":
                    print("🔧 Action: Read Screen Text (OCR)")
                    self.broadcaster.broadcast("speaking", "Reading all text on your screen... 👓")
                    result = read_text_on_screen()

                if not result:
                    result = "Action completed."

                function_responses.append({
                    "id": call_id,
                    "name": name,
                    "response": {"result": str(result)}
                })

            # Send all tool results back to Gemini in one single package
            if function_responses:
                try:
                    await ws.send(enc({
                        "toolResponse": {
                            "functionResponses": function_responses
                        }
                    }))
                finally:
                    self.tool_active = False
            elif calls:
                self.tool_active = False

            # Transcripts
            transcript = get_user_transcript(msg)
            if transcript:
                text = transcript.lower()
                print(f"🗣️ Boss: {transcript}")
                self.broadcaster.broadcast("listening", f"Boss: {transcript}")
                log_conversation(transcript, "")
                
                # ✅ GO TO SLEEP COMMAND
                if "go to sleep" in text or "sleep twinku" in text or "stop listening" in text:
                    print("💤 TWINKU: As you wish, Boss. Going back to sleep... ❤️")
                    self.broadcaster.broadcast("speaking", "Going back to sleep, Boss... ❤️")
                    self.session_active = False
                    await ws.close()
                    break

                # We rely on the OPEN_APP_TOOL function call for opening apps.
                # Removed the manual string-matching fallback to prevent opening apps twice.
                app_name = extract_app_name(transcript)
                if app_name:
                    print(f"💡 Detected intent to open: {app_name} (Waiting for tool call)")

            # AI Speech processing
            sc = msg.get("serverContent", {})
            aria_text = sc.get("outputTranscription", {})
            twinku_speech_text = ""
            if isinstance(aria_text, dict) and aria_text.get("text", "").strip():
                twinku_speech_text = aria_text['text'].strip()
                
            if not twinku_speech_text:
                for part in sc.get("modelTurn", {}).get("parts", []):
                    if "text" in part:
                        twinku_speech_text += part["text"]

            twinku_speech_text = twinku_speech_text.strip()
            if twinku_speech_text:
                print(f"🤖 TWINKU: {twinku_speech_text}")
                self.broadcaster.broadcast("speaking", f"Twinku: {twinku_speech_text}")
                log_conversation("", twinku_speech_text)

            # Audio output
            for part in sc.get("modelTurn", {}).get("parts", []):
                d = part.get("inlineData")
                if d and "audio/pcm" in d.get("mimeType", ""):
                    raw_bytes = base64.b64decode(d["data"])
                    pcm = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                    try:
                        audio_q.put_nowait(pcm)
                    except Exception:
                        pass

# ── Run ───────────────────────────────────────────────────
VOICE_OPTIONS = {
    "1": {"name": "Aoede", "desc": "Warm & Smooth (Official)"},
    "2": {"name": "Kore", "desc": "Calm & Clear (Official)"},
    "3": {"name": "Leda", "desc": "Professional (Official)"},
    "7": {"name": "Charon", "desc": "Deep & Resonant (Official)"},
    "8": {"name": "Fenrir", "desc": "Energetic & Fast (Official)"},
}

def select_voice():
    print("\n" + "="*45)
    print("🎤 SELECT TWINKU'S VOICE")
    print("="*45)
    for k in ["1", "2", "3", "7", "8"]:
        print(f"  [{k}] {VOICE_OPTIONS[k]['name']:<8} - {VOICE_OPTIONS[k]['desc']}")
    
    choice = input("Enter voice number [Default: 1]: ").strip()
    config = VOICE_OPTIONS.get(choice, VOICE_OPTIONS["1"])
    return config["name"]

if __name__ == "__main__":
    import sys
    if "--startup" in sys.argv:
        selected_voice = VOICE_OPTIONS["1"]["name"]
        print(f"\n✅ Started in Startup Mode. Defaulting TWINKU voice to {selected_voice}...")
    else:
        selected_voice = select_voice()
        
    SETUP["setup"]["generation_config"]["speech_config"]["voice_config"]["prebuilt_voice_config"]["voice_name"] = selected_voice
    print(f"\n✅ Initializing TWINKU with {selected_voice} voice...")
    
    assistant = TWINKU()
    asyncio.run(assistant.start())
import streamlit as st
import google.generativeai as genai
import time
import os
import tempfile
import gc
import io
import hashlib
import asyncio
import struct
import re
import yt_dlp
from PIL import Image

# --- LIBRARY IMPORTS ---
PDF_AVAILABLE, DOCX_AVAILABLE, GDOWN_AVAILABLE, SUPABASE_AVAILABLE, EDGE_TTS_AVAILABLE, GENAI_NEW_AVAILABLE = True, True, True, True, True, True

try: import PyPDF2
except: PDF_AVAILABLE = False
try: from docx import Document
except: DOCX_AVAILABLE = False
try: import gdown
except: GDOWN_AVAILABLE = False
try: from supabase import create_client
except: SUPABASE_AVAILABLE = False
try: import edge_tts
except: EDGE_TTS_AVAILABLE = False
try: from google import genai as genai_new; from google.genai import types
except: GENAI_NEW_AVAILABLE = False

SUPABASE_URL = "https://ohjvgupjocgsirhwuobf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oanZndXBqb2Nnc2lyaHd1b2JmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MzkwMTgsImV4cCI6MjA4MTUxNTAxOH0.oZxQZ6oksjbmEeA_m8c44dG_z5hHLwtgoJssgK2aogI"
supabase = None
if SUPABASE_AVAILABLE:
    try: supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except: SUPABASE_AVAILABLE = False

st.set_page_config(
    page_title="AI Studio Pro", 
    layout="centered", 
    initial_sidebar_state="collapsed",
    page_icon="🎬"
)

# === MODERN GLASSMORPHISM UI ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-dark: #4f46e5;
    --accent: #22d3ee;
    --accent-pink: #f472b6;
    --bg-dark: #0a0a1a;
    --bg-card: rgba(15, 23, 42, 0.8);
    --bg-glass: rgba(255, 255, 255, 0.05);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border-glass: rgba(255, 255, 255, 0.1);
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
}

* {
    font-family: 'Poppins', 'Noto Sans Myanmar', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, var(--bg-dark) 0%, #0f172a 50%, #1e1b4b 100%) !important;
    background-attachment: fixed !important;
}

/* Animated background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(34, 211, 238, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(244, 114, 182, 0.08) 0%, transparent 40%);
    pointer-events: none;
    z-index: 0;
}

header, #MainMenu, footer, [data-testid="stDecoration"] {
    visibility: hidden !important;
    display: none !important;
}

/* Main container */
[data-testid="block-container"] {
    max-width: 100% !important;
    padding: 1rem !important;
    margin: 0 auto !important;
}

@media (min-width: 768px) {
    [data-testid="block-container"] {
        max-width: 900px !important;
        padding: 2rem !important;
    }
}

/* Glass card effect */
.stContainer, [data-testid="stVerticalBlock"] > div[data-testid="element-container"] {
    position: relative;
    z-index: 1;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 20px !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15, 23, 42, 0.6) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--success) 0%, #059669 100%) !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
}

/* Tabs - Modern pill style */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(10px) !important;
    padding: 8px !important;
    border-radius: 16px !important;
    gap: 8px !important;
    border: 1px solid var(--border-glass) !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-secondary) !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    transition: all 0.3s ease !important;
    white-space: nowrap !important;
}

@media (max-width: 600px) {
    .stTabs [data-baseweb="tab"] {
        padding: 8px 12px !important;
        font-size: 12px !important;
    }
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

h1 {
    background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent) 50%, var(--accent-pink) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 2rem !important;
}

@media (max-width: 600px) {
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }
}

p, span, label, div[data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
}

/* Select box */
.stSelectbox > div > div {
    background: rgba(15, 23, 42, 0.6) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
}

[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.6) !important;
    border-color: var(--border-glass) !important;
}

/* File uploader */
div[data-testid="stFileUploader"] section {
    background: rgba(15, 23, 42, 0.4) !important;
    border: 2px dashed var(--border-glass) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stFileUploader"] section:hover {
    border-color: var(--primary) !important;
    background: rgba(99, 102, 241, 0.05) !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-weight: 700 !important;
}

/* Divider */
hr {
    background: linear-gradient(90deg, transparent, var(--border-glass), transparent) !important;
    height: 1px !important;
    border: none !important;
    margin: 1.5rem 0 !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
    border-radius: 10px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-glass) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* Radio buttons */
.stRadio > div {
    gap: 1rem !important;
}

.stRadio > div > label {
    background: var(--bg-glass) !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    border: 1px solid var(--border-glass) !important;
    transition: all 0.3s ease !important;
}

.stRadio > div > label:hover {
    border-color: var(--primary) !important;
}

/* Checkbox */
.stCheckbox > label {
    color: var(--text-secondary) !important;
}

/* Slider */
.stSlider > div > div > div {
    background: var(--primary) !important;
}

/* Info/Warning/Error boxes */
.stAlert {
    background: var(--bg-glass) !important;
    border-radius: 12px !important;
    border-left: 4px solid var(--primary) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
}

/* Custom title styling */
.main-title {
    text-align: center;
    padding: 1rem 0;
}

.main-title h1 {
    margin: 0;
    font-size: 2.5rem !important;
}

.main-title p {
    color: var(--text-secondary);
    margin-top: 0.5rem;
}

/* Card hover effect */
.hover-card {
    transition: all 0.3s ease;
}

.hover-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
}

/* Animated gradient border */
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.gradient-border {
    background: linear-gradient(135deg, var(--primary), var(--accent), var(--accent-pink), var(--primary));
    background-size: 300% 300%;
    animation: gradient-shift 5s ease infinite;
    padding: 2px;
    border-radius: 20px;
}

/* Audio player */
audio {
    width: 100% !important;
    border-radius: 12px !important;
}

/* Number input */
.stNumberInput > div > div > input {
    background: rgba(15, 23, 42, 0.6) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# === HELPER FUNCTIONS ===
def parse_mime(m):
    b, r = 16, 24000
    for p in m.split(";"):
        p = p.strip()
        if p.lower().startswith("rate="):
            r = int(p.split("=")[1])
        elif p.startswith("audio/L"):
            b = int(p.split("L")[1])
    return b, r

def to_wav(d, m):
    b, r = parse_mime(m)
    h = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36+len(d), b"WAVE", b"fmt ", 16, 1, 1, r, r*b//8, b//8, b, b"data", len(d))
    return h + d

def get_hash(k): 
    return hashlib.sha256(k.encode()).hexdigest()[:32]

def cleanup(): 
    gc.collect()

def get_text(r):
    try:
        if not r or not r.candidates:
            return None, "No response"
        parts = r.candidates[0].content.parts if hasattr(r.candidates[0], 'content') else []
        t = "\n".join([p.text for p in parts if hasattr(p, 'text') and p.text])
        return (t, None) if t else (None, "No text")
    except Exception as e:
        return None, str(e)

def call_api(m, c, to=900):
    for i in range(3):
        try:
            r = m.generate_content(c, request_options={"timeout": to})
            t, e = get_text(r)
            if t:
                return r, None
            if i < 2:
                time.sleep(10)
        except Exception as e:
            if any(x in str(e).lower() for x in ['rate', 'quota', '429']):
                if i < 2:
                    time.sleep(10 * (2**i))
                else:
                    return None, "Rate limit - Please try again later"
            else:
                return None, str(e)
    return None, "Max retries exceeded"

def upload_gem(p, s=None):
    try:
        if s:
            s.info(f"📤 Uploading ({os.path.getsize(p)/(1024*1024):.1f}MB)...")
        f = genai.upload_file(p)
        w = 0
        while f.state.name == "PROCESSING":
            w += 1
            if s:
                s.info(f"⏳ Processing...({w*2}s)")
            time.sleep(2)
            f = genai.get_file(f.name)
            if w > 300:
                return None
        return f if f.state.name != "FAILED" else None
    except Exception as e:
        if s:
            s.error(str(e))
        return None

def save_up(u):
    try:
        ext = u.name.split('.')[-1] if '.' in u.name else 'mp4'
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
        u.seek(0, 2)
        sz = u.tell()
        u.seek(0)
        prog = st.progress(0)
        wr = 0
        while ch := u.read(10*1024*1024):
            tmp.write(ch)
            wr += len(ch)
            prog.progress(min(wr/sz, 1.0))
        tmp.close()
        prog.empty()
        return tmp.name, None
    except Exception as e:
        return None, str(e)

def rm_file(p):
    if p and os.path.exists(p):
        try:
            os.remove(p)
        except:
            pass

def read_file(u):
    try:
        t = u.type
        if t == "text/plain":
            return u.getvalue().decode("utf-8")
        elif t == "application/pdf" and PDF_AVAILABLE:
            return "\n".join([p.extract_text() or "" for p in PyPDF2.PdfReader(io.BytesIO(u.getvalue())).pages])
        elif "wordprocessingml" in t and DOCX_AVAILABLE:
            return "\n".join([p.text for p in Document(io.BytesIO(u.getvalue())).paragraphs])
        return None
    except:
        return None

def get_gid(url):
    try:
        if 'drive.google.com' in url:
            if '/file/d/' in url:
                return url.split('/file/d/')[1].split('/')[0].split('?')[0]
            elif 'id=' in url:
                return url.split('id=')[1].split('&')[0]
        return None
    except:
        return None

def dl_gdrive(url, s=None):
    try:
        fid = get_gid(url)
        if not fid:
            return None, "Invalid URL"
        if s:
            s.info("📥 Downloading from Google Drive...")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        if GDOWN_AVAILABLE and gdown.download(f"https://drive.google.com/uc?id={fid}", tmp, quiet=False, fuzzy=True):
            if os.path.exists(tmp) and os.path.getsize(tmp) > 1000:
                return tmp, None
        return None, "Download failed"
    except Exception as e:
        return None, str(e)

def download_video_url(url, status=None):
    """Download from YouTube, Facebook, TikTok, Google Drive"""
    try:
        if status:
            status.info("📥 Downloading video...")
        
        try:
            cookies_content = st.secrets["youtube"]["cookies"]
            with open("/tmp/cookies.txt", "w") as f:
                f.write(cookies_content)
        except:
            pass
        
        if 'drive.google.com' in url:
            path, err = dl_gdrive(url, status)
            return path, err
        
        output_path = f"/tmp/video_{int(time.time())}.mp4"
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 60,
            'cookiefile': '/tmp/cookies.txt' if os.path.exists('/tmp/cookies.txt') else None,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(output_path):
            return output_path, None
        else:
            return None, "Download failed"
    except Exception as e:
        return None, str(e)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login(e, p):
    if not supabase:
        return None, "Database Error"
    try:
        r = supabase.table('users').select('*').eq('email', e).eq('password', hash_pw(p)).execute()
        if r.data:
            u = r.data[0]
            return (u, "OK") if u['approved'] else (None, "Pending approval")
        return None, "Invalid credentials"
    except Exception as ex:
        return None, str(ex)

def register(e, p):
    if not supabase:
        return False, "Database Error"
    try:
        if supabase.table('users').select('email').eq('email', e).execute().data:
            return False, "Email already exists"
        supabase.table('users').insert({"email": e, "password": hash_pw(p), "approved": False, "is_admin": False}).execute()
        return True, "Registered! Please wait for admin approval."
    except Exception as ex:
        return False, str(ex)

def srt_to_text(srt_content):
    lines = srt_content.split('\n')
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.isdigit() or '-->' in line:
            continue
        text_lines.append(line)
    return '\n'.join(text_lines)

def text_to_srt(text, sec_per_line=3):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    srt_out = []
    for i, line in enumerate(lines):
        start = i * sec_per_line
        end = (i + 1) * sec_per_line
        sh, sm, ss = start // 3600, (start % 3600) // 60, start % 60
        eh, em, es = end // 3600, (end % 3600) // 60, end % 60
        srt_out.append(f"{i+1}")
        srt_out.append(f"{sh:02d}:{sm:02d}:{ss:02d},000 --> {eh:02d}:{em:02d}:{es:02d},000")
        srt_out.append(line)
        srt_out.append("")
    return '\n'.join(srt_out)

# === TTS FUNCTIONS ===
def edge_v():
    return {
        "🇲🇲 Myanmar-Thiha (Male)": "my-MM-ThihaNeural",
        "🇲🇲 Myanmar-Nilar (Female)": "my-MM-NilarNeural",
        "🇺🇸 English-Jenny (Female)": "en-US-JennyNeural",
        "🇺🇸 English-Guy (Male)": "en-US-GuyNeural",
        "🇹🇭 Thai (Female)": "th-TH-PremwadeeNeural",
        "🇨🇳 Chinese (Female)": "zh-CN-XiaoxiaoNeural",
        "🇯🇵 Japanese (Female)": "ja-JP-NanamiNeural",
        "🇰🇷 Korean (Female)": "ko-KR-SunHiNeural"
    }

def gem_v():
    return {
        "Puck (Male)": "Puck",
        "Charon (Male)": "Charon",
        "Kore (Female)": "Kore",
        "Fenrir (Male)": "Fenrir",
        "Aoede (Female)": "Aoede",
        "Leda (Female)": "Leda",
        "Orus (Male)": "Orus",
        "Zephyr (Male)": "Zephyr"
    }

def get_voice_styles():
    return {
        "🎬 Standard Storytelling": "Narrate in an engaging and expressive storytelling style, suitable for a movie recap.",
        "🔥 Dramatic & Suspenseful": "A deep, dramatic, and suspenseful narration style. The voice should sound serious and intense.",
        "😊 Casual & Friendly": "Speak in a casual, friendly, and energetic manner, like a YouTuber summarizing a movie to a friend.",
        "🎃 Horror & Creepy": "Narrate in a chilling, eerie, and unsettling tone perfect for ghost stories and horror content.",
        "🎭 Emotional & Dramatic": "Deliver the narration with deep emotional expression, as if performing a dramatic reading.",
        "📺 News Anchor": "Speak in a professional, clear, and authoritative news anchor style.",
        "🎓 Documentary": "Narrate in a calm, educational, and informative documentary style.",
        "🎪 Custom": ""
    }

def gen_gem_styled(key, txt, v, mdl, style_prompt="", speed=1.0):
    if not GENAI_NEW_AVAILABLE:
        return None, "google-genai not installed"
    try:
        cl = genai_new.Client(api_key=key)
        speed_instruction = ""
        if speed < 1.0:
            speed_instruction = f" Speak slowly at {speed}x speed."
        elif speed > 1.0:
            speed_instruction = f" Speak faster at {speed}x speed."
        full_text = f"[Voice Style: {style_prompt}{speed_instruction}]\n\n{txt}" if style_prompt or speed_instruction else txt
        cfg = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=v)
                )
            )
        )
        aud = b""
        mime = "audio/L16;rate=24000"
        for ch in cl.models.generate_content_stream(
            model=mdl,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=full_text)])],
            config=cfg
        ):
            if ch.candidates and ch.candidates[0].content and ch.candidates[0].content.parts:
                p = ch.candidates[0].content.parts[0]
                if hasattr(p, 'inline_data') and p.inline_data and p.inline_data.data:
                    aud += p.inline_data.data
                    mime = p.inline_data.mime_type
        if not aud:
            return None, "No audio generated"
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(out, "wb") as f:
            f.write(to_wav(aud, mime))
        return out, None
    except Exception as e:
        return None, str(e)

def gen_edge(txt, v, r=0):
    if not EDGE_TTS_AVAILABLE:
        return None, "Edge TTS not available"
    try:
        out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        rs = f"+{r}%" if r >= 0 else f"{r}%"
        async def _g():
            await edge_tts.Communicate(txt, v, rate=rs).save(out)
        asyncio.run(_g())
        return out, None
    except Exception as e:
        return None, str(e)

# === CONTENT TYPES AND DURATION SETTINGS ===
def get_content_types():
    return {
        "📰 ဆောင်းပါး (Article)": "article",
        "🏆 အောင်မြင်ရေးနည်းလမ်း (Success Tips)": "success_tips",
        "📖 ဝတ္ထုတို (Short Story)": "short_story",
        "🧸 ပုံပြင်တို (Short Tale)": "short_tale",
        "📢 သတင်း (News)": "news",
        "🎬 ဇာတ်လမ်း (Drama)": "drama",
        "👻 သရဲဇာတ်လမ်း (Horror Story)": "horror_story",
        "💔 ဂမ္ဘီရဇာတ်လမ်း (Tragic Story)": "tragic_story",
        "💕 အချစ်ဇာတ်လမ်း (Romance)": "romance",
        "🔮 စိတ်ကူးယဉ် (Fantasy)": "fantasy",
        "🔍 လျှို့ဝှက်ဆန်းကြယ် (Mystery)": "mystery",
        "😂 ဟာသ (Comedy)": "comedy",
        "💪 လှုံ့ဆော်စာ (Motivational)": "motivational",
        "📚 ပညာရေး (Educational)": "educational",
        "🎯 Custom (စိတ်ကြိုက်)": "custom"
    }

def get_duration_options():
    return {
        "⚡ 1 မိနစ် (~150 words)": 150,
        "📝 3 မိနစ် (~450 words)": 450,
        "📄 5 မိနစ် (~750 words)": 750,
        "📑 10 မိနစ် (~1500 words)": 1500,
        "📃 15 မိနစ် (~2250 words)": 2250,
        "📋 20 မိနစ် (~3000 words)": 3000,
        "📚 25 မိနစ် (~3750 words)": 3750,
        "📖 30 မိနစ် (~4500 words)": 4500,
        "📕 35 မိနစ် (~5250 words)": 5250,
        "📗 45 မိနစ် (~6750 words)": 6750,
        "📘 1 နာရီ (~9000 words)": 9000
    }

def get_content_prompt(content_type, title, duration_words, custom_instructions=""):
    base_prompts = {
        "article": f"""ခေါင်းစဉ် "{title}" နဲ့ ပတ်သက်တဲ့ ဆောင်းပါးတစ်ပုဒ် ရေးပါ။
- အချက်အလက်ပြည့်စုံစွာ ရေးပါ
- ဖတ်ရှုသူစိတ်ဝင်စားစေမယ့် အဖွင့်စာပိုဒ်နဲ့ စတင်ပါ
- ကျွမ်းကျင်မှုနဲ့ ယုံကြည်စိတ်ချရမှု ပေါ်လွင်အောင် ရေးပါ""",

        "success_tips": f"""ခေါင်းစဉ် "{title}" နဲ့ ပတ်သက်တဲ့ အောင်မြင်ရေးနည်းလမ်းများ ရေးပါ။
- လက်တွေ့ကျတဲ့ အကြံဉာဏ်များ ပေးပါ
- ဥပမာများ ထည့်သွင်းပါ
- လှုံ့ဆော်စေတဲ့ ပုံစံဖြင့် ရေးပါ""",

        "short_story": f"""ခေါင်းစဉ် "{title}" နဲ့ ဝတ္ထုတိုတစ်ပုဒ် ရေးပါ။
- ဖတ်ရှုသူကို ဆွဲဆောင်နိုင်တဲ့ အစနဲ့ စတင်ပါ
- ဇာတ်ကောင်တွေရဲ့ စိတ်ခံစားချက်ကို ဖော်ပြပါ
- အဆုံးသတ်မှာ သင်ခန်းစာ သို့မဟုတ် အံ့အားသင့်စရာ ထည့်ပါ""",

        "short_tale": f"""ခေါင်းစဉ် "{title}" နဲ့ ပုံပြင်တိုတစ်ပုဒ် ရေးပါ။
- ကလေးများ သို့မဟုတ် လူတိုင်းဖတ်ရှုနိုင်အောင် ရေးပါ
- သင်ခန်းစာ ပါရှိအောင် ရေးပါ
- စိတ်ဝင်စားစရာ ဖြစ်စေပါ""",

        "news": f"""ခေါင်းစဉ် "{title}" နဲ့ ပတ်သက်တဲ့ သတင်းတစ်ပုဒ် ရေးပါ။
- ဂျာနယ်လစ် ပုံစံဖြင့် ရေးပါ
- Who, What, When, Where, Why ပါဝင်အောင် ရေးပါ
- တိကျမှန်ကန်သော ပုံစံဖြင့် ရေးပါ""",

        "drama": f"""ခေါင်းစဉ် "{title}" နဲ့ ဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- စိတ်လှုပ်ရှားစေတဲ့ ဇာတ်လမ်းဖွဲ့ပါ
- ဇာတ်ကောင်တွေရဲ့ dialog များ ထည့်ပါ
- တင်းမာမှု၊ ပဋိပက္ခ ပါဝင်အောင် ရေးပါ""",

        "horror_story": f"""ခေါင်းစဉ် "{title}" နဲ့ သရဲဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- ထိတ်လန့်စေတဲ့ ပတ်ဝန်းကျင် ဖန်တီးပါ
- တဖြည်းဖြည်း တင်းမာလာအောင် ရေးပါ
- ကြောက်စရာကောင်းတဲ့ အဆုံးသတ် ပေးပါ""",

        "tragic_story": f"""ခေါင်းစဉ် "{title}" နဲ့ ဂမ္ဘီရဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- နက်နဲတဲ့ ခံစားချက်များ ဖော်ပြပါ
- ဖတ်ရှုသူ မျက်ရည်ကျစေလောက်အောင် ရေးပါ
- ဘဝသင်ခန်းစာ ပါဝင်အောင် ရေးပါ""",

        "romance": f"""ခေါင်းစဉ် "{title}" နဲ့ အချစ်ဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- ချစ်စရာကောင်းတဲ့ ဇာတ်ကောင်တွေ ဖန်တီးပါ
- စိတ်လှုပ်ရှားစေတဲ့ ခံစားချက်များ ဖော်ပြပါ
- ရင်ခုန်စရာ အခိုက်အတန့်များ ထည့်ပါ""",

        "fantasy": f"""ခေါင်းစဉ် "{title}" နဲ့ စိတ်ကူးယဉ်ဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- ထူးဆန်းတဲ့ ကမ္ဘာတစ်ခု ဖန်တီးပါ
- မှော်အတတ်၊ ထူးဆန်းသောအရာများ ထည့်ပါ
- စိတ်ဝင်စားစရာ စွန့်စားခန်း ရေးပါ""",

        "mystery": f"""ခေါင်းစဉ် "{title}" နဲ့ လျှို့ဝှက်ဆန်းကြယ်ဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- စုံထောက်ပုံစံ သို့မဟုတ် လျှို့ဝှက်ချက်တွေ ထည့်ပါ
- ဖတ်ရှုသူကို ခန့်မှန်းခိုင်းပါ
- အံ့အားသင့်စရာ အဆုံးသတ် ပေးပါ""",

        "comedy": f"""ခေါင်းစဉ် "{title}" နဲ့ ဟာသဇာတ်လမ်းတစ်ပုဒ် ရေးပါ။
- ရယ်စရာကောင်းတဲ့ အခြေအနေများ ဖန်တီးပါ
- ဟာသဆန်တဲ့ dialog များ ထည့်ပါ
- ပျော်ရွှင်စေတဲ့ အဆုံးသတ် ပေးပါ""",

        "motivational": f"""ခေါင်းစဉ် "{title}" နဲ့ လှုံ့ဆော်စာတစ်ပုဒ် ရေးပါ။
- အားပေးစကားများ ထည့်ပါ
- တကယ့်ဘဝ ဥပမာများ ထည့်ပါ
- လုပ်ဆောင်နိုင်တဲ့ အကြံဉာဏ်များ ပေးပါ""",

        "educational": f"""ခေါင်းစဉ် "{title}" နဲ့ ပညာရေးဆိုင်ရာ အကြောင်းအရာ ရေးပါ။
- ရှင်းလင်းလွယ်ကူအောင် ရေးပါ
- ဥပမာများနဲ့ ရှင်းပြပါ
- သိမှတ်စရာ အချက်များ ထည့်ပါ""",

        "custom": f"""ခေါင်းစဉ် "{title}" နဲ့ content ရေးပါ။"""
    }
    
    prompt = base_prompts.get(content_type, base_prompts["article"])
    
    if custom_instructions:
        prompt += f"\n\nအထူးညွှန်ကြားချက်များ:\n{custom_instructions}"
    
    prompt += f"""

**အရေးကြီး**:
- စာလုံးရေ: {duration_words} words ဝန်းကျင် ဖြစ်ရမည်
- ဘာသာစကား: မြန်မာဘာသာဖြင့်သာ ရေးပါ
- အရည်အသွေး: ပရော်ဖက်ရှင်နယ် content creator အဆင့် ဖြစ်ရမည်
- ဖော်မတ်: TTS အတွက် သင့်တော်သော ပုံစံဖြင့် ရေးပါ (အပိုဒ်ခွဲ၊ စာကြောင်းတိုများ)

ယခုပဲ ရေးပါ။ မိတ်ဆက်စာ မလိုပါ။"""
    
    return prompt

# === INITIALIZE SESSION STATE ===
def init_st():
    defaults = {
        'generated_images': [],
        'tts_audio': None,
        'user_session': None,
        'content_result': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_st()

# === LOGIN SYSTEM ===
if not st.session_state['user_session']:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎬 AI Studio Pro</h1>
        <p style="color: #94a3b8; font-size: 1rem;">Content Creator's Ultimate Toolkit</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    t1, t2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with t1:
        with st.container(border=True):
            st.subheader("Welcome Back!")
            with st.form("login_form"):
                e = st.text_input("📧 Email", placeholder="your@email.com")
                p = st.text_input("🔑 Password", type="password", placeholder="Enter password")
                if st.form_submit_button("Login", use_container_width=True):
                    if e and p:
                        u, m = login(e, p)
                        if u:
                            st.session_state['user_session'] = u
                            st.rerun()
                        elif m == "Pending approval":
                            st.warning("⏳ Your account is pending admin approval")
                        else:
                            st.error(f"❌ {m}")
                    else:
                        st.warning("Please fill in all fields")
    
    with t2:
        with st.container(border=True):
            st.subheader("Create Account")
            new_email = st.text_input("📧 Email", key="reg_email", placeholder="your@email.com")
            new_pass = st.text_input("🔑 Password", type="password", key="reg_pass", placeholder="Create password")
            new_pass2 = st.text_input("🔑 Confirm Password", type="password", key="reg_pass2", placeholder="Confirm password")
            
            if st.button("Sign Up", use_container_width=True):
                if new_email and new_pass and new_pass2:
                    if new_pass != new_pass2:
                        st.error("❌ Passwords don't match")
                    else:
                        success, msg = register(new_email, new_pass)
                        if success:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
                else:
                    st.warning("Please fill all fields")

else:
    # === MAIN APP ===
    user = st.session_state['user_session']
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <h1 style="margin: 0; font-size: 1.8rem;">🎬 AI Studio Pro</h1>
            <p style="margin: 0; font-size: 0.85rem; color: #94a3b8;">Content Creator's Toolkit</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['user_session'] = None
            st.rerun()
    
    st.caption(f"👤 {user['email']}")
    
    # Admin Panel
    if user.get('is_admin'):
        with st.expander("🔧 Admin Panel"):
            if supabase:
                users = supabase.table('users').select('*').order('created_at', desc=True).execute().data or []
                for u in users:
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.write(u['email'])
                    with c2:
                        st.caption("✅ Active" if u['approved'] else "⏳ Pending")
                    with c3:
                        if u['email'] != user['email'] and st.button("Toggle", key=f"t_{u['id']}"):
                            supabase.table('users').update({'approved': not u['approved']}).eq('id', u['id']).execute()
                            st.rerun()
    
    st.markdown("---")
    
    # === API KEY SETTINGS ===
    with st.container(border=True):
        st.subheader("⚙️ API Settings")
        st.markdown("""
        <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem;">
            API Key နှစ်မျိုးထည့်နိုင်ပါတယ်။ Pro account (free tier) သို့မဟုတ် Paid account ကို သုံးနိုင်ပါတယ်။
        </p>
        """, unsafe_allow_html=True)
        
        key_type = st.radio(
            "API Key Type",
            ["🆓 Pro Account (Free Tier)", "💳 Paid Account (Billing Enabled)"],
            horizontal=True,
            help="Pro account မှာ rate limits ရှိပါတယ်။ Paid account က unlimited usage ရပါတယ်။"
        )
        
        if "Pro Account" in key_type:
            api_key = st.text_input(
                "🔑 Google AI Pro API Key",
                type="password",
                placeholder="AIza...",
                help="Google AI Studio မှ ရယူနိုင်ပါတယ်: https://aistudio.google.com/apikey"
            )
            st.info("💡 Pro account မှာ တစ်မိနစ်လျှင် requests 15 ခုပဲ သုံးနိုင်ပါတယ်။ Rate limit error ရရင် ခဏစောင့်ပြီး ပြန်ကြိုးစားပါ။")
        else:
            api_key = st.text_input(
                "🔑 Google AI Paid API Key",
                type="password",
                placeholder="AIza...",
                help="Billing enabled API key ထည့်ပါ"
            )
            st.success("✅ Paid account ဖြစ်လျှင် unlimited usage ရပါတယ်။")
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                st.success("✅ API Connected Successfully!")
            except Exception as e:
                st.error(f"❌ Invalid API Key: {str(e)}")
    
    st.markdown("---")
    
    # === MAIN TABS ===
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Content", "🌐 Translate", "🎙️ TTS", "🖼️ Thumbnail"])
    
    # === TAB 1: CONTENT CREATOR ===
    with tab1:
        st.header("✍️ Content Creator")
        st.markdown("""
        <p style="color: #94a3b8; margin-bottom: 1rem;">
            နှစ်သက်ရာခေါင်းစဉ်ပေးလိုက်တာနဲ့ အရည်အသွေးမြင့် content ဖန်တီးပေးပါမယ်။
        </p>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            # Title input
            content_title = st.text_input(
                "📝 ခေါင်းစဉ် (Title)",
                placeholder="ဥပမာ: ဘဝမှာ အောင်မြင်ဖို့ လိုအပ်တဲ့ အရာ ၅ ခု",
                help="ရေးချင်တဲ့ content ရဲ့ ခေါင်းစဉ်ကို ထည့်ပါ"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Content type selection
                content_types = get_content_types()
                selected_type = st.selectbox(
                    "📂 Content အမျိုးအစား",
                    list(content_types.keys()),
                    help="ရေးချင်တဲ့ content အမျိုးအစားကို ရွေးပါ"
                )
            
            with col2:
                # Duration selection
                durations = get_duration_options()
                selected_duration = st.selectbox(
                    "⏱️ Content ကြာချိန်",
                    list(durations.keys()),
                    help="Video duration အရ content အရှည်ကို ရွေးပါ"
                )
            
            # Model selection
            content_model = st.selectbox(
                "🤖 AI Model",
                [
                    "models/gemini-2.5-flash",
                    "models/gemini-2.5-pro",
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-flash",
                    "models/gemini-3-flash-preview",
                    "models/gemini-3-pro-preview"
                ],
                help="Pro model များက ပိုကောင်းသော်လည်း ပိုနှေးပါတယ်"
            )
            
            # Custom instructions (expandable)
            with st.expander("🎨 Custom Instructions (Optional)"):
                custom_instructions = st.text_area(
                    "အထူးညွှန်ကြားချက်များ",
                    placeholder="ဥပမာ: ရယ်စရာတွေ ထည့်ပေးပါ၊ Gen Z ပုံစံဖြင့် ရေးပါ...",
                    height=100,
                    help="သင့်စိတ်ကြိုက် ညွှန်ကြားချက်များ ထည့်နိုင်ပါတယ်"
                )
            
            # Generate button
            if st.button("✨ Generate Content", use_container_width=True, type="primary"):
                if not api_key:
                    st.error("❌ API Key ထည့်ပါ!")
                elif not content_title.strip():
                    st.warning("⚠️ ခေါင်းစဉ် ထည့်ပါ!")
                else:
                    content_type_value = content_types[selected_type]
                    word_count = durations[selected_duration]
                    
                    # Custom type handling
                    if content_type_value == "custom" and not custom_instructions:
                        st.warning("⚠️ Custom အမျိုးအစားအတွက် instructions ထည့်ပါ!")
                    else:
                        with st.spinner(f"✍️ {selected_duration} content ရေးနေပါတယ်..."):
                            try:
                                model = genai.GenerativeModel(content_model)
                                prompt = get_content_prompt(
                                    content_type_value,
                                    content_title,
                                    word_count,
                                    custom_instructions
                                )
                                
                                response, error = call_api(model, prompt, 600)
                                
                                if response:
                                    result, _ = get_text(response)
                                    if result:
                                        st.session_state['content_result'] = result
                                        st.success("✅ Content ဖန်တီးပြီးပါပြီ!")
                                else:
                                    st.error(f"❌ Error: {error}")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
        
        # Display result
        if st.session_state.get('content_result'):
            with st.container(border=True):
                st.subheader("📄 Generated Content")
                
                result = st.session_state['content_result']
                
                # Word count display
                word_count = len(result.split())
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Words", f"{word_count:,}")
                with col2:
                    st.metric("⏱️ Read Time", f"~{max(1, word_count//200)} min")
                with col3:
                    st.metric("🎙️ Speak Time", f"~{max(1, word_count//150)} min")
                
                # Content display
                st.text_area("Content", result, height=400, label_visibility="collapsed")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download TXT",
                        result,
                        f"{content_title[:20]}_content.txt",
                        use_container_width=True
                    )
                with col2:
                    if st.button("🗑️ Clear", use_container_width=True):
                        st.session_state['content_result'] = None
                        st.rerun()
    
    # === TAB 2: TRANSLATE ===
    with tab2:
        st.header("🌐 Translator")
        
        # Important notice
        st.markdown("""
        <div style="background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #22d3ee; margin: 0; font-size: 0.9rem;">
                💡 <strong>အကြံပြုချက်:</strong> Google Drive link (သို့) File upload နည်းလမ်းက အဆင်အပြေဆုံးဖြစ်ပါတယ်။ 
                YouTube/TikTok link များမှာ rate limit ပြဿနာ ရှိနိုင်ပါတယ်။
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col2:
                trans_model = st.selectbox(
                    "🤖 Model",
                    [
                        "models/gemini-2.5-flash",
                        "models/gemini-2.5-pro",
                        "gemini-2.0-flash-exp",
                        "gemini-1.5-flash"
                    ],
                    key="trans_model"
                )
            
            with col1:
                languages = {
                    "🇲🇲 Burmese": "Burmese",
                    "🇺🇸 English": "English",
                    "🇹🇭 Thai": "Thai",
                    "🇨🇳 Chinese": "Chinese",
                    "🇯🇵 Japanese": "Japanese",
                    "🇰🇷 Korean": "Korean"
                }
                target_lang = st.selectbox("🎯 Target Language", list(languages.keys()))
            
            # Input method
            input_method = st.radio(
                "📁 Input Method",
                ["📤 File Upload (Recommended)", "🔗 Video URL"],
                horizontal=True,
                help="File upload နှင့် Google Drive link က ပိုမိုယုံကြည်စိတ်ချရပါတယ်"
            )
            
            if "File Upload" in input_method:
                trans_file = st.file_uploader(
                    "Upload File",
                    type=["mp3", "mp4", "txt", "srt", "docx"],
                    help="Audio, Video, Text files များ upload လုပ်နိုင်ပါတယ်"
                )
                video_url = None
            else:
                trans_file = None
                video_url = st.text_input(
                    "🔗 Video URL",
                    placeholder="YouTube, Facebook, TikTok, Google Drive link",
                    help="Google Drive link က အဆင်အပြေဆုံးဖြစ်ပါတယ်"
                )
            
            # Style file (optional)
            with st.expander("🎨 Style Reference (Optional)"):
                style_file = st.file_uploader(
                    "Style File",
                    type=["txt", "pdf", "docx"],
                    key="trans_style",
                    help="ဘာသာပြန်ပုံစံကို ကိုးကားဖို့ file upload လုပ်နိုင်ပါတယ်"
                )
            
            style_text = ""
            if style_file:
                content = read_file(style_file)
                if content:
                    style_text = content[:3000]
                    st.success(f"✅ Style loaded: {style_file.name}")
            
            # Translate button
            if st.button("🌐 Translate", use_container_width=True, type="primary"):
                if not api_key:
                    st.error("❌ API Key ထည့်ပါ!")
                elif not trans_file and not video_url:
                    st.warning("⚠️ File upload လုပ်ပါ သို့မဟုတ် URL ထည့်ပါ!")
                else:
                    target = languages[target_lang]
                    model = genai.GenerativeModel(trans_model)
                    style_instruction = f"\n\nStyle reference:\n{style_text}" if style_text else ""
                    
                    # Video URL handling
                    if video_url and not trans_file:
                        progress = st.progress(0)
                        status = st.empty()
                        
                        status.info("📥 Downloading video...")
                        progress.progress(10)
                        
                        path, err = download_video_url(video_url, status)
                        
                        if path:
                            progress.progress(30)
                            status.info("📤 Uploading to Gemini...")
                            
                            gem_file = upload_gem(path)
                            
                            if gem_file:
                                status.info("🌐 Transcribing & Translating...")
                                progress.progress(50)
                                
                                response, err = call_api(
                                    model,
                                    [gem_file, f"Listen to this video/audio carefully. Transcribe all spoken words and translate them to {target}. Return ONLY the translated text in {target} language.{style_instruction}"],
                                    900
                                )
                                
                                progress.progress(90)
                                
                                if response:
                                    result, _ = get_text(response)
                                    progress.progress(100)
                                    status.success("✅ Translation completed!")
                                    
                                    if result:
                                        st.text_area("📝 Result", result, height=300)
                                        
                                        # Prepare downloads
                                        if '-->' in result:
                                            srt_result = result
                                            txt_result = srt_to_text(result)
                                        else:
                                            srt_result = text_to_srt(result, 3)
                                            txt_result = result
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.download_button("📥 TXT Download", txt_result, "translated.txt", use_container_width=True)
                                        with col2:
                                            st.download_button("📥 SRT Download", srt_result, "translated.srt", use_container_width=True)
                                else:
                                    progress.empty()
                                    status.error(f"❌ Error: {err if err else 'Timeout'}")
                                
                                try:
                                    genai.delete_file(gem_file.name)
                                except:
                                    pass
                            else:
                                progress.empty()
                                status.error("❌ Upload to Gemini failed")
                            
                            rm_file(path)
                        else:
                            status.error(f"❌ Download failed: {err}")
                    
                    # File upload handling
                    elif trans_file:
                        ext = trans_file.name.split('.')[-1].lower()
                        
                        if ext in ['txt', 'srt']:
                            txt = trans_file.getvalue().decode("utf-8")
                            st.info(f"📄 File: {trans_file.name} | {len(txt):,} characters")
                            
                            progress = st.progress(0)
                            status = st.empty()
                            
                            status.info("🌐 Translating...")
                            progress.progress(30)
                            
                            response, err = call_api(
                                model,
                                f"Translate to {target}. Return ONLY translated text.{style_instruction}\n\n{txt}",
                                900
                            )
                            
                            progress.progress(90)
                            
                            if response:
                                result, _ = get_text(response)
                                progress.progress(100)
                                status.success("✅ Done!")
                                
                                if result:
                                    st.text_area("📝 Result", result, height=300)
                                    
                                    if '-->' in result:
                                        srt_result = result
                                        txt_result = srt_to_text(result)
                                    else:
                                        srt_result = text_to_srt(result, 3)
                                        txt_result = result
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.download_button("📥 TXT", txt_result, f"trans_{trans_file.name.rsplit('.', 1)[0]}.txt", use_container_width=True)
                                    with col2:
                                        st.download_button("📥 SRT", srt_result, f"trans_{trans_file.name.rsplit('.', 1)[0]}.srt", use_container_width=True)
                            else:
                                progress.empty()
                                status.error(f"❌ Error: {err if err else 'Timeout'}")
                        
                        elif ext == 'docx':
                            txt = read_file(trans_file)
                            if txt:
                                st.info(f"📄 File: {trans_file.name} | {len(txt):,} characters")
                                
                                progress = st.progress(0)
                                status = st.empty()
                                
                                status.info("🌐 Translating...")
                                progress.progress(30)
                                
                                response, err = call_api(
                                    model,
                                    f"Translate to {target}. Return ONLY translated text.{style_instruction}\n\n{txt}",
                                    900
                                )
                                
                                progress.progress(90)
                                
                                if response:
                                    result, _ = get_text(response)
                                    progress.progress(100)
                                    status.success("✅ Done!")
                                    
                                    if result:
                                        st.text_area("📝 Result", result, height=300)
                                        st.download_button("📥 Download", result, f"trans_{trans_file.name.rsplit('.', 1)[0]}.txt", use_container_width=True)
                                else:
                                    progress.empty()
                                    status.error(f"❌ Error: {err if err else 'Timeout'}")
                        
                        else:  # Audio/Video files
                            st.info(f"📁 File: {trans_file.name}")
                            
                            progress = st.progress(0)
                            status = st.empty()
                            
                            status.info("📤 Uploading file...")
                            progress.progress(20)
                            
                            path, _ = save_up(trans_file)
                            
                            if path:
                                status.info("🔄 Processing...")
                                progress.progress(40)
                                
                                gem_file = upload_gem(path)
                                
                                if gem_file:
                                    status.info("🌐 Transcribing & Translating...")
                                    progress.progress(60)
                                    
                                    response, err = call_api(
                                        model,
                                        [gem_file, f"Listen to this video/audio carefully. Transcribe all spoken words and translate them to {target}. Return ONLY the translated text.{style_instruction}"],
                                        900
                                    )
                                    
                                    progress.progress(90)
                                    
                                    if response:
                                        result, _ = get_text(response)
                                        progress.progress(100)
                                        status.success("✅ Done!")
                                        
                                        if result:
                                            st.text_area("📝 Result", result, height=300)
                                            
                                            if '-->' in result:
                                                srt_result = result
                                                txt_result = srt_to_text(result)
                                            else:
                                                srt_result = text_to_srt(result, 3)
                                                txt_result = result
                                            
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.download_button("📥 TXT", txt_result, f"{trans_file.name.rsplit('.', 1)[0]}_trans.txt", use_container_width=True)
                                            with col2:
                                                st.download_button("📥 SRT", srt_result, f"{trans_file.name.rsplit('.', 1)[0]}_trans.srt", use_container_width=True)
                                    else:
                                        progress.empty()
                                        status.error(f"❌ Error: {err if err else 'Timeout'}")
                                    
                                    try:
                                        genai.delete_file(gem_file.name)
                                    except:
                                        pass
                                else:
                                    progress.empty()
                                    status.error("❌ Upload failed")
                                
                                rm_file(path)
    
    # === TAB 3: TTS ===
    with tab3:
        st.header("🎙️ Text to Speech")
        
        with st.container(border=True):
            engine = st.radio(
                "🔊 TTS Engine",
                ["⚡ Edge TTS (Free, Myanmar)", "✨ Gemini TTS (Pro, Styled)"],
                horizontal=True
            )
            
            st.markdown("---")
            
            if "Edge TTS" in engine:
                if not EDGE_TTS_AVAILABLE:
                    st.error("❌ Edge TTS not available")
                else:
                    tts_text = st.text_area(
                        "📝 Text to Convert",
                        height=200,
                        placeholder="ဒီမှာ စာသားရိုက်ထည့်ပါ...",
                        key="edge_text"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        voice = st.selectbox("🔊 Voice", list(edge_v().keys()), key="edge_voice")
                    with col2:
                        rate = st.slider("⚡ Speed", -50, 50, 0, format="%d%%", key="edge_rate")
                    
                    st.caption(f"📊 Characters: {len(tts_text)}")
                    
                    if st.button("🎙️ Generate Audio", use_container_width=True, key="gen_edge", type="primary"):
                        if tts_text.strip():
                            with st.spinner("🔄 Generating..."):
                                path, err = gen_edge(tts_text, edge_v()[voice], rate)
                                if path:
                                    st.session_state['tts_audio'] = path
                                    st.success("✅ Audio generated!")
                                else:
                                    st.error(f"❌ {err}")
                        else:
                            st.warning("⚠️ Enter text first!")
            
            else:  # Gemini TTS
                if not GENAI_NEW_AVAILABLE:
                    st.error("❌ google-genai not installed")
                else:
                    tts_text = st.text_area(
                        "📝 Text to Convert",
                        height=200,
                        placeholder="ဒီမှာ စာသားရိုက်ထည့်ပါ...",
                        key="gem_text"
                    )
                    
                    # Voice style selection
                    voice_styles = get_voice_styles()
                    selected_style = st.selectbox("🎨 Voice Style", list(voice_styles.keys()), key="gem_style")
                    style_prompt = voice_styles[selected_style]
                    
                    if "Custom" in selected_style:
                        style_prompt = st.text_area(
                            "Custom Style",
                            height=80,
                            placeholder="Describe how you want the voice to sound...",
                            key="custom_voice_style"
                        )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        voice = st.selectbox("🔊 Voice", list(gem_v().keys()), key="gem_voice")
                    with col2:
                        tts_model = st.selectbox(
                            "🤖 Model",
                            ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"],
                            key="gem_model"
                        )
                    with col3:
                        speed = st.slider("⚡ Speed", 0.50, 2.00, 1.00, 0.02, key="gem_speed")
                    
                    st.caption(f"📊 Characters: {len(tts_text)}")
                    
                    if st.button("🎙️ Generate Audio", use_container_width=True, key="gen_gem", type="primary"):
                        if not api_key:
                            st.error("❌ API Key ထည့်ပါ!")
                        elif not tts_text.strip():
                            st.warning("⚠️ Enter text first!")
                        else:
                            with st.spinner(f"🔄 Generating with {tts_model}..."):
                                path, err = gen_gem_styled(api_key, tts_text, gem_v()[voice], tts_model, style_prompt, speed)
                                if path:
                                    st.session_state['tts_audio'] = path
                                    st.success("✅ Audio generated!")
                                else:
                                    st.error(f"❌ {err}")
        
        # Audio output
        if st.session_state.get('tts_audio') and os.path.exists(st.session_state['tts_audio']):
            with st.container(border=True):
                st.subheader("🔊 Generated Audio")
                
                with open(st.session_state['tts_audio'], 'rb') as f:
                    audio_bytes = f.read()
                
                mime = "audio/wav" if st.session_state['tts_audio'].endswith(".wav") else "audio/mp3"
                st.audio(audio_bytes, format=mime)
                
                ext = "wav" if ".wav" in st.session_state['tts_audio'] else "mp3"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 Download Audio", audio_bytes, f"audio.{ext}", mime, use_container_width=True)
                with col2:
                    if st.button("🗑️ Clear Audio", use_container_width=True):
                        rm_file(st.session_state['tts_audio'])
                        st.session_state['tts_audio'] = None
                        st.rerun()
    
    # === TAB 4: THUMBNAIL ===
    with tab4:
        st.header("🖼️ AI Thumbnail Generator")
        st.caption("Powered by Gemini 3 Pro Image")
        
        with st.container(border=True):
            # Reference images
            ref_images = st.file_uploader(
                "🖼️ Reference Images (Max 10)",
                type=["png", "jpg", "jpeg", "webp"],
                accept_multiple_files=True,
                help="Similar style ရှိတဲ့ ပုံများ upload လုပ်နိုင်ပါတယ်"
            )
            
            if ref_images:
                st.caption(f"📷 {len(ref_images)} image(s) uploaded")
                cols = st.columns(min(len(ref_images), 6))
                for i, img in enumerate(ref_images[:6]):
                    with cols[i]:
                        st.image(img, use_container_width=True)
            
            st.markdown("---")
            
            # Templates
            templates = {
                "🎨 Custom": "",
                "🎬 Movie Recap": "dramatic YouTube movie recap thumbnail, cinematic lighting, emotional scene, bold title text, film grain effect, dark moody atmosphere",
                "😱 Shocking": "YouTube thumbnail, shocked surprised expression, bright red yellow background, bold dramatic text, eye-catching, viral style",
                "👻 Horror": "horror movie thumbnail, dark scary atmosphere, creepy shadows, fear expression, blood red accents, haunted feeling",
                "😂 Comedy": "funny comedy thumbnail, bright colorful, laughing expression, playful text, cheerful mood",
                "💕 Romance": "romantic movie thumbnail, soft pink lighting, couple silhouette, heart elements, dreamy bokeh background",
                "💥 Action": "action movie thumbnail, explosive background, fire sparks, intense expression, dynamic pose, bold red orange colors",
                "😢 Drama": "emotional drama thumbnail, tears sad expression, rain effect, blue moody lighting, touching moment",
                "🔮 Fantasy": "fantasy magical thumbnail, glowing effects, mystical atmosphere, enchanted, purple blue colors"
            }
            
            selected_template = st.selectbox("📋 Template", list(templates.keys()))
            
            # Size options
            sizes = {
                "📺 16:9 (1280x720)": "1280x720",
                "📱 9:16 (720x1280)": "720x1280",
                "⬜ 1:1 (1024x1024)": "1024x1024",
                "🖼️ 4:3 (1024x768)": "1024x768"
            }
            size = st.selectbox("📐 Size", list(sizes.keys()))
            
            # Prompt
            prompt = st.text_area(
                "✏️ Prompt",
                value=templates[selected_template],
                height=100,
                placeholder="Describe your thumbnail..."
            )
            
            # Text and style
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                add_text = st.text_input("📝 Add Text", placeholder="EP.1, Part 2, etc.")
            
            with col2:
                text_styles = {
                    "Default": "bold text",
                    "Gold 3D": "gold 3D metallic text, shiny, luxurious",
                    "White 3D Blue": "white 3D text with dark blue outline, bold",
                    "Yellow 3D Black": "yellow 3D text with black outline, bold impact",
                    "Red 3D Yellow": "red 3D text with yellow outline, bold dramatic",
                    "Horror": "creepy horror text, blood dripping, scary font",
                    "Romance": "elegant romantic pink text, script font"
                }
                text_style = st.selectbox("🎨 Text Style", list(text_styles.keys()))
            
            with col3:
                num_images = st.selectbox("🔢 Count", [1, 2, 3, 4])
            
            # Generate button
            if st.button("✨ Generate Thumbnails", use_container_width=True, type="primary"):
                if not api_key:
                    st.error("❌ API Key ထည့်ပါ!")
                elif not prompt.strip():
                    st.warning("⚠️ Prompt ထည့်ပါ!")
                else:
                    st.session_state['generated_images'] = []
                    
                    # Build final prompt
                    size_value = sizes[size]
                    text_style_prompt = text_styles[text_style] if add_text else ""
                    final_prompt = prompt.strip()
                    if add_text:
                        final_prompt += f", text:'{add_text}', {text_style_prompt}"
                    final_prompt += f", {size_value}, high quality"
                    
                    # Load reference images
                    ref_pil_images = []
                    if ref_images:
                        for r in ref_images[:10]:
                            try:
                                r.seek(0)
                                img_bytes = r.read()
                                ref_pil_images.append(Image.open(io.BytesIO(img_bytes)))
                            except Exception as e:
                                st.warning(f"⚠️ Reference image load failed: {e}")
                    
                    # Generate function
                    def generate_single(idx, prompt, ref_imgs):
                        try:
                            mdl = genai.GenerativeModel("models/gemini-3-pro-image-preview")
                            content_parts = [f"Generate image: {prompt}"]
                            if ref_imgs:
                                content_parts.extend(ref_imgs)
                            
                            response = mdl.generate_content(content_parts, request_options={"timeout": 300})
                            
                            if response.candidates:
                                for p in response.candidates[0].content.parts:
                                    if hasattr(p, 'inline_data') and p.inline_data:
                                        img_data = p.inline_data.data
                                        mime = p.inline_data.mime_type
                                        
                                        if img_data and len(img_data) > 1000:
                                            return {'data': img_data, 'mime': mime, 'idx': idx, 'success': True}
                            
                            return {'error': 'No image generated', 'idx': idx, 'success': False}
                        except Exception as e:
                            return {'error': str(e), 'idx': idx, 'success': False}
                    
                    # Progress
                    progress_bar = st.progress(0)
                    status = st.empty()
                    
                    generated_count = 0
                    
                    for i in range(1, num_images + 1):
                        status.info(f"🎨 Generating image {i}/{num_images}...")
                        
                        result = generate_single(i, final_prompt, ref_pil_images)
                        
                        if result and result.get('success'):
                            st.session_state['generated_images'].append(result)
                            generated_count += 1
                            status.success(f"✅ Image {i} generated!")
                        else:
                            error_msg = result.get('error', 'Unknown error') if result else 'No response'
                            status.warning(f"⚠️ Image {i} failed: {error_msg}")
                        
                        progress_bar.progress(i / num_images)
                        
                        if i < num_images:
                            time.sleep(1)
                    
                    if generated_count > 0:
                        status.success(f"✅ Generated {generated_count}/{num_images} images!")
                    else:
                        status.error("❌ All images failed to generate")
            
            # Display results
            if st.session_state.get('generated_images'):
                st.markdown("---")
                st.subheader("🖼️ Generated Thumbnails")
                
                if st.button("🗑️ Clear All", key="clear_thumbs"):
                    st.session_state['generated_images'] = []
                    st.rerun()
                
                for i, img in enumerate(st.session_state['generated_images']):
                    with st.container(border=True):
                        try:
                            st.image(img['data'], use_container_width=True)
                            st.download_button(
                                f"📥 Download #{img['idx']}",
                                img['data'],
                                f"thumbnail_{img['idx']}.png",
                                mime=img.get('mime', 'image/png'),
                                key=f"dl_thumb_{i}_{int(time.time()*1000)}",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error displaying image: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <p style="color: #64748b; font-size: 0.85rem;">
            🎬 AI Studio Pro v7.0 | Made with ❤️ for Content Creators
        </p>
    </div>
    """, unsafe_allow_html=True)

# flightbot_simulation_subtitles_expanded.py
"""
Expanded version of the cockpit simulation with:
 - cinematic subtitles (fade in/out)
 - full-line subtitle display (no word-by-word)
 - text wrapping for long lines
 - forced video trim (start / end) with fail-safe end even if video lags
 - pip loop + alarms + flightbot chime
 - speech time-stretching (SPEED_SCALE) to make voices sound more natural
 - websocket broadcast (optional) for external subtitle clients
"""

import asyncio
import websockets
import threading
import json
import os
import time
import subprocess
import urllib.request
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine
import pygame
import uuid
import math
import textwrap

# Audio & video assets in project root
ambient_file = "cockpit_ambient.mp3"
fixed_ambient = "cockpit_ambient_fixed.wav"
video_filename = "cockpitsim.mp4"

# Directories for generated voices
base_audio_dir = "voices"
for folder in ["pilot", "copilot", "atc", "flightbot", "cabincrew", "temp"]:
    os.makedirs(os.path.join(base_audio_dir, folder), exist_ok=True)
os.makedirs("temp", exist_ok=True)

# WebSocket port (optional)
WS_PORT = 8765

VIDEO_PATH = "your_video.mp4"

# 🎬 Force video trim range (seconds)
VIDEO_TRIM_START = 220.0
VIDEO_TRIM_END = 370.0

# Speed scale for making speech feel natural (1.0 = original). <1.0 slows down.
SPEED_SCALE = 0.85

# Subtitle fade durations
FADE_IN = 0.35
FADE_OUT = 0.35

# Subtitle visuals
SUB_FONT_SIZE = 36
SUB_MAX_WIDTH_RATIO = 0.78

# Pygame audio channels
CHANNEL_AMBIENT = 0
CHANNEL_PIP = 1
CHANNEL_VOICE = 2
CHANNEL_ALARM = 3

# TTS language mapping
voice_roles = {
    "Pilot": "en",
    "Co-Pilot": "en",
    "ATC": "en",
    "Flight Bot": "en",
    "Cabin Crew": "en"
}

# Script: (speaker, text, pause_after_seconds)
script = [
    ("Pilot", "Bird strike! Bird strike! Both engines gone!", 1.5),
    ("Co-Pilot", "Oh no! We're losing control!", 1.5),
    ("Pilot", "Relax! Focus on your instruments. We can handle this.", 1.5),
    ("Co-Pilot", "Okay, okay okay. I'm trying to stabilize the plane.", 1.5),
    ("Pilot", "Contact ATC immediately. Declare emergency!", 1.0),
    ("Co-Pilot", "Mayday! Mayday! Mayday! We have lost both engines. We are currently gliding and heading towards Kwesi Andrews Airport. Is runway R3 available?", 2.0),
    ("ATC", "Roger that. Flight Quebec Alpha one two three, runway Zero Niner Romeo is clear for immediate landing.", 1.8),
    ("Pilot", "Attention cabin crew, this is your captain. Brace for impact!", 1.0),
    ("Cabin Crew", "Fasten your seatbelt! Brace for impact! Brace! Brace! Brace! Brace!", 0.8),
    ("Pilot", "Activating Flight Bot.", 0.6),
    ("Flight Bot", "Flight Bot activated. Running system diagnostics for 2 seconds.", 0.6),
    ("Flight Bot", "Engines offline. Initiate emergency glide procedure. Maintain heading 180 degrees.", 0.8),
    ("Flight Bot", "Prepare checklist for dual engine failure. Monitor altitude, airspeed, and heading.", 0.8),
    ("Flight Bot", "Communicate with ATC, declare emergency, and request closest landing site.", 1.0),
    ("Pilot", "Following Flight Bot instructions.", 0.8),
    ("Flight Bot", "Approaching landing zone. Configure flaps and landing gear. Maintain stabilized approach.", 0.8),
    ("Flight Bot", "Touchdown in progress. Reduce throttle and engage braking procedures.", 1.0),
    ("Pilot", "We have landed successfully. Excellent job.", 1.5),
]

def get_folder_for_speaker(speaker):
    mapping = {
        "Pilot": "pilot",
        "Co-Pilot": "copilot",
        "ATC": "atc",
        "Flight Bot": "flightbot",
        "Cabin Crew": "cabincrew"
    }
    return os.path.join(base_audio_dir, mapping.get(speaker, "temp"))

def safe_fname(prefix="tmp", ext="wav"):
    return os.path.join("temp", f"{prefix}_{uuid.uuid4().hex}.{ext}")

os.makedirs("temp", exist_ok=True)

def convert_to_fixed_ambient(src, dest):
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", src,
            "-acodec", "pcm_s16le", "-ar", "44100", dest
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(dest):
            return True
    except Exception:
        pass
    try:
        seg = AudioSegment.from_file(src)
        seg.export(dest, format="wav")
        return os.path.exists(dest)
    except Exception:
        return False

if not os.path.exists(fixed_ambient) and os.path.exists(ambient_file):
    convert_to_fixed_ambient(ambient_file, fixed_ambient)

def generate_bird_strike_alarm(duration_ms=2000):
    t1 = Sine(600).to_audio_segment(duration=duration_ms).apply_gain(-6)
    t2 = Sine(900).to_audio_segment(duration=duration_ms).apply_gain(-10)
    alarm = t1.overlay(t2)
    pulse = Sine(1000).to_audio_segment(duration=200).apply_gain(-5)
    repeated = AudioSegment.silent(duration=0)
    for _ in range(int(duration_ms/300)):
        repeated += pulse + AudioSegment.silent(duration=100)
    alarm = alarm.overlay(repeated)
    path = safe_fname("bird_alarm")
    alarm.export(path, format="wav")
    return path

def generate_brace_bell():
    chime = Sine(1500).to_audio_segment(duration=120).apply_gain(-3).fade_in(10).fade_out(30)
    seq = chime + AudioSegment.silent(duration=100) + chime + AudioSegment.silent(duration=100) + chime
    path = safe_fname("brace_bell")
    seq.export(path, format="wav")
    return path

def generate_mayday_pulse(duration_ms=2000):
    pulse = Sine(700).to_audio_segment(duration=150).apply_gain(-6)
    seg = AudioSegment.silent(duration=0)
    for _ in range(int(duration_ms/250)):
        seg += pulse + AudioSegment.silent(duration=100)
    path = safe_fname("mayday")
    seg.export(path, format="wav")
    return path

def generate_touchdown_thud():
    thud = Sine(80).to_audio_segment(duration=200).apply_gain(-2).low_pass_filter(200)
    thud = thud.fade_in(10).fade_out(80)
    path = safe_fname("thud")
    thud.export(path, format="wav")
    return path

def generate_flightbot_beep():
    n1 = Sine(1200).to_audio_segment(duration=120).apply_gain(-6).fade_in(10).fade_out(40)
    n2 = Sine(1600).to_audio_segment(duration=160).apply_gain(-8).fade_in(10).fade_out(40)
    combo = n1 + AudioSegment.silent(duration=40) + n2
    path = safe_fname("flightbot_beep")
    combo.export(path, format="wav")
    return path

def generate_pip_loop(loop_ms=3000):
    base = AudioSegment.silent(duration=0)
    pip_tone = Sine(1000).to_audio_segment(duration=60).apply_gain(-6)
    elapsed_local = 0
    while elapsed_local < loop_ms:
        base += pip_tone + AudioSegment.silent(duration=140)
        elapsed_local = len(base)
    path = safe_fname("pip_loop")
    base.export(path, format="wav")
    return path

print("🔔 Generating internal alarms and pip loop...")
alarm_files = {
    "bird": generate_bird_strike_alarm(),
    "brace": generate_brace_bell(),
    "mayday": generate_mayday_pulse(),
    "thud": generate_touchdown_thud(),
    "flightbot": generate_flightbot_beep(),
    "pip": generate_pip_loop(loop_ms=3000),
}
print("✅ Alarms & pip loop ready.")

def make_time_stretched(src_path, dest_path, speed):
    if os.path.exists(dest_path):
        return True
    try:
        seg = AudioSegment.from_file(src_path)
        new_frame = int(max(1000, seg.frame_rate * speed))
        stretched = seg._spawn(seg.raw_data, overrides={"frame_rate": new_frame})
        stretched = stretched.set_frame_rate(44100)
        stretched.export(dest_path, format="wav")
        return os.path.exists(dest_path)
    except Exception as e:
        print("⚠️ time-stretch failed:", e)
        return False

audio_files = []
subtitle_list = []
sim_time = 0.0

print("🎤 Generating voice lines (gTTS) and preparing slowed versions (if needed)...")
for idx, (speaker, text, pause) in enumerate(script):
    folder = get_folder_for_speaker(speaker)
    os.makedirs(folder, exist_ok=True)
    mp3_path = os.path.join(folder, f"voice_{idx}_{speaker}.mp3")
    wav_path = mp3_path.replace(".mp3", ".wav")
    fixed_wav = wav_path.replace(".wav", "_fixed.wav")
    slowed_wav = fixed_wav.replace(".wav", f"_slow.wav")

    if not os.path.exists(fixed_wav):
        try:
            tts = gTTS(text=text, lang=voice_roles.get(speaker, "en"), slow=False)
            tts.save(mp3_path)
            AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
            subprocess.run([
                "ffmpeg", "-y", "-i", wav_path,
                "-acodec", "pcm_s16le", "-ar", "44100", fixed_wav
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"⚠️ gTTS failed for {speaker} ({e}). Creating silent fallback.")
            est_seconds = max(0.6, len(text.split()) * 0.15)
            AudioSegment.silent(duration=int(est_seconds * 1000)).export(fixed_wav, format="wav")

    if SPEED_SCALE != 1.0:
        ok = make_time_stretched(fixed_wav, slowed_wav, SPEED_SCALE)
        play_path = slowed_wav if ok else fixed_wav
    else:
        play_path = fixed_wav

    try:
        dur = AudioSegment.from_wav(play_path).duration_seconds
    except Exception:
        dur = 1.0

    audio_files.append((play_path, text, speaker, pause))
    subtitle_list.append({
        "speaker": speaker,
        "text": text,
        "start": sim_time,
        "end": sim_time + dur
    })
    sim_time += dur + pause

print("✅ Voice generation complete. Total simulated time (approx): {:.2f}s".format(sim_time))

clients = set()
ws_loop = None

async def _ws_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            pass
    finally:
        clients.remove(websocket)

async def _ws_server():
    global ws_loop
    ws_loop = asyncio.get_running_loop()
    async with websockets.serve(_ws_handler, "localhost", WS_PORT):
        print(f"🌐 WebSocket server running on ws://localhost:{WS_PORT}")
        await asyncio.Future()

def start_ws_thread():
    threading.Thread(target=lambda: asyncio.run(_ws_server()), daemon=True).start()

start_ws_thread()

def broadcast_subtitle(speaker, text):
    if ws_loop is None:
        return
    async def _broadcast():
        if clients:
            msg = json.dumps({"speaker": speaker, "text": text})
            await asyncio.gather(*(ws.send(msg) for ws in list(clients)))
    try:
        asyncio.run_coroutine_threadsafe(_broadcast(), ws_loop)
    except Exception:
        pass

pygame.mixer.init()
pygame.mixer.set_num_channels(8)
ambient_channel = pygame.mixer.Channel(CHANNEL_AMBIENT)
pip_channel = pygame.mixer.Channel(CHANNEL_PIP)
voice_channel = pygame.mixer.Channel(CHANNEL_VOICE)
alarm_channel = pygame.mixer.Channel(CHANNEL_ALARM)

ambient_loaded = False
if os.path.exists(fixed_ambient):
    try:
        ambient_obj = pygame.mixer.Sound(fixed_ambient)
        ambient_channel.play(ambient_obj, loops=-1)
        ambient_channel.set_volume(0.4)
        ambient_loaded = True
        print("🎵 Ambient loaded and playing (40%).")
    except Exception as e:
        print("⚠️ Ambient load/play failed:", e)

pip_obj = None
try:
    pip_obj = pygame.mixer.Sound(alarm_files.get("pip"))
except Exception:
    pip_obj = None

pygame.font.init()

def smooth_volume(channel, start_v, end_v, duration=0.6, steps=12):
    if channel is None: return
    try:
        step_time = duration / max(1, steps)
        delta = (end_v - start_v) / max(1, steps)
        for i in range(steps):
            channel.set_volume(max(0.0, min(1.0, start_v + delta * (i + 1))))
            time.sleep(step_time)
    except Exception:
        pass

def play_alarm(name):
    path = alarm_files.get(name)
    if not path or not os.path.exists(path):
        return
    try:
        snd = pygame.mixer.Sound(path)
        alarm_channel.play(snd)
    except Exception:
        pass

def wrap_text_to_surface(text, font, max_width):
    wrapper = textwrap.TextWrapper(width=1000)
    words = text.split()
    if not words:
        return font.render("", True, (255,255,255))
    lines = []
    current = words[0]
    for w in words[1:]:
        test = current + " " + w
        w_px, _ = font.size(test)
        if w_px <= max_width:
            current = test
        else:
            lines.append(current)
            current = w
    lines.append(current)
    line_surfaces = [font.render(line, True, (255,255,255)) for line in lines]
    widths = [s.get_width() for s in line_surfaces]
    heights = [s.get_height() for s in line_surfaces]
    surf_w = max(widths) if widths else 0
    surf_h = sum(heights) + (len(heights)-1) * 6
    surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
    y = 0
    for i, ls in enumerate(line_surfaces):
        surf.blit(ls, (0, y))
        y += heights[i] + 6
    return surf

video_path = os.path.join(os.getcwd(), video_filename)
video_stop_event = threading.Event()
sim_start_time = None

try:
    subtitle_font = pygame.font.SysFont(None, SUB_FONT_SIZE, bold=True)
except Exception:
    pygame.font.init()
    subtitle_font = pygame.font.SysFont(None, SUB_FONT_SIZE, bold=True)

MAX_VIDEO_SEGMENT_DURATION = max(0.001, VIDEO_TRIM_END - VIDEO_TRIM_START)

def get_active_subtitle(now):
    for sub in subtitle_list:
        if sub["start"] <= now <= sub["end"]:
            return sub
    return None

def video_player_thread():
    try:
        import cv2
    except Exception:
        print("⚠️ OpenCV (cv2) not available — skipping video display.")
        return

    if not os.path.exists(video_path):
        print("⚠️ Video not found:", video_path)

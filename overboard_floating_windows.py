import tkinter as tk
import time
import math
import random
import os
import wave
import struct
import ctypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WAV_FILE = os.path.join(SCRIPT_DIR, "overboard_vt.wav")
TOTAL_DURATION = 54.03
SPOTIFY_START_OFFSET = 137.0  # Menit 02:17


class HardwareAudioClock:
    def __init__(self, wav_path):
        self.wav_path = wav_path
        self.alias = "overboard_seamless_sync"
        self.winmm = getattr(ctypes, "windll", None)
        self.has_mci = self.winmm is not None and hasattr(self.winmm, "winmm")
        self._buf = ctypes.create_unicode_buffer(128) if self.has_mci else None
        self.fallback_start = 0.0
        self.is_playing = False

    def _mci(self, cmd):
        if self.has_mci:
            return self.winmm.winmm.mciSendStringW(cmd, self._buf, 128, 0)
        return -1

    def start(self):
        self.stop()
        self.fallback_start = time.perf_counter()
        if self.has_mci and os.path.exists(self.wav_path):
            q = '"'
            err = self._mci(f"open {q}{self.wav_path}{q} type waveaudio alias {self.alias}")
            if err == 0:
                self._mci(f"set {self.alias} time format milliseconds")
                self._mci(f"play {self.alias} from 0")
                self.is_playing = True
                return
        self.is_playing = True

    def get_time_sec(self):
        if self.has_mci and self.is_playing:
            err = self._mci(f"status {self.alias} position")
            if err == 0 and self._buf.value.strip().isdigit():
                return int(self._buf.value.strip()) / 1000.0
        return time.perf_counter() - self.fallback_start

    def stop(self):
        if self.has_mci:
            self._mci(f"stop {self.alias}")
            self._mci(f"close {self.alias}")
        self.is_playing = False


# =============================================================================
#   DATA LIRIK & REFERENSI WAKTU PERSIS DARI KODE ANDA
#   Format: (baris_lagu, delay_karakter, delay_setelah, indo_sub, header_title, theme)
# =============================================================================
INITIAL_DELAY = 0.70  # Detik vokal pertama "Got me..." mulai terdengar di audio

LIRIK_REF = [
    ("Got me out here in the water and i ",              0.10, 0.80, "keluarkan aku dari dalam air dan aku",          "🌊  A D R I F T   I N   T H E   W A T E R", "CYAN"),
    ("I'm overboard ",                                   0.14, 0.20, "aku terjatuh ke dalam air",                     "🌊  C A U G H T   O V E R B O A R D",       "AMETHYST"),
    ("Overboard ",                                       0.08, 0.40, "(jatuh dalam air)",                             "🌊  E C H O   I N   T H E   W A V E S",     "ROSE"),
    ("And i need your love ",                            0.14, 0.01, "Dan aku membutuhkan cintamu",                   "💜  N E E D   Y O U R   L O V E",           "CYAN"),
    ("Pull me up (pull me up) ",                         0.10, 0.10, "tarik aku ke atas (tarik aku ke atas)",         "⚓  P U L L   M E   U P",                   "GOLD"),
    ("I can't swim on my own ",                          0.10, 0.20, "Aku tidak bisa berenang sendiri",               "🌊  L O S T   I N   T H E   D E E P",       "CYAN"),
    ("It's too much (it's too much) ",                   0.09, 0.20, "ini terlalu berat (ini terlalu berat)",         "⚡  W A V E S   T O O   H E A V Y",         "ROSE"),
    ("Feels like i'm drowning ",                         0.08, 0.01, "Terasa seperti tenggelam",                      "💧  S I N K I N G   D E E P E R",           "AMETHYST"),
    ("Without your love ",                               0.10, 0.80, "Tanpa cintamu",                                 "💔  W I T H O U T   Y O U R   L O V E",     "ROSE"),
    ("So throw yourself out to me ",                     0.10, 0.40, "Maka melompatlah padaku",                       "🛟  R E A C H   F O R   M E",               "CYAN"),
    ("My life saver ",                                   0.12, 2.00, "penyelamat hidupku",                            "🛟  M Y   L I F E S A V E R  ✦",            "GOLD"),
    ("It's supposed to be some give and take i know ",   0.08, 1.00, "Harusnya cinta memberi dan menerima, aku tahu", "✨  G I V E   A N D   T A K E",             "AMETHYST"),
    ("But you're only taking and not giving anymore ",   0.09, 2.00, "tapi kau hanya menerima dan tak memberi lagi",  "🌙  O N E - S I D E D   T I D E S",         "ROSE"),
    ("So what do i do (so what do i do) ",               0.08, 0.08, "Jadi apa yang aku lakukan",                     "💭  S O   W H A T   D O   I   D O ?",       "CYAN"),
    ("Cause i still love you (i still love you baby) ",  0.07, 0.10, "Karena aku masih mencintaimu",                  "💖  S T I L L   L O V E   Y O U   B A B Y", "ROSE"),
    ("And you're the only one who can save me ",         0.08, 0.40, "dan kau satu-satunya yang bisa menyelamatkanku","✨  T H E   O N L Y   O N E  ✦",            "GOLD"),
]


def build_lyrics_schedule():
    schedule = []
    current_t = INITIAL_DELAY
    for raw_text, char_delay, post_delay, indo, title, theme in LIRIK_REF:
        type_dur = len(raw_text) * char_delay
        line_end = current_t + type_dur + post_delay
        schedule.append({
            "start": round(current_t, 3),
            "type_end": round(current_t + type_dur, 3),
            "end": round(line_end, 3),
            "raw_text": raw_text,
            "text": raw_text.strip(),
            "char_delay": char_delay,
            "post_delay": post_delay,
            "indo": indo,
            "title": title,
            "theme": theme,
        })
        current_t = line_end
    return schedule


lyrics = build_lyrics_schedule()

THEMES = {
    "AMETHYST": {
        "bg": "#1a0926",
        "card_bg": "#2b103d",
        "border": "#c77dff",
        "accent": "#e0aaff",
        "wave1": "#3c1654",
        "wave2": "#5a189a",
        "text": "#ffffff",
        "highlight": "#ffd166",
        "sub": "#e0aaff",
    },
    "CYAN": {
        "bg": "#071320",
        "card_bg": "#0c1f33",
        "border": "#00e5ff",
        "accent": "#72efdd",
        "wave1": "#10314f",
        "wave2": "#174973",
        "text": "#f2fbff",
        "highlight": "#72efdd",
        "sub": "#90e0ef",
    },
    "ROSE": {
        "bg": "#21091e",
        "card_bg": "#33102f",
        "border": "#ff4d8d",
        "accent": "#ff85b3",
        "wave1": "#4d1645",
        "wave2": "#6e1f62",
        "text": "#fff0f6",
        "highlight": "#ffbe0b",
        "sub": "#ffccd5",
    },
    "GOLD": {
        "bg": "#191129",
        "card_bg": "#25193d",
        "border": "#ffd166",
        "accent": "#ffd166",
        "wave1": "#38255c",
        "wave2": "#503582",
        "text": "#ffffff",
        "highlight": "#ffd166",
        "sub": "#ffe599",
    }
}

KEYWORDS = {
    "overboard", "drowning", "saver", "water",
    "swim", "love", "pull", "save", "anymore"
}

# Kecepatan melayang perlahan, mulus, dan tenang (tidak kencang)
RISE_SPEED = 40.0       # 40 piksel per detik (pelan & sangat elegan)
WAVE_SWAY_AMP = 8.0     # Ayunan ombak sangat halus (±8px)
WAVE_SWAY_FREQ = 1.3    # Frekuensi ayunan tenang


def load_audio_envelope(wav_path, step_sec=0.05):
    envelope = []
    if not os.path.exists(wav_path):
        return envelope
    try:
        with wave.open(wav_path, "rb") as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            chunk_frames = max(1, int(framerate * step_sec))

            while True:
                raw = wf.readframes(chunk_frames)
                if not raw:
                    break
                if sampwidth == 2:
                    count = len(raw) // 2
                    samples = struct.unpack(f"<{count}h", raw)
                    stride = max(1, n_channels * 4)
                    sub = samples[::stride]
                    avg_energy = sum(abs(s) for s in sub) / max(1, len(sub))
                    envelope.append(min(1.0, avg_energy / 8500.0))
                else:
                    envelope.append(0.5)
    except Exception:
        pass
    return envelope


def format_spotify_clock(sec):
    total = int(SPOTIFY_START_OFFSET + sec)
    return f"{total // 60:02d}:{total % 60:02d}"


class OceanLyricWindow:
    """
    Jendela pop-up lirik yang muncul lembut di bagian bawah layar (fade-in mulus)
    dan melayang naik pelan-pelan secara seamless tanpa sentakan kencang.
    """
    def __init__(self, master, item, spawn_x, screen_h):
        self.master = master
        self.spawn_sec = item["start"]
        self.type_end_sec = item["type_end"]
        self.end_sec = item["end"]
        self.raw_text = item["raw_text"]
        self.full_text = item["text"]
        self.char_delay = item["char_delay"]
        self.indo_sub = item["indo"]
        self.header_title = item["title"]
        self.theme_key = item["theme"]
        self.theme = THEMES.get(self.theme_key, THEMES["CYAN"])
        self.duration = max(0.8, self.end_sec - self.spawn_sec)
        self.has_kw = any(kw in self.full_text.lower() for kw in KEYWORDS)

        # Ukuran kartu yang proporsional & rapi
        self.box_w = 410
        self.box_h = 175
        self.w = self.box_w - 4
        self.h = self.box_h - 4
        self.screen_h = screen_h

        # Titik dasar awal: Tepat di atas batas taskbar/layar bawah
        self.base_x = float(spawn_x)
        self.x = float(spawn_x)
        self.start_y = float(self.screen_h - self.box_h - 15)
        self.y = self.start_y

        self.phase = random.uniform(0, math.pi * 2)
        self.destroyed = False

        self.win = tk.Toplevel(master)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 0.05)  # Awalnya transparan untuk fade-in lembut
        self.win.configure(bg=self.theme["border"])
        self.win.geometry(f"{self.box_w}x{self.box_h}+{int(self.x)}+{int(self.y)}")

        self.canvas = tk.Canvas(
            self.win,
            width=self.w,
            height=self.h,
            bg=self.theme["card_bg"],
            highlightthickness=0
        )
        self.canvas.pack(padx=2, pady=2, fill="both", expand=True)

        self._build_canvas_items()

        self._drag_x = 0
        self._drag_y = 0
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)

    def _build_canvas_items(self):
        c = self.canvas
        w, h = self.w, self.h
        t = self.theme

        # Gelombang air laut bawah
        self.wave1_id = c.create_polygon([0, h, w, h], fill=t["wave1"], outline="")
        self.wave2_id = c.create_polygon([0, h, w, h], fill=t["wave2"], outline="")

        # Gelembung udara
        self.bubbles = []
        for _ in range(5):
            bx = random.uniform(20, w - 20)
            by = random.uniform(35, h - 12)
            r = random.uniform(2.0, 4.2)
            cid = c.create_oval(bx - r, by - r, bx + r, by + r, outline=t["accent"], width=1)
            self.bubbles.append({"id": cid, "x": bx, "y": by, "r": r, "speed": random.uniform(18.0, 36.0)})

        # Header bar rapi
        c.create_rectangle(0, 0, w, 32, fill=t["bg"], outline="")
        c.create_line(0, 32, w, 32, fill=t["border"], width=1)

        # Indikator piringan vinyl berputar
        vcx, vcy = 18, 16
        c.create_oval(vcx - 9, vcy - 9, vcx + 9, vcy + 9, fill="#09060d", outline=t["border"], width=1.5)
        self.vinyl_line_id = c.create_line(vcx, vcy, vcx + 6, vcy, fill=t["accent"], width=1.5)
        c.create_oval(vcx - 2.5, vcy - 2.5, vcx + 2.5, vcy + 2.5, fill=t["border"], outline="")

        c.create_text(34, 16, anchor="w", text=self.header_title, font=("Segoe UI", 8, "bold"), fill=t["accent"])

        c.create_rectangle(w - 52, 6, w - 8, 26, fill=t["wave1"], outline=t["border"])
        self.clock_id = c.create_text(w - 30, 16, text=format_spotify_clock(self.spawn_sec), font=("Consolas", 8, "bold"), fill="#ffffff")

        # Teks lirik bahasa Inggris (Utama)
        en_y = 74
        self.en_shadow_id = c.create_text(
            w // 2 + 1, en_y + 1, text="", font=("Segoe UI", 14, "bold"),
            fill="#05030a", width=w - 30, justify="center"
        )
        self.en_text_id = c.create_text(
            w // 2, en_y, text="", font=("Segoe UI", 14, "bold"),
            fill=t["text"], width=w - 30, justify="center"
        )

        # Teks terjemahan bahasa Indonesia
        id_y = 120
        c.create_text(
            w // 2 + 1, id_y + 1, text=f"“{self.indo_sub}”", font=("Segoe UI", 9, "italic"),
            fill="#05030a", width=w - 32, justify="center"
        )
        c.create_text(
            w // 2, id_y, text=f"“{self.indo_sub}”", font=("Segoe UI", 9, "italic"),
            fill=t["sub"], width=w - 32, justify="center"
        )

        # Equalizer bar & progress bar
        self.eq_ids = []
        eq_y = h - 8
        for bi in range(10):
            bx = 14 + bi * 7
            lid = c.create_line(bx, eq_y, bx, eq_y - 4, fill=t["border"], width=2.5)
            self.eq_ids.append((bx, lid))

        self.bar_x1 = 96
        self.bar_w = w - 110
        c.create_rectangle(self.bar_x1, h - 11, self.bar_x1 + self.bar_w, h - 8, fill=t["bg"], outline="")
        self.prog_id = c.create_rectangle(self.bar_x1, h - 11, self.bar_x1, h - 8, fill=t["border"], outline="")

    def _on_drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag_motion(self, event):
        self.base_x += (event.x - self._drag_x)
        self.y += (event.y - self._drag_y)

    def get_synced_text(self, song_sec):
        elapsed = max(0.0, song_sec - self.spawn_sec)
        n_chars = int(elapsed / max(0.01, self.char_delay)) + 1
        if n_chars >= len(self.raw_text):
            return self.full_text, True
        return self.raw_text[:n_chars], False

    def update_frame(self, dt, song_sec, audio_level=0.5):
        if self.destroyed:
            return

        age = max(0.0, song_sec - self.spawn_sec)

        # ── Gerak Melayang Naik Pelan & Konstan (Seamless, tanpa loncatan) ──
        # Kartu naik secara teratur 40px/detik dari posisi awal di bawah
        self.y = self.start_y - (RISE_SPEED * age)
        sway = math.sin(age * WAVE_SWAY_FREQ + self.phase) * WAVE_SWAY_AMP
        self.x = self.base_x + sway

        # ── Fade-In Halus Saat Muncul & Fade-Out di Bagian Paling Atas ──
        if age < 0.6:
            # Transisi fade-in lembut dari 0.05 ke 0.95 dalam 0.6 detik
            alpha = min(0.95, 0.05 + 0.90 * (age / 0.6))
        elif self.y < 120:
            # Fade-out perlahan saat mendekati batas atas layar
            alpha = max(0.0, min(0.95, self.y / 120.0 * 0.95))
        else:
            alpha = 0.95

        try:
            self.win.attributes("-alpha", alpha)
            self.win.geometry(f"{self.box_w}x{self.box_h}+{int(self.x)}+{int(self.y)}")
        except tk.TclError:
            self.destroyed = True
            return

        c = self.canvas
        w, h = self.w, self.h
        t = self.theme

        # Update teks lirik
        curr_str, is_done = self.get_synced_text(song_sec)
        cursor = "▍" if not is_done and int(song_sec * 8) % 2 == 0 else ""
        disp = curr_str + cursor
        txt_col = t["highlight"] if (self.has_kw and is_done) else t["text"]

        c.itemconfig(self.en_shadow_id, text=disp)
        c.itemconfig(self.en_text_id, text=disp, fill=txt_col)

        # Update animasi gelombang air laut & equalizer
        boost = 1.0 + audio_level * 0.7
        for wid, amp, speed, y_base in [
            (self.wave1_id, 6.0 * boost, 3.2, h - 30),
            (self.wave2_id, 4.0 * boost, -4.2, h - 16),
        ]:
            pts = [0, h]
            for px in range(0, w + 32, 32):
                py = y_base + math.sin((px * 0.04) + (age * speed) + self.phase) * amp
                pts.extend([px, py])
            pts.extend([w, h])
            c.coords(wid, *pts)

        for b in self.bubbles:
            b["y"] -= b["speed"] * dt * boost
            if b["y"] < 32:
                b["y"] = h - 4
                b["x"] = random.uniform(18, w - 18)
            r = b["r"]
            c.coords(b["id"], b["x"] - r, b["y"] - r, b["x"] + r, b["y"] + r)

        angle = song_sec * 4.0 + self.phase
        c.coords(self.vinyl_line_id, 18, 16, 18 + math.cos(angle) * 6, 16 + math.sin(angle) * 6)
        c.itemconfig(self.clock_id, text=format_spotify_clock(song_sec))

        eq_y = h - 8
        for bi, (bx, lid) in enumerate(self.eq_ids):
            wave_mod = abs(math.sin(age * 7.5 + bi * 0.65))
            bar_h = 2.5 + (wave_mod * 4.5) + (audio_level * 8.0 * wave_mod)
            c.coords(lid, bx, eq_y, bx, eq_y - bar_h)

        line_prog = min(1.0, max(0.0, age / self.duration))
        c.coords(self.prog_id, self.bar_x1, h - 11, self.bar_x1 + int(self.bar_w * line_prog), h - 8)

    def is_offscreen(self):
        return self.y + self.box_h < -20 or self.destroyed

    def destroy(self):
        self.destroyed = True
        try:
            self.win.destroy()
        except tk.TclError:
            pass


class OverboardAutoShowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✦ DROWNING IN LOVE • LIVE LYRICS ✦")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        hud_w, hud_h = 360, 50
        hud_x = self.screen_w - hud_w - 24
        hud_y = self.screen_h - hud_h - 68
        self.root.geometry(f"{hud_w}x{hud_h}+{hud_x}+{hud_y}")
        self.root.configure(bg="#c77dff")

        self.audio_clock = HardwareAudioClock(WAV_FILE)
        self.envelope = load_audio_envelope(WAV_FILE, step_sec=0.05)
        self.windows = []
        self.next_idx = 0
        self.side_toggle = 0
        self.is_running = True

        self._drag_x = 0
        self._drag_y = 0

        self.build_mini_hud()
        self.root.bind("<Escape>", lambda e: self.quit_app())
        self.root.bind("<r>", lambda e: self.restart_show())
        self.root.bind("<R>", lambda e: self.restart_show())

        self.root.after(40, self.start_immediately)

    def build_mini_hud(self):
        frame = tk.Frame(self.root, bg="#1a0926")
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        frame.bind("<ButtonPress-1>", self._start_move)
        frame.bind("<B1-Motion>", self._do_move)

        self.lbl_title = tk.Label(
            frame,
            text="✦  M Y   L I F E S A V E R  •  L I V E",
            font=("Segoe UI", 9, "bold"),
            bg="#1a0926", fg="#e0aaff"
        )
        self.lbl_title.pack(side="left", padx=(10, 6))
        self.lbl_title.bind("<ButtonPress-1>", self._start_move)
        self.lbl_title.bind("<B1-Motion>", self._do_move)

        self.lbl_time = tk.Label(
            frame,
            text="02:17 / 03:11",
            font=("Consolas", 9, "bold"),
            bg="#1a0926", fg="#ffd166"
        )
        self.lbl_time.pack(side="left", padx=4)

        btn_replay = tk.Button(
            frame, text="↻", font=("Segoe UI", 9, "bold"),
            bg="#3c1654", fg="#72efdd", relief="flat", bd=0,
            padx=7, pady=2, cursor="hand2", command=self.restart_show
        )
        btn_replay.pack(side="left", padx=4)

        btn_quit = tk.Button(
            frame, text="✕", font=("Segoe UI", 9, "bold"),
            bg="#4d1645", fg="#ff4d8d", relief="flat", bd=0,
            padx=7, pady=2, cursor="hand2", command=self.quit_app
        )
        btn_quit.pack(side="right", padx=6)

    def _start_move(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_move(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def start_immediately(self):
        self.next_idx = 0
        self.side_toggle = 0
        self.audio_clock.start()
        self.last_perf = time.perf_counter()
        self.tick()

    def restart_show(self):
        for w in self.windows:
            w.destroy()
        self.windows.clear()
        self.start_immediately()

    def choose_spawn_x(self):
        """
        Dua kolom simetris di tengah layar monitor (Kiri & Kanan),
        menghindari tabrakan dan tampak seimbang dan rapi.
        """
        center_x = self.screen_w // 2
        box_w = 410
        gap = 25
        if self.side_toggle % 2 == 0:
            x = center_x - box_w - gap
        else:
            x = center_x + gap
        self.side_toggle += 1
        return max(15, min(self.screen_w - box_w - 15, x))

    def get_current_audio_level(self, song_sec):
        if not self.envelope:
            return 0.5
        idx = int(song_sec / 0.05)
        if 0 <= idx < len(self.envelope):
            return self.envelope[idx]
        return 0.2

    def tick(self):
        if not self.is_running:
            return

        now = time.perf_counter()
        dt = now - self.last_perf
        self.last_perf = now

        song_sec = self.audio_clock.get_time_sec()

        shown_sec = min(song_sec, TOTAL_DURATION)
        self.lbl_time.config(text=f"{format_spotify_clock(shown_sec)} / 03:11")

        # Munculkan jendela baru saat waktunya tiba (muncul halus dari bawah)
        while (
            self.next_idx < len(lyrics)
            and lyrics[self.next_idx]["start"] <= song_sec
        ):
            item = lyrics[self.next_idx]
            sx = self.choose_spawn_x()
            card = OceanLyricWindow(self.root, item, sx, self.screen_h)
            self.windows.append(card)
            self.next_idx += 1

        audio_lvl = self.get_current_audio_level(song_sec)

        still_alive = []
        for card in self.windows:
            card.update_frame(dt, song_sec, audio_level=audio_lvl)
            if card.is_offscreen():
                card.destroy()
            else:
                still_alive.append(card)
        self.windows = still_alive

        if song_sec < TOTAL_DURATION + 6.5 or self.windows:
            self.root.after(15, self.tick)

    def quit_app(self):
        self.is_running = False
        self.audio_clock.stop()
        for card in self.windows:
            card.destroy()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OverboardAutoShowApp(root)
    root.mainloop()

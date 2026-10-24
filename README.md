# 🌊 Overboard — Justin Bieber ft. Jessica Jarrell
### *Aesthetic Floating Lyric Windows in Python (Cyber-Ocean Edition)*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![TikTok](https://img.shields.io/badge/TikTok-Live%20Demo-EE1D52?style=for-the-badge&logo=tiktok&logoColor=white)](https://www.tiktok.com/@noturjir0/video/7699927615372627201)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External%20Pip-4CAF50?style=for-the-badge)]()

A modern, highly-polished desktop Floating Lyric Windows experience in Python. Inspired by viral TikTok desktop floating lyric videos, but upgraded with custom ocean-glassmorphism, hardware-synchronized audio timing, dual-column choreography, and buttery-smooth slow upward drift.

---

## 📱 Live Demo (TikTok)

Lihat tampilan live demo animasi di TikTok melalui tautan berikut:

👉 **[Tonton Live Demo di TikTok (@noturjir0)](https://www.tiktok.com/@noturjir0/video/7699927615372627201)**

---

## ✨ Fitur Utama

- **🌊 Seamless, Slow & Gentle Drift Animation:**
  - Jendela lirik **tidak muncul tiba-tiba di tengah layar**, melainkan muncul lembut dari bagian paling bawah monitor dengan efek *smooth fade-in* (0.05 ke 0.95).
  - Melayang naik secara perlahan dan konstan (`40 px/detik`), bebas dari sentakan mendadak.
  - Menghilang perlahan (*soft fade-out*) saat mencapai puncak layar (`y < 120`).

- **⏱️ Hardware Audio Synchronization (0-Drift):**
  - Menggunakan Windows Multimedia API (`winmm.dll`) bawaan untuk membaca posisi milidetik audio langsung dari *sound card hardware*.
  - Musik dan teks lirik 100% presisi tanpa jeda *loading* atau *drift*.

- **🎨 Glassmorphic Ocean Theme & Typography:**
  - Desain kartu bergaya *cyber-ocean / glassmorphism* dengan border neon bercahaya.
  - Dilengkapi teks utama bahasa Inggris bergaya *typewriter* dan terjemahan bahasa Indonesia di bawahnya.
  - Kata-kata emosional (*overboard, drowning, lifesaver, water, love*) otomatis bersinar terang (*glow highlight*).

- **🎧 Audio-Reactive Equalizer & Vinyl Disc:**
  - Equalizer bar di bagian bawah kartu bergerak dinamis mengikuti level energi ketukan musik asli.
  - Animasi piringan vinyl mini berputar di header bar dan indikator pill waktu lagu ala Spotify.

- **🚀 Zero External Dependencies:**
  - Berjalan langsung di Python standar (versi 3.8 ke atas di Windows).
  - Menggunakan modul standar bawaan Python: `tkinter`, `ctypes`, `wave`, `struct`, `math`, `time`, `random`, dan `os`. Tidak perlu `pip install`.

---

## 📁 Struktur Direktori

```text
Overboard-Justin-Bieber/
├── .env.example                # Template konfigurasi environment
├── .gitignore                  # File filter git (mengabaikan video/cache)
├── overboard.mp3               # Audio lagu kompresi (Overboard)
├── overboard_floating_windows.py # Kode Python utama
├── overboard_vt.wav            # Audio WAV tanpa kompresi untuk pemutar Windows
├── README.md                   # Dokumentasi proyek & link live demo
├── requirements.txt            # Catatan dependency (0 external pip)
└── run_overboard.bat           # Launcher one-click untuk Windows
```

---

## 🚀 Cara Menjalankan

### Cara 1: One-Click Launcher (Paling Mudah)
Cukup klik dua kali file **`run_overboard.bat`** di Windows Explorer.

### Cara 2: Lewat Command Prompt / PowerShell
1. Pastikan Python 3.8+ sudah terinstal di Windows Anda.
2. Clone repository ini:
   ```powershell
   git clone https://github.com/v0rade/Overboard-Justin-Bieber.git
   cd Overboard-Justin-Bieber
   ```
3. Jalankan script:
   ```powershell
   python overboard_floating_windows.py
   ```

---

## ⌨️ Kontrol Keyboard & Mouse

| Aksi | Fungsi |
| :--- | :--- |
| **Klik & Drag Mouse** | Menggeser kartu lirik yang sedang melayang secara bebas di desktop |
| **Tekan `R`** | Mengulang animasi dan musik dari awal (*Restart*) |
| **Tekan `Esc`** | Menutup semua jendela lirik dan keluar aplikasi |
| **Mini HUD Controller** | Dock kecil di pojok kanan bawah dengan tombol replay (↻) dan tutup (✕) |

---

## ⚙️ Kustomisasi

Anda dapat menyesuaikan parameter animasi di [overboard_floating_windows.py](overboard_floating_windows.py) atau lewat file `.env`:

```ini
# Kecepatan melayang naik (makin kecil makin pelan & santai)
RISE_SPEED=40.0

# Amplitudo & frekuensi ayunan gelombang ombak
WAVE_SWAY_AMP=8.0
WAVE_SWAY_FREQ=1.3

# Jeda waktu vokal awal (detik)
INITIAL_DELAY=0.70
```

---

## 🎵 Kredit & Inspirasi

- **Lagu:** *Overboard* — Justin Bieber ft. Jessica Jarrell (*My World 2.0*, 2010)
- **Live Demo:** [@noturjir0 di TikTok](https://www.tiktok.com/@noturjir0/video/7699927615372627201)
- **Inspirasi Animasi:** Floating Lyric Windows Community & Creator TikTok

---

⭐ **Jika Anda menyukai proyek ini, silakan berikan bintang (Star) di repository ini!**

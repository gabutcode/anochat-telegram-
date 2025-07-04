# 🤖 Anochat Telegram Bot

**Anochat** adalah bot Telegram Anonymous Chat yang memungkinkan pengguna untuk terhubung secara acak dengan orang lain berdasarkan gender. Bot ini juga dilengkapi fitur Premium, media (foto dan suara), serta admin tools untuk monitoring pengguna.

Bot ini dibuat untuk digunakan di Termux atau server Linux ringan, cocok untuk komunitas atau project pribadi.

---

## ✨ Fitur Utama

- Chat anonymous berdasarkan gender (Cowok / Cewek)
- Kirim pesan teks, gambar, dan voice note
- Fitur Premium (unlock media tanpa batas, prioritas match)
- Panel admin langsung dari bot untuk cek user, partner, dan data lainnya
- Penyimpanan media lokal (terpisah per user)
- Tidak perlu database eksternal (menggunakan SQLite bawaan)

---

## 🔧 Cara Instalasi (di Termux)

1. **Install Termux** dari F-Droid atau Play Store.
2. Buka Termux dan jalankan:
   ```bash
   pkg update && pkg upgrade
   pkg install git python -y
git clone https://github.com/gabutcode/anochat-telegram-.git
cd anochat-telegram-
pip install -r requirements.txt
python bot.py

jangan lupa untuk edit token dan id
TOKEN = "ISI_TOKEN_BOT_KAMU"
ADMIN_ID = 123456789

📌 Catatan

Bot ini tidak menyimpan isi chat

Semua foto dan VN hanya disimpan untuk admin monitoring

Gunakan dengan bijak. Bot ini bukan untuk spam, scam, atau penyalahgunaan lainnya.

📜 Lisensi

Dikembangkan oleh GabutCode
Bebas digunakan untuk pembelajaran dan proyek pribadi.
Tidak diperbolehkan untuk komersialisasi tanpa izin.

# 🤖 Anochat Telegram Bot

Anochat adalah bot Telegram chat anonim yang menghubungkan pengguna secara acak dengan orang lain berdasarkan gender (cowok atau cewek).
Bot ini mendukung pengiriman pesan teks, gambar, dan voice note, serta menyediakan fitur Premium dan panel admin langsung dari bot.
Dirancang agar bisa dijalankan langsung di Termux Android atau server kecil tanpa setup rumit.

---

## 🚀 Cara Pasang & Jalankan Bot (di Termux Android)

```bash
pkg update && pkg upgrade
pkg install git python -y
git clone https://github.com/gabutcode/anochat-telegram-.git
cd anochat-telegram-
pip install -r requirements.txt
```

Edit file `bot.py`, ganti:

```python
TOKEN = "ISI_TOKEN_BOT_KAMU"
ADMIN_ID = 123456789
```

Lalu jalankan bot:
```bash
python bot.py
```

Jika muncul error `RuntimeError: This event loop is already running`, ubah bagian akhir `bot.py` menjadi:

```python
import nest_asyncio
nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())
```

---

## 💬 Perintah untuk Pengguna

| Perintah | Fungsi |
|----------|--------|
| /start   | Mulai bot & pilih gender |
| /next    | Cari partner |
| /stop    | Keluar dari chat |
| /cekpremium | Cek status Premium |
| /donate  | Info donasi |

---

## 🔐 Perintah Admin

| Perintah | Fungsi |
|----------|--------|
| /addpremium <id>    | Jadikan user Premium |
| /removepremium <id> | Cabut status Premium |
| /listusers          | Lihat semua user |
| /userinfo <id>      | Lihat detail user |

---

## 📁 Struktur Folder

- `bot.py`             → Bot utama
- `database.db`        → Data user
- `media/photo/`       → Foto user
- `media/voice/`       → VN user
- `requirements.txt`   → Kebutuhan Python

---

## 💰 Dukungan & Premium

Premium membuka:
- Kirim media tanpa batas
- Prioritas dalam pencarian partner

Donasi: [https://trakteer.id/gabutcode](https://trakteer.id/gabutcode)

---

## 👨‍💻 Developer

GabutCode  
GitHub: [https://github.com/gabutcode](https://github.com/gabutcode)

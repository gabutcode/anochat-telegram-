## 🚀 Cara Pasang & Jalankan Bot Anochat (di Termux Android)

Ikuti langkah-langkah berikut untuk menjalankan bot ini di HP Android menggunakan Termux:

### 1. Instal Termux

- Disarankan pakai Termux dari [F-Droid](https://f-droid.org/en/packages/com.termux/)
- Jangan install dari Play Store, karena versinya sudah tidak update

---

### 2. Update & Pasang Git dan Python

```bash
pkg update && pkg upgrade
pkg install git python -y


---

3. Clone Project dari GitHub

git clone https://github.com/gabutcode/anochat-telegram-.git
cd anochat-telegram-


---

4. Pasang Semua Kebutuhan Python

pip install -r requirements.txt


---

5. Edit Token Bot dan ID Admin

Buka file bot.py dan ubah bagian ini:

TOKEN = "ISI_TOKEN_BOT_KAMU"
ADMIN_ID = 123456789  # Ganti dengan ID Telegram kamu

> Untuk tahu ID kamu, kamu bisa cek pakai bot: @userinfobot




---

6. Jalankan Bot

python bot.py

Kalau muncul error seperti ini:

RuntimeError: This event loop is already running

Maka ubah bagian paling bawah bot.py menjadi:

import nest_asyncio
nest_asyncio.apply()
asyncio.get_event_loop().run_until_complete(main())


---

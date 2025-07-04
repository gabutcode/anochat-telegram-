🤖 Anochat Telegram Bot

Anochat adalah bot Telegram chat anonim yang menghubungkan pengguna secara acak dengan orang lain berdasarkan gender (cowok atau cewek).
Bot ini mendukung pengiriman pesan teks, gambar, dan voice note, serta menyediakan fitur Premium dan panel admin langsung dari bot.
Dirancang agar bisa dijalankan langsung di Termux Android atau server kecil tanpa setup rumit.

============================
📦 Cara Pasang Bot di Termux
============================

1. Update & Pasang Git dan Python:
   pkg update && pkg upgrade
   pkg install git python -y

2. Clone project dari GitHub:
   git clone https://github.com/gabutcode/anochat-telegram-.git
   cd anochat-telegram-

3. Install kebutuhan bot:
   pip install -r requirements.txt

4. Edit file bot.py
   Ganti:
     TOKEN = "ISI_TOKEN_BOT_KAMU"
     ADMIN_ID = 123456789
   dengan token bot dan ID Telegram kamu

5. Jalankan bot:
   python bot.py

Jika error "event loop is already running",
ganti bagian bawah bot.py dengan:
   import nest_asyncio
   nest_asyncio.apply()
   asyncio.get_event_loop().run_until_complete(main())

============================
📋 Perintah Utama (User)
============================
/start        → Mulai bot & pilih gender
/next         → Cari partner
/stop         → Keluar dari chat
/cekpremium   → Cek status Premium
/donate       → Info donasi

============================
🔐 Perintah Admin
============================
/addpremium <id>      → Jadikan user Premium
/removepremium <id>   → Cabut Premium
/listusers            → Lihat semua user
/userinfo <id>        → Detail user

============================
📁 Folder & File Penting
============================
- bot.py             = Bot utama
- database.db        = Data user
- media/photo/       = Foto user
- media/voice/       = VN user
- requirements.txt   = Daftar lib Python

============================
💡 Info Lain
============================
- Donasi: https://trakteer.id/gabutcode
- Developer: github.com/gabutcode

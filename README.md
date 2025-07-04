## Anochat bot telegram 

Anochat adalah bot Telegram chat anonim yang menghubungkan pengguna secara acak dengan orang lain berdasarkan gender (cowok atau cewek).  
Bot ini mendukung pengiriman pesan teks, gambar, dan voice note, serta menyediakan fitur Premium dan panel admin langsung dari bot.  
Dirancang agar bisa dijalankan langsung di Termux Android atau server kecil tanpa setup rumit.

### Update & Pasang Git dan Python

pkg update && pkg upgrade
pkg install git python -y
git clone https://github.com/gabutcode/anochat-telegram-.git
cd anochat-telegram-
pip install -r requirements.txt
python bot.py

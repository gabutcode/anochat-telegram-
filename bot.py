import asyncio
import aiosqlite
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from pathlib import Path
from datetime import datetime

TOKEN = "ISI_TOKEN_BOT_KAMU"
ADMIN_ID = 123456789
DB_PATH = "database.db"

GENDER_KEYBOARD = ReplyKeyboardMarkup(
    [["Cowok", "Cewek"]],
    one_time_keyboard=True,
    resize_keyboard=True
)

MEDIA_PATH = Path("media")
PHOTO_PATH = MEDIA_PATH / "photo"
VOICE_PATH = MEDIA_PATH / "voice"
PHOTO_PATH.mkdir(parents=True, exist_ok=True)
VOICE_PATH.mkdir(parents=True, exist_ok=True)

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                gender TEXT,
                partner_id INTEGER,
                is_premium INTEGER DEFAULT 0,
                has_sent_media INTEGER DEFAULT 0,
                note TEXT
            )
        """)
        await db.commit()

async def get_partner(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("SELECT partner_id FROM users WHERE user_id = ?", (user_id,))
        return row[0] if row else None

async def remove_partner(user_id):
    partner_id = await get_partner(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET partner_id = NULL WHERE user_id = ?", (user_id,))
        if partner_id:
            await db.execute("UPDATE users SET partner_id = NULL WHERE user_id = ?", (partner_id,))
        await db.commit()
    return partner_id

async def get_gender(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("SELECT gender FROM users WHERE user_id = ?", (user_id,))
        return row[0] if row else None

async def check_premium(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("SELECT is_premium FROM users WHERE user_id = ?", (user_id,))
        return row[0] == 1 if row else False

async def has_sent_media(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("SELECT has_sent_media FROM users WHERE user_id = ?", (user_id,))
        return row[0] == 1 if row else False

async def mark_sent_media(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET has_sent_media = 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def find_partner(user_id):
    gender = await get_gender(user_id)
    if not gender:
        return None
    target = "cewek" if gender == "cowok" else "cowok"
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("""
            SELECT user_id FROM users
            WHERE partner_id IS NULL AND gender = ? AND user_id != ?
            LIMIT 1
        """, (target, user_id))
        if row:
            pid = row[0]
            await db.execute("UPDATE users SET partner_id = ? WHERE user_id = ?", (pid, user_id))
            await db.execute("UPDATE users SET partner_id = ? WHERE user_id = ?", (user_id, pid))
            await db.commit()
            return pid
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (uid,))
        await db.commit()
    await update.message.reply_text("Halo! Kamu cowok atau cewek?", reply_markup=GENDER_KEYBOARD)

async def message_handler_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.lower()
    if text in ["cowok", "cewek"]:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE users SET gender = ?, has_sent_media = 0 WHERE user_id = ?", (text, uid))
            await db.commit()
        await update.message.reply_text("Gender disimpan. Gunakan /next untuk cari partner.")
    else:
        await message_handler(update, context)

async def next_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    old = await remove_partner(uid)
    if old:
        await context.bot.send_message(old, "Partner meninggalkan obrolan.")
    pid = await find_partner(uid)
    if pid:
        await update.message.reply_text("Partner ditemukan! Mulai chat.")
        await context.bot.send_message(pid, "Partner ditemukan! Mulai chat.")
    else:
        await update.message.reply_text("Belum ada partner, menunggu...")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    pid = await remove_partner(uid)
    if pid:
        await context.bot.send_message(pid, "Partner meninggalkan obrolan.")
    await update.message.reply_text("Obrolan dihentikan.")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\ud83d\udc96 Donasi: https://trakteer.id/gabutcode")

async def cekpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    status = await check_premium(uid)
    await update.message.reply_text("\u2705 Premium" if status else "\u274c Belum Premium")

async def addpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args: return await update.message.reply_text("Gunakan: /addpremium <user_id>")
    uid = int(context.args[0])
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET is_premium = 1 WHERE user_id = ?", (uid,))
        await db.commit()
    await update.message.reply_text("User premium ditambahkan.")

async def listusers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    async with aiosqlite.connect(DB_PATH) as db:
        rows = await db.execute_fetchall("SELECT user_id, gender, is_premium, partner_id FROM users")
        text = "\n".join([f"{r[0]} | {r[1]} | {'\u2705' if r[2] else '\u274c'} | Partner: {r[3]}" for r in rows])
    await update.message.reply_text(text or "Tidak ada pengguna.")

async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args: return await update.message.reply_text("Gunakan: /userinfo <user_id>")
    uid = int(context.args[0])
    async with aiosqlite.connect(DB_PATH) as db:
        row = await db.execute_fetchone("SELECT * FROM users WHERE user_id = ?", (uid,))
        if not row:
            return await update.message.reply_text("User tidak ditemukan.")
        text = f"ID: {row[0]}\nGender: {row[1]}\nPartner: {row[2]}\nPremium: {'Ya' if row[3] else 'Tidak'}\nKirim media: {'Ya' if row[4] else 'Tidak'}\nNote: {row[5] or '-'}"
        await update.message.reply_text(text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    pid = await get_partner(uid)
    if pid:
        await context.bot.send_message(pid, update.message.text)
    else:
        await update.message.reply_text("Gunakan /next untuk mulai chat.")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    pid = await get_partner(uid)
    if pid:
        photo = update.message.photo[-1]
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = PHOTO_PATH / str(uid)
        folder.mkdir(exist_ok=True)
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive(folder / f"{now}.jpg")
        await context.bot.send_photo(pid, photo.file_id)
        await mark_sent_media(uid)

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    pid = await get_partner(uid)
    if pid:
        voice = update.message.voice
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = VOICE_PATH / str(uid)
        folder.mkdir(exist_ok=True)
        file = await context.bot.get_file(voice.file_id)
        await file.download_to_drive(folder / f"{now}.ogg")
        await context.bot.send_voice(pid, voice.file_id)
        await mark_sent_media(uid)

async def main():
    await init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", next_cmd))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("cekpremium", cekpremium))
    app.add_handler(CommandHandler("addpremium", addpremium))
    app.add_handler(CommandHandler("listusers", listusers))
    app.add_handler(CommandHandler("userinfo", userinfo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_gender))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    await app.run_polling()

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

if __name__ == "__main__":
    asyncio.run(main())

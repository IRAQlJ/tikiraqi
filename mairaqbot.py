import telebot
import requests
import os
import uuid

# -------------------- تكوين البوت --------------------
TOKEN = "7851333119:AAGDrK_kgYdU9p97ME7UxIAd6eWJaWe_cdQ"
CHANNEL_USERNAME = "TikIraqi"
SHARE_BOT_LINK = "https://t.me/TikIRAQlbot"
LINKS_FILE = "saved_links.txt"
STATS_FILE = "stats.txt"
USERS_FILE = "users.txt"

bot = telebot.TeleBot(TOKEN)

# -------------------- دوال مساعدة --------------------

def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def increase_download_count():
    count = 0
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            try:
                count = int(f.read().strip())
            except:
                count = 0
    count += 1
    with open(STATS_FILE, "w") as f:
        f.write(str(count))
    return count

def get_download_count():
    if not os.path.exists(STATS_FILE):
        return 0
    with open(STATS_FILE, "r") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def save_link(user_id, link):
    with open(LINKS_FILE, "a") as f:
        f.write(f"{user_id}: {link}\n")

def get_user_links(user_id):
    if not os.path.exists(LINKS_FILE):
        return []
    with open(LINKS_FILE, "r") as f:
        lines = f.readlines()
    user_lines = [line.split(": ", 1)[1].strip() for line in lines if line.startswith(str(user_id))]
    return user_lines[-10:]

def delete_user_links(user_id):
    if not os.path.exists(LINKS_FILE):
        return False
    with open(LINKS_FILE, "r") as f:
        lines = f.readlines()
    new_lines = [line for line in lines if not line.startswith(str(user_id))]
    with open(LINKS_FILE, "w") as f:
        f.writelines(new_lines)
    return True

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")

def get_total_users():
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, "r") as f:
        return len(f.read().splitlines())

user_states = {}

# -------------------- أمر /start --------------------

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    save_user(user_id)

    if not is_user_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔔 اشترك بالقناة", url=f"https://t.me/{CHANNEL_USERNAME}"))
        bot.send_message(
            message.chat.id,
            "🔒 للاسف لازم تشترك بقناتنا أولاً حتى تقدر تستخدم البوت 💡\n"
            "👇 اضغط الزر واشترك وارجع ارسل /start من جديد:",
            reply_markup=markup
        )
        return

    caption = (
        "🎉 <b>هلاااا بيك ببوت التحميل من TikTok</b>\n\n"
        "🎥 اضغط على زر (🎬 تحميل فديو) لتحميل فيديو من TikTok بدون علامة مائية.\n"
        "🎵 اضغط على زر (🎵 تحويل الى صوت) لتحويل فيديو سبق إرساله إلى مقطع صوتي.\n"
        "📥 روابطك تنخزن وتكدر ترجعلهن من زر (📂 روابطي)\n\n"
        f"📊 عدد التنزيلات الكلي: <b>{get_download_count()}</b>\n"
        f"👤 عدد مستخدمين البوت: <b>{get_total_users()}</b>\n"
        "⚒️ المطور: <a href='https://t.me/IR_A_Ql'>@IR_A_Ql</a>"
    )

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("📂 روابطي", callback_data="my_links"),
        telebot.types.InlineKeyboardButton("🗑️ حذف روابطي", callback_data="delete_links")
    )
    markup.row(
        telebot.types.InlineKeyboardButton("🎬 تحميل فديو", callback_data="download_video"),
        telebot.types.InlineKeyboardButton("🎵 تحويل الى صوت", callback_data="convert_to_audio")
    )
    markup.add(telebot.types.InlineKeyboardButton("🔗 مشاركة البوت", url=SHARE_BOT_LINK))

    bot.send_message(
        message.chat.id,
        caption,
        parse_mode="HTML",
        reply_markup=markup
    )

# -------------------- تشغيل البوت --------------------

if __name__ == "__main__":
    print("✅ Bot is running...")
    bot.infinity_polling()
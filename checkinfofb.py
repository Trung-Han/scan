import telebot
import requests
import json
from telebot import types

# 🔑 TOKEN BOT
TOKEN = "7528656365:AAGBik2_e6glb1JL_YunzN7JWP4bOhRFJ1w"
bot = telebot.TeleBot(TOKEN)

# ==========================
# LỆNH /fb
# ==========================
@bot.message_handler(commands=['fb'])
def get_facebook_info(message):
    try:
        parts = message.text.split(" ")
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Vui lòng nhập UID Facebook!\n\n👉 Ví dụ: /fb 4")
            return

        uid = parts[1]
        api_url = f"https://adidaphat.site/facebook/getinfo?uid={uid}&apikey=apikeysumi"
        res = requests.get(api_url)

        # 🧩 Dữ liệu trả về có thể là str JSON hoặc dict
        data = res.json()
        if isinstance(data, str):
            data = json.loads(data)

        if not isinstance(data, dict) or "name" not in data:
            bot.reply_to(message, "❌ Không tìm thấy thông tin người dùng này!")
            return

        # 🧠 Lấy dữ liệu
        name = data.get("name", "Không rõ")
        username = data.get("username", "Không có")
        link = data.get("link_profile", "Không rõ")
        gender = data.get("gender", "Không rõ")
        location = data.get("location", "Không rõ")
        follower = data.get("follower", 0)
        birthday = data.get("birthday", "Không rõ")
        relationship = data.get("relationship_status", "Không rõ")
        love = data.get("love", {}).get("name", "Không có") if isinstance(data.get("love"), dict) else "Không có"
        created = data.get("created_time", "Không rõ")
        quotes = data.get("quotes", "Không có")
        tichxanh = "✅ Có" if data.get("tichxanh") else "❌ Không"
        author = data.get("author", "")
        avatar_url = data.get("avatar")

        # 🧾 Nội dung hiển thị
        caption = (
            f"👤 <b>Thông tin Facebook</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🧩 Họ tên: <b>{name}</b>\n"
            f"🔗 Username: @{username}\n"
            f"🆔 UID: <code>{uid}</code>\n"
            f"🌐 Link: <a href='{link}'>Xem trang cá nhân</a>\n"
            f"📅 Ngày tạo: {created}\n"
            f"🎂 Sinh nhật: {birthday}\n"
            f"💑 Tình trạng: {relationship}\n"
            f"❤️ Người yêu: {love}\n"
            f"👫 Giới tính: {gender}\n"
            f"📍 Nơi ở: {location}\n"
            f"👥 Người theo dõi: {follower:,}\n"
            f"☑️ Tích xanh: {tichxanh}\n"
            f"💬 Quotes: {quotes}"
        )

        # 🖼️ Gửi avatar + caption
        bot.send_photo(message.chat.id, avatar_url, caption=caption, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi: {e}")

# ==========================
# KHỞI CHẠY BOT
# ==========================
print("🤖 Bot Facebook Info đang chạy... Lệnh: /fb <uid>")
bot.infinity_polling()
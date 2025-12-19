import telebot
import os
import subprocess
import datetime
import sqlite3
import psutil
import hashlib
import logging
import sys
import json
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
import tempfile
import os
from telegram.ext import CallbackContext
from telegram import Update, ChatMember
import qrcode
from telebot import types

ADMIN_ID = int(os.getenv("ADMIN_ID", "1322814990"))

bot_token = os.getenv("BOT_TOKEN", "7528656365:AAGBik2_e6glb1JL_YunzN7JWP4bOhRFJ1w") 
name_bot = "Phan Trọng Phúc Coder" 
zalo = "056.378.1006" #
allowed_group_id = int(os.getenv("ALLOWED_GROUP_ID", "-1002709505938")) 
admin = "@NgocLinh2x_CTV" 

bot = telebot.TeleBot(bot_token)
print("[BOT] Kết Nối Thành Công => Xin Chào  Cậu Chủ Phan Trọng Phúc")

logging.basicConfig(level=logging.INFO)

user_last_command_time = {}
COOLDOWN_PERIOD = datetime.timedelta(seconds=90)

processes = []

user_input_state = {}

connection = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def save_user_to_database(user_id, expiration_time):
    cursor.execute(
        '''
            INSERT OR REPLACE INTO users (user_id, expiration_time)
            VALUES (?, ?)
        ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S'))
    )
    connection.commit()

def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    allowed_users = []
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)
    return allowed_users

allowed_users = load_users_from_database()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    username = message.from_user.username
    xinchao = f"""<blockquote>Danh Sách Các Lệnh
╔==========[Xin Chào @{username}============╗
╠➤ /ff - Info Free Fire
╠➤ /fbid - Info Facebook
╠➤ /checkbanff - Ban Acc FF
╠➤ /tiktok - Info TikTok
╠======[VLXX]======
╠➤ /vdgai - Video Gái Xing
╠➤ /mong - Ảnh Mông
╠➤ /girl - Ảnh Girl
╠➤ /bu - Ảnh Bú
╠➤ /gainhat - Ảnh Gái Nhật
╠➤ /japcosplay - Ảnh Cosplay
╠➤ /tw - Ảnh Gái Tài Khựa
╠➤ /anime - Ảnh Anime
╠➤ /sagiri - Ảnh Sagiri
╠=====[Tiện Ích]======
╠➤ /ai - Tạo Ảnh AI
╠➤ /2fa - Get Key 2Fa
╠➤ /dich - En -> Vi
╠➤ /war - Spam Tin Nhắn Tele
╠➤ /src - Lấy Full Code Src + Tool + Bot
╠➤ /html - Lấy Html Trang Web
╠➤ /checkip - Để Check Ip 
╠➤ /qr - Để Tạo Qr = Chữ
╠➤ /cadao - Ca Dao Tục Ngữ
╠➤ /xsmb - Check Kết Quả Sổ Xố
╠➤ /thathinh - Thả Thính Boy & Girl
╠➤ /thoitiet - Thời Tiết Hôm Nay
╠➤ /weather - Thời Tiết 7 Ngày Qua 
╠➤ /voice - Để Đổi Text Thành Giọng Nói
╠➤ /info - Check ID Người Dùng 
╠➤ /doneta - Ủng Hộ AD
╚======[Copyright_By Phan Trọng Phúc] ======╝</blockquote>"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)  
    keyboard.add(
        types.InlineKeyboardButton("👤 Admin", url="https://t.me/NgocLinh2x_CTV"),
       

    video_url = "https://files.catbox.moe/xbgx14.mp4"
    bot.send_video(message.chat.id, video_url, caption=xinchao, parse_mode='HTML', reply_markup=keyboard)

  
# #Xoá Tin Nhắn /
# @bot.message_handler(func=lambda message: message.text.startswith("/"))
# def delete_command_message(message):
#     try:
#         bot.delete_message(message.chat.id, message.message_id)
#     except:
#         pass

# Gái
API_LIST = {
    "mong": "https://imgs-api.vercel.app/mong?apikey=mk001", #mong
    # "jack": "https://imgs-api.vercel.app/jack?apikey=mk001", #jack
    "girl": "https://imgs-api.vercel.app/girl?apikey=mk001", #girl
    "du": "https://imgs-api.vercel.app/du?apikey=mk001", #dú
    "gainhat": "https://imgs-api.vercel.app/gainhat?apikey=mk001", #gái nhật
    "japcosplay": "https://imgs-api.vercel.app/japcosplay?apikey=mk001", #Cosplay
    "loli": "https://imgs-api.vercel.app/loli?apikey=mk001", #loli
    "tw": "https://imgs-api.vercel.app/tw?apikey=mk001", #tw
    "anime": "https://imgs-api.vercel.app/anime?apikey=mk001", #anime
    "umaru": "https://imgs-api.vercel.app/umaru?apikey=mk001", #icon
    "sagiri": "https://imgs-api.vercel.app/sagiri?apikey=mk001" #sagiri
}

@bot.message_handler(commands=list(API_LIST.keys()))
def send_image(message):
    try:
        cmd = message.text[1:]  # Lấy lệnh, bỏ dấu "/"
        user = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

        # Gọi API tương ứng với lệnh
        response = requests.get(API_LIST[cmd], timeout=10).json()
        if 'url' in response:
            img = requests.get(response['url'], headers={"User-Agent": "Mozilla/5.0"}, timeout=10).content
            bot.send_photo(message.chat.id, BytesIO(img), caption=f"Lóc Xọ Đi Cu {user}")
        else:
            bot.reply_to(message, f"Lỗi Api Không Thể Get '{cmd}'.")

    except Exception:
        bot.reply_to(message, "Lỗi! Không thể lấy ảnh.")


#Src Code   
ADMIN_IDS = 1322814990
DATA_FILE = "src_links.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        src_links = json.load(f)
else:
    src_links = {}

@bot.message_handler(commands=["addsrc"])
def add_src(message):
    if message.from_user.id != ADMIN_IDS:
        bot.reply_to(message, "Mày Bị Ngáo À")
        return
    
    try:
        _, name, url = message.text.split(maxsplit=2)
        src_links[name] = url
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(src_links, f, indent=4)
        bot.reply_to(message, f"✅ Đã thêm link: {name} → {url}")
    except ValueError:
        bot.reply_to(message, "❌ Sai cú pháp! Dùng: /addsrc [tên] [link]")

@bot.message_handler(commands=["src"])
def show_src(message):
    if not src_links:
        bot.reply_to(message, "Chưa Có Gì Đâu")
        return
    
    keyboard = types.InlineKeyboardMarkup()
    for name, url in src_links.items():
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    
    bot.send_message(message.chat.id, "🔗 Danh Sách Code:", reply_markup=keyboard)

@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    text = message.text[len('/voice '):].strip()
    
    if not text:
        bot.reply_to(message, "🤖 Hello Babi\nUsage: /voice <Text>")
        return

    temp_file_path = tempfile.mktemp(suffix='at_muzic.mp3')

    try:
        tts = gTTS(text, lang='vi')
        tts.save(temp_file_path)

        with open(temp_file_path, 'rb') as audio_file:
            bot.send_voice(chat_id=message.chat.id, voice=audio_file)

    except Exception as e:
        bot.reply_to(message, "Error Bot")
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@bot.message_handler(commands=['qr'])
def generate_qr(message):
    input_text = message.text.split(maxsplit=1)
    
    if len(input_text) > 1:
        input_text = input_text[1] 
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(input_text)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        bio = BytesIO()
        bio.name = 'qr.png'
        img.save(bio, 'PNG')
        bio.seek(0)

        bot.send_photo(message.chat.id, photo=bio, caption=f"<blockquote>QR Của Bạn: {input_text}</blockquote>",parse_mode="HTML")
    else:
        bot.reply_to(message, "🤖 Usage: /qr <Chữ Cần Tạo QR>")

import datetime
todaya = datetime.datetime.now().strftime("%d/%m/%Y")
        
from io import BytesIO
@bot.message_handler(commands=['doneta'])
def bank_info(message):
    image_url = "https://ibb.co/Kph43vVJ" # IMG ẢNH QR
    
    try:
        response = requests.get(image_url, timeout=5) 
        response.raise_for_status() 
        photo = BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, "🚨 Không thể tải ảnh, vui lòng thử lại sau!")
        print(f"Lỗi khi tải ảnh: {e}")
        return  

    user_id = message.from_user.id

    bank_info_text = f'''
<b>Thông Tin Donate</b>
├ Ngân Hàng: MBBank
├ STK: 698336
├ Chủ TK: PHAN TRONG PHUC
├ ND: ngai_loc{user_id}
├ Số Tiền: Tuỳ Tâm
├ GỬI BILL CHO AD ĐỂ ĐƯỢC NÂNG VIP
├ LƯU Ý: PHẢI CÓ NỘI DUNG CHUYỂN KHOẢN
└ NOTE: CẢM ƠN ANH EM ĐÃ ỦNG HỘ!!! 
'''

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("ADMIN", url="https://t.me/NgocLinh2x_CTV"))

    bot.send_photo(message.chat.id, photo, caption=bank_info_text, parse_mode='HTML', reply_markup=keyboard)

    

import datetime
import pytz  
import time
from datetime import timedelta
from io import BytesIO
import requests
import random

start_time = time.time()

last_command_time = {}

def get_elapsed_time():
    elapsed_time = time.time() - start_time
    return str(timedelta(seconds=int(elapsed_time)))

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        username = new_member.username
        first_name = new_member.first_name
        
        
        if username:
            user_info = f"@{username}"
        else:
            user_info = first_name
        
        welcome_text = f'''
<blockquote>🎉 Chào Mừng {user_info} Đến Với Nhóm! 🎉
Huy Vọng Bạn Sẽ Có Thời Gian Vui Vẻ ở Đây!
Nhập /help để xem danh sách lệnh !!!
</blockquote>
        '''
        
        bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

import threading

@bot.message_handler(commands=['info'])
def handle_check(message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    waiting = bot.reply_to(message, "🔎")
    
    user_photos = bot.get_user_profile_photos(user.id)
    chat_info = bot.get_chat(user.id)
    chat_member_status = bot.get_chat_member(message.chat.id, user.id).status
    
    bio = chat_info.bio or "Không có bio"
    user_first_name = user.first_name
    user_last_name = user.last_name or ""
    user_username = f"@{user.username}" if user.username else "Không có username"
    user_language = user.language_code or 'Không xác định'
    
    status_dict = {
        "creator": "Admin chính",
        "administrator": "Admin",
        "member": "Thành viên",
        "restricted": "Bị hạn chế",
        "left": "Rời nhóm",
        "kicked": "Bị đuổi khỏi nhóm"
    }
    status = status_dict.get(chat_member_status, "Không xác định")
    
    caption = (
        "<pre>     🚀 THÔNG TIN 🚀\n"
        "┌──────────⭓INFO⭓─────────\n"
        f"│ 🆔 : {user.id}\n"
        f"│ 👤 Tên: {user_first_name} {user_last_name}\n"
        f"│ 👉 Username: {user_username}\n"
        f"│ 🔰 Ngôn ngữ: {user_language}\n"
        f"│ 🏴 Trạng thái: {status}\n"
        f"│ ✍️ Bio: {bio}\n"
        f"│ 🤳 Avatar: {'Đã có avatar' if user_photos.total_count > 0 else 'Không có avatar'}\n"
        f"| 🚀 Trạng thái tài khoản:\n"
        f"| 👤 Đây là người dùng thật\n"
        f"| ✅ Không có dấu hiệu lừa đảo\n"
        f"| ✅ Không phải tài khoản giả mạo\n"
        f"| ✅ Không bị hạn chế\n"
        f"| ❌ Không phải tài khoản hỗ trợ\n"
        "└───────────────[✓]─────────────</pre>"
    )
    
    if user_photos.total_count > 0:
        bot.send_photo(message.chat.id, user_photos.photos[0][-1].file_id, caption=caption, parse_mode='HTML', reply_to_message_id=message.message_id)
    else:
        bot.reply_to(message, caption, parse_mode='HTML')
    
    def xoatn(message, delay):
        try:
            bot.delete_message(message.chat.id, waiting.message_id)
        except Exception as e:
            print(f"Lỗi khi xóa tin nhắn: {e}")
    
    threading.Thread(target=xoatn, args=(message, 0)).start()

# XSMB 
API_URL = "https://nguyenmanh.name.vn/api/xsmb?apikey=KLY6MQVh"

@bot.message_handler(commands=['xsmb'])
def get_xsmb(message):
    try:
        response = requests.get(API_URL, timeout=10).json()

        if response.get("status") == 200:
            ketqua = response.get("result", "❌ Không có dữ liệu.")
            bot.send_message(message.chat.id, f"🎯 <b>Kết quả XSMB:</b>\n<pre>{ketqua}</pre>", parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Không lấy được kết quả XSMB.")

    except Exception:
        bot.reply_to(message, "⚠️ Lỗi khi lấy kết quả xổ số.")
        
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, '<blockquote>EM CÓ QUYỀN HẢ ??</blockquote>', parse_mode='HTML')
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>........</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        bot.kick_chat_member(message.chat.id, user_id)
        
        bot.send_message(
            message.chat.id, 
            f"<blockquote>🔨 Người dùng với ID {user_id} đã bị ban khỏi nhóm.</blockquote>",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.reply_to(message, '<blockquote>Không thể ban người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>', parse_mode='HTML')
        print(f"Error banning user: {e}")

@bot.message_handler(commands=['im'])
def warn_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, '<blockquote>EM ĐƯỢC CHAT CÂUU NÀY HẢ ??</blockquote>', parse_mode='HTML')
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>Ơ !!!</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        until_date = int(time.time()) + 15 * 60
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            until_date=until_date
        )
        
        bot.send_message(
            message.chat.id, 
            f"<blockquote>⚠️ Người dùng với ID {user_id} đã bị cảnh báo và cấm chat trong 15 phút.</blockquote>",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.reply_to(message, "<blockquote>Không thể cảnh báo người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>", parse_mode='HTML')
        print(f"Error warning user: {e}")

import requests

@bot.message_handler(commands=['check'])
def check_hot_web(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, '<blockquote>Vui lòng cung cấp URL của trang web cần kiểm tra (VD: /check https://example.com).</blockquote>',parse_mode='HTML')
        return
    
    url = message.text.split()[1]

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            bot.reply_to(message, f"<blockquote>🔗 Trang web {url} đang hoạt động bình thường (Status: 200 OK).</blockquote>", parse_mode='HTML')
        else:
            bot.reply_to(message, f"<blockquote>⚠️ Trang web {url} có vấn đề (Status: {response.status_code}).</blockquote>", parse_mode='HTML')
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"<blockquote>❌ Không thể kết nối tới trang web {url}. Lỗi: {e}</blockquote>", parse_mode='HTML')


import requests

@bot.message_handler(commands=['checkip'])
def check_ip(message):
    params = message.text.split()
    
    if len(params) < 2:
        bot.reply_to(message, '<blockquote>Vui lòng cung cấp địa chỉ IP cần kiểm tra (VD: /checkip 8.8.8.8).</blockquote>', parse_mode='blockquote')
        return
    
    ip_address = params[1]

    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=10)
        response.raise_for_status()  
        
        ip_data = response.json()

        city = ip_data.get('city', 'Không xác định')
        region = ip_data.get('region', 'Không xác định')
        country = ip_data.get('country', 'Không xác định')
        org = ip_data.get('org', 'Không xác định')
        loc = ip_data.get('loc', 'Không xác định')
        
        ip_info = (f"<blockquote>🌐 Địa chỉ IP: {ip_address}\n"
                   f"📍 Thành Phố: {city}\n"
                   f"🏛 Khu Vực: {region}\n"
                   f"🌎 Quốc Gia: {country}\n"
                   f"🏢 Tổ Chức: {org}\n"
                   f"📍 Vị Trí (Lat, Lng): {loc}</blockquote>")
        
        bot.reply_to(message, ip_info, parse_mode='HTML')
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"<blockquote>❌ Không thể kết nối tới dịch vụ kiểm tra IP. Lỗi: {e}</pre>", parse_mode='blockquote')
    except Exception as e:
        bot.reply_to(message, f"<blockquote>❌ Đã xảy ra lỗi khi kiểm tra IP. Lỗi: {e}</pre>", parse_mode='blockquote')


@bot.message_handler(commands=['unim'])
def unrestrict_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, '<blockquote>Bạn không có quyền sử dụng lệnh này.</pre>', parse_mode='blockquote')
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, '<blockquote>Vui lòng trả lời tin nhắn của người dùng cần hủy cấm chat.</blockquote>', parse_mode='HTML')
        return

    user_id = message.reply_to_message.from_user.id
    
    try:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            until_date=0  
        )
        
        bot.send_message(
            message.chat.id, 
            f"<blockquote>✅ Người dùng với ID {user_id} đã được phép chat trở lại.</blockquote>", 
            parse_mode='HTML'
        )
    except Exception as e:
        bot.reply_to(message, '<blockquote>Không thể gỡ cấm chat cho người dùng. Vui lòng kiểm tra lại thông tin hoặc quyền hạn của bot.</blockquote>', parse_mode='HTML')
        print(f"Error unrestricted user: {e}")

from urllib.parse import urlparse

@bot.message_handler(commands=['html'])
def handle_code_command(message):
    command_args = message.text.split(maxsplit=1)

    if len(command_args) < 2:
        bot.reply_to(message, "Vui lòng cung cấp url sau lệnh /html. Ví dụ: /html https://example.com")
        return

    url = command_args[1]
    
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        bot.reply_to(message, "Vui lòng cung cấp một URL hợp lệ.")
        return

    domain = parsed_url.netloc
    file_name = f"at_get_html.txt"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        with open(file_name, 'rb') as file:
            caption = f"<blockquote>HTML Của Trang Web:\n{url}</blockquote>"
            bot.send_document(message.chat.id, file, caption=caption, parse_mode='HTML')

    except requests.RequestException as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi tải trang web: {e}")

    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi xử lý file: {e}")

    finally:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                bot.reply_to(message, f"Đã xảy ra lỗi khi xóa file: {e}")
                
# thời tiết 1 này
API_URL = "https://nguyenmanh.name.vn/api/thoitiet?type=text&query={city}&apikey=KLY6MQVh"
API_IMG = "https://nguyenmanh.name.vn/api/thoitiet?type=image&query={city}&apikey=KLY6MQVh"

@bot.message_handler(commands=['thoitiet'])
def get_weather(message):
    try:
        # Lấy thành phố từ tin nhắn, mặc định là Hà Nội
        parts = message.text.split(" ", 1)
        city = parts[1] if len(parts) > 1 else "Hà Nội"

        # Gọi API lấy dữ liệu thời tiết
        response = requests.get(API_URL.format(city=city), timeout=10).json()

        if response.get("status") == 200:
            weather_text = response["result"]["result"]
            image_url = response["result"]["image"]

            # Gửi tin nhắn văn bản
            bot.send_message(message.chat.id, f"📍 Thời tiết tại <pre>{city}</pre>:\n\n{weather_text}", parse_mode='HTML')

            # Gửi ảnh thời tiết
            bot.send_photo(message.chat.id, image_url, caption="🖼 Ảnh dự báo thời tiết", parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Không lấy được thông tin thời tiết.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi lấy dữ liệu thời tiết: {e}")
                
#thời tiết 7 này
API_URL = "https://nguyenmanh.name.vn/api/weather?city={city}&apikey=KLY6MQVh"

FLIRT_QUOTES = [
    "Trời {city} lạnh thế này, chắc em cần một vòng tay ấm áp nhỉ? 🥰",
    "Hôm nay trời {city} có nắng, nhưng tim anh lại đổ mưa nhớ em rồi. ☔️❤️",
    "Thời tiết {city} thay đổi thất thường, nhưng tình cảm anh dành cho em thì vẫn luôn như vậy. 💕",
    "Gió {city} có thể lạnh, nhưng anh hứa sẽ luôn ấm áp với em. 🌬️💖",
    "Bầu trời {city} có thể âm u, nhưng nụ cười em vẫn là ánh nắng trong tim anh. ☀️😘",
    "Dự báo thời tiết nói {city} có mưa, nhưng chẳng ai dự báo được anh thương em nhiều thế nào. 😘",
    "Trời {city} có thể mưa, nhưng anh vẫn muốn cùng em đi dưới cơn mưa ấy. 🌧️🥰",
    "Người ta nói thời tiết {city} hôm nay đẹp lắm, nhưng với anh, đẹp nhất vẫn là em. 💘",
    "Hôm nay {city} nhiều mây, nhưng trái tim anh lúc nào cũng hướng về em như ánh nắng ban mai. ☀️💕",
    "Nếu em thấy trời {city} lạnh, hãy nhớ rằng anh luôn ở đây để sưởi ấm cho em. 🔥❤️"
]

@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        parts = message.text.split(" ", 1)
        city = parts[1] if len(parts) > 1 else "Vĩnh Phúc"

        response = requests.get(API_URL.format(city=city), timeout=10).json()

        if response.get("status") == 200:
            weather_info = response.get("result", {})
            city_name = weather_info.get("name", city)
            country = weather_info["sys"].get("country", "Không rõ")
            temp = weather_info["main"].get("temp", "N/A")
            feels_like = weather_info["main"].get("feels_like", "N/A")
            humidity = weather_info["main"].get("humidity", "N/A")
            pressure = weather_info["main"].get("pressure", "N/A")
            wind_speed = weather_info["wind"].get("speed", "N/A")
            weather_desc = weather_info["weather"][0].get("description", "Không rõ")
            cloudiness = weather_info["clouds"].get("all", "N/A")
            rain = weather_info.get("rain", {}).get("1h", 0) 

            flirt_text = random.choice(FLIRT_QUOTES).format(city=city_name)

            weather_text = (
                f"🌤 <b>Thời tiết tại {city_name}, {country}</b>\n"
                f"🌡 Nhiệt độ: <b>{temp}°C</b> (Cảm giác như {feels_like}°C)\n"
                f"🌥 Mô tả: <i>{weather_desc}</i>\n"
                f"💧 Độ ẩm: {humidity}% | Áp suất: {pressure} hPa\n"
                f"💨 Gió: {wind_speed} km/h\n"
                f"🌧 Lượng mưa: {rain} mm | ☁ Mây: {cloudiness}%\n\n"
                f"<pre>💌 {flirt_text}</pre>"
            )

            bot.send_message(message.chat.id, weather_text, parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Không lấy được thông tin thời tiết.")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi lấy dữ liệu thời tiết: {e}")
# ca dao 
API_URL = "https://nguyenmanh.name.vn/api/cadao?apikey=KLY6MQVh"

@bot.message_handler(commands=['cadao'])
def get_cadao(message):
    try:
        response = requests.get(API_URL).json()
        if response.get("status") == 200:
            rdCadao = response["result"]["rdCadao"]
            image_url = response["result"]["image"]

            bot.send_photo(message.chat.id, image_url, caption=f"📜 <b>Ca Dao Tục Ngữ:</b>\n<pre>{rdCadao}</pre>", parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Không lấy được dữ liệu ca dao.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi khi lấy ca dao: {e}")
        
# API TikTok
API_URL = "https://tikwm.com/api/?url={url}"

@bot.message_handler(commands=['tiktok'])
def get_tiktok_video(message):
    try:
        # Tách link từ tin nhắn
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "🎬 Sử dụng: <pre>/tiktok <url></pre>", parse_mode="HTML")
            return

        url = args[1]  # Lấy URL từ tin nhắn
        loading_msg = bot.reply_to(message, "💸 <pre>Đang Lấy Thông Tin Video...</pre>", parse_mode="HTML")

        # Gọi API TikTok
        response = requests.get(API_URL.format(url=url)).json()

        # Xóa tin nhắn "Đang lấy thông tin..."
        bot.delete_message(message.chat.id, loading_msg.message_id)

        if response.get("code") == 0 and "play" in response["data"]:
            video_url = response["data"]["play"]
            title = response["data"].get("title", "Video TikTok")
            nickname = response["data"].get("nickname", "Unknown")
            video_id = response["data"].get("id", "Không xác định")  # Lấy video_id

            caption = f"""
🎬 <b>Video TikTok</b>
👤 Used Đăng: <pre>{nickname}</pre>
🏷️ Tiêu Đề: <pre>{title}</pre>
🆔 ID Video: <pre>{video_id}</pre>
            """
            bot.send_video(message.chat.id, video_url, caption=caption, parse_mode="HTML")
        else:
            bot.reply_to(message, f"❌ <pre>Lỗi: {response.get('msg', 'Không xác định')}</pre>", parse_mode="HTML")
    
    except Exception as e:
        bot.reply_to(message, f"⚠️ <pre>Lỗi khi lấy video: {e}</pre>", parse_mode="HTML")
        
#WAR TELE
ADMIN_IDS = {6980410649, 123456789}  

def load_war_messages():
    with open('war.txt', 'r', encoding='utf-8') as file:
        return file.readlines()

def send_random_message(chat_id):
    messages = load_war_messages()
    if not messages:
        bot.send_message(chat_id, "<pre>❌ War Text Lỗi</pre>", parse_mode='HTML')
        return
    message = random.choice(messages).strip()
    bot.send_message(chat_id, message)

@bot.message_handler(commands=['war'])
def war(message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) != 3:
        bot.reply_to(message, "<pre>Cú Pháp: /war <ID> <Số lần></pre>", parse_mode='HTML')
        return

    try:
        target_id = int(args[1])
        count = int(args[2])
    except ValueError:
        bot.reply_to(message, "<pre>❌ Vui Lòng Nhập ID & Số Lần Hợp Lệ!</pre>", parse_mode='HTML')
        return

    if target_id in ADMIN_IDS:
        bot.reply_to(message, "<pre>❌ ĐCU MÀY WAR AI ĐẤY!</pre>", parse_mode='HTML')
        return

    if count <= 0:
        bot.reply_to(message, "<pre>❌ Số Lần Phải > 0 </pre>", parse_mode='HTML')
        return

    bot.send_message(chat_id, f"<pre>🔥 Bắt Đầu Tấn Công: {target_id} 🔥</pre>", parse_mode='HTML')
    for _ in range(count):
        send_random_message(target_id)
        time.sleep(1)

#check ff
API_URL = "https://api.ffcommunity.site/info.php?uid="

@bot.message_handler(commands=['ff'])
def get_ff_info(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "<pre>❌Cú Pháp /ff 12345678</pre>", parse_mode='HTML')
            return

        uid = args[1]
        response = requests.get(API_URL + uid)
        
        if response.status_code != 200:
            bot.reply_to(message, "❌ Lỗi Api")
            return

        data = response.json()

        username = data.get("AccountName", "Không có")
        level = data.get("AccountLevel", "Không có")
        br_rank = data.get("BrRank", "Không có")
        cs_rank = data.get("CsRank", "Không có")
        likes = data.get("AccountLikes", "Không có")
        region = data.get("AccountRegion", "Không có")
        created_at = data.get("AccountCreateTime", "Không rõ")
        last_login = data.get("AccountLastLogin", "Không rõ")
        signature = data.get("AccountSignature", "Không có")

        guild_info = data.get("Guild Information", {})
        guild_name = guild_info.get("GuildName", "Không có")
        guild_level = guild_info.get("GuildLevel", "Không có")

        pet_info = data.get("Pet Information", {})
        pet_name = pet_info.get("PetName", "Không có")
        pet_level = pet_info.get("PetLevel", "Không có")

        message_text = f"""<pre>
📌Thông Tin Free Fire:
🆔 UID: {uid}
👤 Tên: {username}
🏆 Cấp độ: {level}
🎖️ Rank BR: {br_rank}
🥇 Rank CS: {cs_rank}
👍 Lượt Thích: {likes}
🌍 Khu Vực: {region}
📅 Ngày Tạo: {created_at}
🕒 Login Gần Đây: {last_login}
📝 Tiểu Sử: {signature}

🏠 Quân Đoàn: {guild_name}
🔝 Cấp Độ: {guild_level}

🐾 Thú Cưng: {pet_name}
🔝 Cấp Độ: {pet_level}
</pre>"""
        bot.send_message(message.chat.id, message_text, parse_mode="HTML")
    
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")
        
#Check Facebook
@bot.message_handler(commands=['fbid'])
def get_facebook_info(message):
    msg_parts = message.text.split()
    if len(msg_parts) < 2:
        bot.reply_to(message, "<pre>❌ Vui lòng nhập ID Facebook. Ví dụ: /fbid 1000xxxxxxx</pre>", parse_mode="HTML")
        return

    fb_id = msg_parts[1]
    api_url = f"https://api.ffcommunity.site/getInfo.php?id={fb_id}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data["error"] == 0:
            name = data["name"]
            user_id = data["id"]
            reply_text = f"""<pre>📌Thông Tin Facebook:\n
👤 Name Facebook: {name}
🆔 ID Facebook: {user_id}</pre>"""
        else:
            reply_text = "❌ Không tìm thấy thông tin. Vui lòng kiểm tra lại ID."

        bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
        bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.reply_to(message, "❌ Đã xảy ra lỗi khi lấy thông tin Facebook. Vui lòng thử lại sau.")

#Check FF BAN
@bot.message_handler(commands=['checkbanff'])
def check_ban_status(message):
    msg_parts = message.text.split()
    if len(msg_parts) < 2:
        bot.reply_to(message, "❌ Vui lòng nhập UID Free Fire. Ví dụ: /checkbanff 4131xxx", parse_mode="HTML")
        return

    uid = msg_parts[1]
    api_url = f"https://api.ffcommunity.site/isbanned.php?uid={uid}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if "Status" in data:
            account_name = data.get("Account Name", "Không rõ")
            account_uid = data.get("Account UID", "Không rõ")
            account_region = data.get("Account Region", "Không rõ")
            status = data.get("Status", "Không rõ")

            reply_text = f"""<pre>📌Trạng Thái Tài Khoản Free Fire:\n
👤 Tên: {account_name}
🆔 UID: {account_uid}
🌍 Khu vực: {account_region}
🚨 Trạng thái: {status}</pre>"""

        else:
            reply_text = "❌ Không tìm thấy thông tin UID này."

        bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
        bot.delete_message(message.chat.id, message.message_id)
    except:
        bot.reply_to(message, "❌ Đã xảy ra lỗi khi kiểm tra UID. Vui lòng thử lại sau.")
        
#key 2fa
@bot.message_handler(commands=['2fa'])
def get_2fa_code(message):
    args = message.text.split(" ", 1)  
    if len(args) < 2:
        bot.reply_to(message, "<pre>❌ Vui lòng nhập key! Ví dụ: /2fa ABCXYZ</pre>", parse_mode="HTML")
        return
    
    key = args[1]
    api_url = f"https://api.ffcommunity.site/2fa.php?key={key}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("status") == "ok":
            code = data["result"].get("code", "Không có mã")

            reply_text = f"""<pre> Mã 2FA Của Bạn Là:\n
🔢 Mã 2FA: {code}</pre>"""

            bot.send_message(message.chat.id, reply_text, parse_mode="HTML", disable_web_page_preview=True)
        else:
            bot.reply_to(message, "❌ Không thể lấy mã 2FA. Vui lòng thử lại sau.")

        bot.delete_message(message.chat.id, message.message_id)

    except:
        bot.reply_to(message, "❌ Đã xảy ra lỗi khi truy vấn API.")

#video gái
@bot.message_handler(commands=['vdgai'])
def send_random_video(message):
    chat_id = message.chat.id
    user_id = message.from_user.id 

    try:
        response = requests.get("https://api.ffcommunity.site/randomvideo.php").json()

        if "video" in response:
            video_url = response["video"]
            caption = f"<pre>🎥 Video Ngẫu Nhiên Của {user_id} Nè</pre>"

            try:
                bot.send_video(chat_id, video_url, caption=caption, parse_mode="HTML")
            except:
                bot.send_message(chat_id, f"<pre>⚠️ Lỗi Video Rồi {user_id} Xem Tạm Tại Đây: {video_url}</pre>", parse_mode="HTML")

        else:
            bot.send_message(chat_id, "<pre>❌ Không tìm thấy video. Vui lòng thử lại sau.</pre>", parse_mode="HTML")

    except Exception as e:
        bot.send_message(chat_id, "<pre>⚠️ Lỗi khi lấy video! Thử lại sau.</pre>", parse_mode="HTML")
        print(f"Lỗi: {e}")
        
#dịch
@bot.message_handler(commands=['dich'])
def translate_text(message):
    args = message.text.split(" ", 1)  
    if len(args) < 2:
        bot.reply_to(message, "<pre>❌ Vui lòng nhập nội dung cần dịch! Ví dụ: /dich Xin chào</pre>", parse_mode="HTML")
        return
    
    text_to_translate = args[1]
    api_url = f"http://minhnguyen3004.x10.mx/dich.php?lang=vi&dq={text_to_translate}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("success"):
            original_text = data.get("text", "Không có dữ liệu")
            translated_text = data.get("dich_text", "Không có bản dịch")
            lang_from = data.get("lang", "Không rõ")
            lang_to = data.get("lang_dich", "Không rõ")

            reply_text = f"""<pre>🌍 Dịch Thành Công\n
📝 Văn Bản Gốc ({lang_from}): {original_text}
📌 Dịch Sang ({lang_to}): {translated_text}</pre>"""

            bot.send_message(message.chat.id, reply_text, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Không thể dịch văn bản. Vui lòng thử lại sau.")

        bot.delete_message(message.chat.id, message.message_id) 

    except:
        bot.reply_to(message, "❌ Đã xảy ra lỗi khi truy vấn API.")
        
#AI    
@bot.message_handler(commands=['ai'])
def ai_search(message):
    args = message.text.split(maxsplit=1)  # Lấy nội dung sau /ai
    if len(args) < 2:
        bot.reply_to(message, "<pre>❗ Vui lòng nhập mô tả ảnh.\nVí dụ: /ai mèo cute</pre>", parse_mode="HTML")
        return

    prompt = args[1].strip()
    url = f"https://lexica.art/api/v1/search?q={prompt}"

    try:
        response = requests.get(url)
        data = response.json()

        images = data.get("images", [])
        if not images:
            bot.reply_to(message, "❌ Không tìm thấy ảnh phù hợp!")
            return

        selected_image = random.choice(images) 
        image_url = selected_image["src"]

        bot.send_photo(
            chat_id=message.chat.id,
            photo=image_url,
            caption=f"🖼 Ảnh AI Về: *{prompt}*",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, "❌ Lỗi khi lấy ảnh từ AI, vui lòng thử lại sau!")
        
# Chạy bot
bot.polling()
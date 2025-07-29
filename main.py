import telebot
import os
import random
import string

BOT_TOKEN = 'TOKEN-CỦA-MÀY'

bot = telebot.TeleBot(BOT_TOKEN)
UPLOAD_DIR = "upload"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def random_code(length=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Khi /start bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Bot mã hóa Obfuscate Sakura của Văn Trọng đã sẵn sàng!\nGửi file .py vào đây để được mã hóa.")

#  Xử lý khi có file gửi vào (cả group và private)
@bot.message_handler(content_types=['document'])
def handle_file(message):
    doc = message.document
    if not doc.file_name.endswith(".py"):
        bot.reply_to(message, "Chỉ nhận file .py để mã hóa.")
        return

    user_id = message.from_user.id
    rand = random_code()
    original = doc.file_name.rsplit(".", 1)[0]
    input_name = f"{original}_{rand}_{user_id}.py"
    input_path = os.path.join(UPLOAD_DIR, input_name)
    output_name = f"obf_{original}_{rand}_{user_id}.py"
    output_path = os.path.join(OUTPUT_DIR, output_name)

    try:
        # Tải file
        file_info = bot.get_file(doc.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(input_path, "wb") as f:
            f.write(downloaded_file)

        bot.reply_to(message, "⚙️ Đang mã hóa file...")

        code = os.system(f"python obf.py -f {input_path} -o {output_path}")

        if not os.path.exists(output_path):
            bot.reply_to(message, "Mã hóa thất bại!")
            return

        # Gửi file đã mã hóa
        with open(output_path, "rb") as obf_file:
            bot.send_document(message.chat.id, obf_file, caption="✅ Mã hóa hoàn tất!")

    except Exception as e:
        bot.reply_to(message, f" Đã xảy ra lỗi: {e}")
print("Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)



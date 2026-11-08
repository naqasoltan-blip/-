import telebot
import random
import time
import os
import re
import threading
import logging

# ضع التوكن الخاص بك هنا مباشرة بين علامتي التنصيص
TOKEN = "9202505066:AAEbtFmxprFbfLWSKNpLWSh5d_BYHU9FXrs"

if not TOKEN:
    raise ValueError("9202505066:AAEbtFmxprFbfLWSKNpLWSh5d_BYHU9FXrs")

bot = telebot.TeleBot(TOKEN, threaded=True)

logging.basicConfig(level=logging.INFO)

# الكلمات والإيموجيات
emoji_dict = {
    "كلب": "🐶",
    "قطة": "🐱",
    "أسد": "🦁",
    "نمر": "🐯",
    "فيل": "🐘",
    "قرد": "🐵",
    "أرنب": "🐰",
    "دب": "🐻",
    "ثعلب": "🦊",
    "ذئب": "🐺",
    "حصان": "🐴",
    "بقرة": "🐮",
    "خروف": "🐑",
    "دجاجة": "🐔",
    "سمكة": "🐟",
    "فراشة": "🦋",
    "نار": "🔥",
    "قلب": "❤️",
    "تفاح": "🍎",
    "موز": "🍌",
    "عنب": "🍇",
    "برتقال": "🍊",
    "بطيخ": "🍉",
    "فراولة": "🍓",
    "كرز": "🍒",
    "بيتزا": "🍕",
    "برغر": "🍔",
    "بطاطا": "🍟",
    "كعكة": "🎂",
    "شوكولاتة": "🍫",
    "قهوة": "☕",
    "شاي": "🍵",
    "سيارة": "🚗",
    "طائرة": "✈️",
    "سفينة": "🚢",
    "دراجة": "🚲",
    "قطار": "🚆",
    "كرة": "⚽",
    "كرة سلة": "🏀",
    "كأس": "🏆",
    "ميدالية": "🏅",
    "شمس": "☀️",
    "قمر": "🌙",
    "نجمة": "⭐",
    "مطر": "🌧️",
    "ثلج": "❄️",
    "برق": "⚡",
    "وردة": "🌹",
    "زهرة": "🌻",
    "شجرة": "🌳",
    "كتاب": "📖",
    "قلم": "✏️",
    "ساعة": "⏰",
    "هاتف": "📱",
    "حاسوب": "💻",
    "بيت": "🏠",
    "مدرسة": "🏫",
    "مستشفى": "🏥",
    "تاج": "👑",
    "هدية": "🎁",
    "صاروخ": "🚀",
    "نظارة": "👓",
    "مفتاح": "🔑",
    "قفل": "🔒",
    "بالون": "🎈",
    "موسيقى": "🎵",
    "كاميرا": "📷",
    "ساعة يد": "⌚",
    "مصباح": "💡",
    "مظلة": "☂️",
    "سيف": "⚔️",
    "درع": "🛡️",
    "شبح": "👻",
    "روبوت": "🤖",
    "فضائي": "👽",
    "وحش": "👹",
    "تنين": "🐉",
    "قرش": "🦈",
    "أخطبوط": "🐙",
    "سلحفاة": "🐢",
    "بطريق": "🐧"
}

# تخزين التحديات حسب المحادثة
challenges = {}

# منع تداخل العمليات
lock = threading.Lock()


def normalize(text):
    """تنظيف النص لتسهيل مقارنة الإجابات"""
    text = text.strip().lower()

    # حذف التشكيل
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

    # توحيد الحروف
    text = text.replace("أ", "ا")
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")
    text = text.replace("ة", "ه")
    text = text.replace("ى", "ي")

    # حذف علامات الترقيم
    text = re.sub(r'[^\w\s]', '', text)

    return " ".join(text.split())

@bot.message_handler(func=lambda message: message.text is not None and 'سرعة' in message.text)
def start(message):
    chat_id = message.chat.id
    target = random.choice(list(emoji_dict.keys()))

    with lock:
        challenges[chat_id] = {
            "target": target,
            "start_time": time.perf_counter(),
            "active": True
        }

    bot.send_message(
        chat_id,
        "╭•┈•🏛️ 𝓥. 𝓥 🏛️•┈•╮\n"
        "   ⚡ 𝓣𝓾𝓻𝓫𝓸 𝓢𝓹𝓮𝓮𝓭 ⚡   \n"
        "╰•┈•🏛️ 𝓥. 𝓥 🏛️•┈•╯\n\n"
        "🔥 **بدأ تحدي السرعة الخطير!**\n\n"
        f"🎯 **اكتب الكلمة بأسرع ما لديك:**\n\n"
        f"        ✨ ⦗ {target} ⦘ ✨\n\n"
        "🏃‍♂️ *أسرع واحد يكتبها هو الفائز!*"
    )


@bot.message_handler(commands=["stop"])
def stop(message):
    chat_id = message.chat.id

    with lock:
        challenges.pop(chat_id, None)

    bot.send_message(chat_id, "🛑 **تم إيقاف التحدي بنجاح.**")


@bot.message_handler(commands=["emoji"])
def random_emoji(message):
    emoji = random.choice(list(emoji_dict.values()))
    bot.send_message(message.chat.id, emoji)


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "🎮 **أوامر البوت المتاحة:**\n\n"
        "⚡ اكتب كلمة **سرعة** لبدء التحدي الفوري\n"
        "🛑 `/stop` - إيقاف التحدي الحالي\n"
        "🎲 `/emoji` - إرسال إيموجي عشوائي\n"
        "📖 `/help` - قائمة المساعدة"
    )


@bot.message_handler(
    func=lambda message: message.text is not None
    and not message.text.startswith("/")
)
def check_answer(message):

    chat_id = message.chat.id
    username = message.from_user.first_name or "اللاعب"

    answer = normalize(message.text)

    with lock:
        challenge = challenges.get(chat_id)

        if not challenge or not challenge["active"]:
            result = "no_challenge"

        elif answer == normalize(challenge["target"]):

            elapsed = round(
                time.perf_counter() - challenge["start_time"], 3
            )

            target = challenge["target"]
            target_emoji = emoji_dict[target]

            challenge["active"] = False

            result = "correct"

        else:
            result = "wrong"
            target = challenge["target"]

    if result == "no_challenge":
        return

    elif result == "correct":
        bot.send_message(
            chat_id,
            "╔═══❖ೋೋ❖═══╗\n"
            f"   🎉 كفووو يا {username}! 🏆\n"
            "╚═══❖ೋೋ❖═══╝\n\n"
            f"✅ **الكلمة الصحيحة:** {target} {target_emoji}\n"
            f"⏱️ **سرعتك الخارقة:** `{elapsed}` ثانية\n\n"
            "👑 *أنت بطل الجولة بلا منازع!*"
        )

    elif result == "wrong":
        pass


print("Bot is running...")

bot.infinity_polling(skip_pending=True)

import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Bu yerga o'zingning tokeningni yoz!
TOKEN = "8315201190:AAFf4f6R8PosMCeGQfe3_81zPLZmTnI14BI"

# Lug'atlar (so'z: tarjima)
WORDS = {
    "book": "kitob",
    "apple": "olma",
    "house": "uy",
    "car": "mashina",
    "water": "suv",
    "tree": "daraxt",
}

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men lug‘at botman 📚. /test buyrug‘ini bosing.")

# Test funksiyasi
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word, correct = random.choice(list(WORDS.items()))

    # 4 ta variant tanlaymiz
    options = list(WORDS.values())
    random.shuffle(options)
    if correct not in options[:3]:
        options = options[:3] + [correct]
    random.shuffle(options)

    keyboard = ReplyKeyboardMarkup([[opt] for opt in options], one_time_keyboard=True)
    context.user_data["correct_answer"] = correct
    await update.message.reply_text(f"'{word}' so‘zining tarjimasi qaysi?", reply_markup=keyboard)

# Javobni tekshirish
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    correct = context.user_data.get("correct_answer")

    if correct:
        if user_answer == correct:
            await update.message.reply_text("✅ To‘g‘ri!")
        else:
            await update.message.reply_text(f"❌ Noto‘g‘ri. To‘g‘ri javob: {correct}")
        context.user_data["correct_answer"] = None
    else:
        await update.message.reply_text("Testni boshlash uchun /test ni bosing.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    app.run_polling()

if __name__ == "__main__":
    main()

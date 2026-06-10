import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def run_dummy_server():
    port = 8080

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return

    with TCPServer(("", port), QuietHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# =========================
# بيانات البوت
# =========================

TELEGRAM_TOKEN = "8897354719:AAFZHnJu5L0ghCTZbjER9bMzlyWJymZB8HE"
GEMINI_API_KEY = "AQ.Ab8RN6JDtV2kPVt8EHjMhC0q6BOFMx_OnAt9Mo49yZ9_RxUeTA"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# استقبال الرسائل
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()

    auto_replies = {
        'السلام عليكم': 'وعليكم السلام ورحمة الله وبركاته، منور يا غالي! 🌹',
        'الاخبار شنو': 'كلشي تمام التمام والامور طيبة، إنت كيف أمورك؟ ✨',
        'الطورك منو': 'طورني وصنعني المبرمج أحمد! 🤖🔥',
        'الصنعك منو': 'صنعني ومبرمجني الأساسي هو الفخم أحمد 😉💪',
        'منور': 'النور نورك والله يا حبيبنا! 🌟',
        'وين انت': 'لو مهتم كان عرفته 😎',
        'وين مختفي': 'لو مهتم كان عرفته 🙄',
        'وين مختفيه': 'لو مهتمه كان عرفتي 🙃',
        'صباح الخير': 'صبـ(⛅)ـُ(آٍلـٍـً(🌺)ـٍورٍدً)ـ(⛅)ـٍآٍآٍحً',
        'مساء الخير': 'مۡسَـ(🍀)ـاء الۣخـ(🌸)ـيۡݛ',
        'الحاصل شنو': 'Nothing special 😔',
        'كيف الكلام ده': 'عديل 😎',
        'تابعه لي منو انتي': 'احمد فارس 🥺',
        'الخبر شنو': 'الحمدلله انت كيف؟',
        'احسنت بارك الله فيك': 'طيب الله انفاسك 🤍',
        'فطوم': 'شيختنا 🤍🌹',
        'الجديد شنو': 'طلتك يا غالي',
        'الامور شنو': 'الحمدلله',
        'الحمدلله': 'دام حمدك',
        'يديك العافيه': 'الله يعافيك يارب 🤲',
        'شكرا': 'عفواً 🌹',
        'مشتاقين': '🥺🥺',
    }

    if user_text in auto_replies:
        await update.message.reply_text(auto_replies[user_text])
        return

    try:
        prompt = f"""
أنت بوت تليجرام ذكي اسمك Lyra.

صانعك ومطورك ومبرمجك الأساسي هو أحمد.
إذا سألك أي شخص من صنعك أو من طورك أو من برمجك فأخبره أن أحمد هو صانعك ومطورك.

تحدث دائماً بلهجة سودانية ودودة ومختصرة.

رسالة المستخدم:
{user_text}
"""

        response = model.generate_content(prompt)

        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("ما قدرت أفهم الرسالة، جرب تكتبها بطريقة تانية.")

    except Exception as e:
        print(f"Gemini Error: {e}")
        await update.message.reply_text("حصلت مشكلة في الاتصال بالذكاء الاصطناعي، جرب بعد شوية.")

# =========================
# تشغيل البوت
# =========================

if __name__ == "__main__":
    print("Bot Started Successfully 🚀")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.run_polling()

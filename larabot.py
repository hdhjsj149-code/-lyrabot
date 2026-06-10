import os
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args): return
    with TCPServer(("", port), QuietHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

import os
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 1. إعداد مفاتيح الاتصال بأمان من البيئة السحابية (مخفية ومؤمنة)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 2. تشغيل عميل جوجل جيميناي بالمكتبة الجديدة بالطريقة الصحيحة ✅
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# 3. دالة استقبال ومعالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    user_text = update.message.text.strip()
    
    # === [أولاً: لستة الردود التلقائية الثابتة] ===
    auto_replies = {
        'السلام عليكم': 'وعليكم السلام ورحمة الله وبركاته، منور يا غالي! 🌹',
        'الاخبار شنو': 'كلشي تمام التمام والامور طيبة، إنت كيف أمورك؟ ✨',
        'الطورك منو': 'طورني وصنعني المبرمج أحمد! 🤖🔥',
        'الصنعك منو': 'صنعني ومبرمجني الأساسي هو الفخم أحمد، ! 😉💪',
        'منور': 'النور نورك والله يا حبيبنا! 🌟',
        'وين انت': 'لو مهتم كان عرفته 😎',
        'وين مختفي': 'لو مهتم كان عرفته 🙄',
        'وين مختفيه': 'لو مهتمه كان عرفتي 🙃',
        'صباح الخير': 'صبـ(⛅)ـُ(آٍلـٍـً(🌺)ـٍورٍدً)ـ(⛅)ـٍآٍآٍحً ',
        'مساء الخير': 'مۡسَـ(🍀)ـاء الۣخـ(🌸)ـيۡݛ ',
        'الحاصل شنو': 'Nothing special 😔',
        'كيف الكلام ده': 'عديل 😎',
        'تابعه لي منو انتي ': 'احمد فارس 🥺',
        'الخبر شنو': 'الحمدلله انت كيف؟ ',
        'احسنت بارك الله فيك': 'طيب الله انفاسك 🤍',
        'فطوم': 'شيختنا 🤍🌹',
        'الجديد شنو': 'طلتك يا غالي ',
        'الامور شنو': 'الحمدلله ',
        'الحمدلله ': 'دام حمدك',
        'يديك العافيه ': 'الله يعافيك يارب 🤲',
        'شكرا': 'عفواً 🌹',
        'مشتاقين': '🥺🥺',
    }
    
    if user_text in auto_replies:
        await update.message.reply_text(auto_replies[user_text])
        return

    # === [ثانياً: تحويل الرسالة للذكاء الاصطناعي] ===
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=(
                    'أنت بوت تليجرام ذكي وسريع اسمك Lyra. صانعك ومطورك ومبرمجك الأساسي '
                    'هو المبرمج أحمد. إذا سألك أي شخص من صنعك, من طورك، أو من مبرمجك، '
                    'أخبره بفخر وثقة أن أحمد هو صانعك ومطورك، ولا تذكر جوجل إلا إذا سُئلت '
                    'عن التقنية المشغلة لذكائك فقط. رد دائماً بلهجة ودودة ومحترمة ومختصرة بالعامية السودانية.'
                )
            )
        )
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً، لم أستطع فهم الرسالة، جرب صياغتها بطريقة أخرى.")
        
    except Exception as e:
        print(f"حدث خطأ في الاتصال بجوجل: {e}")
        await update.message.reply_text("عذراً، حصلت مشكلة في الاتصال بذكاء جيميناي، جرب تاني!")

# 4. تشغيل وتدوير البوت
if __name__ == '__main__':
    print("البوت بدأ الشغل بنجاح.. 🚀")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

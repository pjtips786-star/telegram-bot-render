from flask import Flask, request
import telegram
import os

app = Flask(__name__)

# Environment Variable से Token लें (Secure तरीका)
TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return '✅ Telegram Bot is Running on Render!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text
            
            # /start Command
            if text == '/start':
                bot.send_message(
                    chat_id, 
                    "🚀 *Welcome!*\n\nBot Render पर Successfully चालू है!\n\nCommands:\n/start - शुरुआत\n/help - मदद", 
                    parse_mode='Markdown'
                )
            
            # /help Command
            elif text == '/help':
                bot.send_message(
                    chat_id,
                    "📋 *Available Commands:*\n\n/start - Bot शुरू करें\n/help - यह मदद दिखाएं\n\nआप कोई भी Message भेज सकते हैं, मैं उसे Repeat करूंगा!",
                    parse_mode='Markdown'
                )
            
            # कोई भी दूसरा Message
            else:
                bot.send_message(
                    chat_id,
                    f"📩 आपने कहा:\n\n_{text}_\n\n✅ Bot काम कर रहा है!",
                    parse_mode='Markdown'
                )
        
        return 'OK', 200
    
    except Exception as e:
        print(f"Error: {e}")
        return 'Error', 500

# Health Check के लिए
@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

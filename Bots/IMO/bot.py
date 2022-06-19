from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json

def send_c(c, args=""):
    return json.loads(requests.get(f"http://sw22.ddns.net:8080/Apis/IMO/?c={c}"+args).content.decode("utf-8"))

def get_qrs():
    return send_c("get_qrs")

def get_money_handling():
    return send_c("my_money")

async def get_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for qr in get_qrs():
        await update.message.reply_text(qr["type"])

"""
app = ApplicationBuilder().token("5498985401:AAGHsqIdKBDxn5L0Aohv9rLTJ015ik9j9yE").build()

app.add_handler(CommandHandler("get_qr", get_qr))
app.run_polling()
"""

print(get_money_handling())
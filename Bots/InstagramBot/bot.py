from telegram import *
from telegram.ext import *
import requests
import json
import time

MEMES_LOCATION = "/var/www/html/Apis/InstagramBot/Content/Memes/"

available_commands = []

def send_c(c, args="", j=False):
    url = f"http://192.168.1.104:8080/Apis/InstagramBot/?c={c}"+args
    print(url)
    r = requests.get(url).content.decode("utf-8")

    #print(r)
    if j:
        return r
    return json.loads(r)


async def memes_unchecked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(len(send_c("get_memes_to_aprove")))

async def hel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Commands:")
    for c in available_commands:
        await update.message.reply_text("--- "+c)

async def help_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for c in send_c("help"):
        await update.message.reply_text(c)

async def recargar_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    send_c("if_reload")
    await update.message.reply_text("Reloaded")

async def aprove_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    send_c("aprove_meme", args=f"&file_name={context.args[0]}", j=True)
    await update.message.reply_text("Aproved")

async def no_aprove_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    send_c("disaprove_meme", args=f"&file_name={context.args[0]}", j=True)
    await update.message.reply_text("Disaproved")

async def aprove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    last_scan = time.time()

    keyboard = []
    types = []
    i = 0

    memes = send_c("get_memes_to_aprove")

    if len(memes) == 0:
        await update.message.reply_text("No hay memes disponibles", reply_markup=ReplyKeyboardMarkup([["/recargar_memes"], ["/start"]]))
    else:
        meme = memes[0]

        if meme["isvideo"]:
            await context.bot.reply_video(chat_id=update.effective_chat.id, photo=open(MEMES_LOCATION+meme["file_name"], "rb"))
            await update.message.reply_video(open(MEMES_LOCATION+meme["file_name"], "rb"))
        else:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(MEMES_LOCATION+meme["file_name"], "rb"))

        await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([[f"/aprove_meme {meme['file_name']}"], [f"/no_aprove_meme {meme['file_name']}"]]))

def add_c(n, f):
    available_commands.append(n)
    return CommandHandler(n,f)

async def Start_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/aprove", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))


app = ApplicationBuilder().token("5402422929:AAFILnDKzcTW3kjcY0OII-d7qviTghQmd8g").build()

app.add_handler(CommandHandler("start", Start_))
app.add_handler(add_c("recargar_memes", recargar_memes))
app.add_handler(add_c("aprove_meme", aprove_meme))
app.add_handler(add_c("no_aprove_meme", no_aprove_meme))
app.add_handler(add_c("help", hel))
app.add_handler(add_c("aprove", aprove))

app.add_handler(add_c("codigos_disponibles", memes_unchecked))
print("Starting")
app.run_polling()



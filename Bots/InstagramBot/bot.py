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

async def memes_checked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(len(send_c("get_aproved_memes")))

async def hel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Commands:")
    for c in available_commands:
        await update.message.reply_text("--- "+c)

async def help_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for c in send_c("help"):
        await update.message.reply_text(c)

async def reload_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Reloading")
    send_c("if_reload")
    await update.message.reply_text("Reloaded")

async def force_reload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Forcing reload")
    send_c("force_reload_requests_data")
    await update.message.reply_text("Reloaded")

async def download_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Downloading memes")
    send_c("download_all")
    await update.message.reply_text("Downloaded")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    data = query.data.split(":::")

    if data[0] == "YES":
        await update.effective_message.reply_text(send_c("aprove_meme", args=f"&file_name={data[1]}"))
    else:
        await update.effective_message.reply_text(send_c("disaprove_meme", args=f"&file_name={data[1]}"))

    update.message = update.effective_message

    await aprove(update, context)

async def new_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        username = context.args[0]

        send_c("new_account_to_steal", args=f"&username={username}")

        await update.message.reply_text(f"{username} added to list")
    else:
        await update.message.reply_text("Username argument missing")



async def new_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = "timordius"

    await update.message.reply_text("Uploading")

    await update.message.reply_text(send_c("new_meme", args=f"&username={username}", j=True))

async def aprove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    last_scan = time.time()

    keyboard = []
    types = []
    i = 0

    memes = send_c("get_memes_to_aprove")

    if len(memes) == 0:
        await update.message.reply_text("No hay memes disponibles", reply_markup=ReplyKeyboardMarkup([["/reload_memes"], ["/start"]]))
        return None
    else:
        for meme in memes:
            try:
                keyboard = InlineKeyboardMarkup([[ InlineKeyboardButton("👍", callback_data="YES:::"+meme['file_name'])], [InlineKeyboardButton("👎", callback_data="NO:::"+meme['file_name']) ]])


                if meme["isvideo"]:
                    print(asfdaf)
                    await context.bot.reply_video(chat_id=update.effective_chat.id, photo=open(meme["url"], "rb"))
                    """await update.message.reply_text("http://sw22.ddns.net:8081/Apis/InstagramBot/Content/Memes/"+meme["file_name"], reply_markup=keyboard)
                    await update.message.reply_video(open(MEMES_LOCATION+meme["file_name"], "rb"), reply_markup=keyboard)"""
                else:
                    await update.message.reply_text(f"From: {meme['account']}  likes: {meme['likes']}  views: {meme['views']} ")
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(MEMES_LOCATION+meme["file_name"], "rb"), reply_markup=keyboard)
            except Exception as e:
                await update.message.reply_text(str(e))
                print(e)
            else:
                return None
        await update.message.reply_text("No hay memes disponibles", reply_markup=ReplyKeyboardMarkup([["/reload_memes"], ["/start"]]))

def add_c(n, f):
    available_commands.append(n)
    return CommandHandler(n,f)

async def Start_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/aprove", "/new_meme"], ["/reload_memes", "/download_memes"], ["/memes_unchecked", "/memes_checked"], ["/help", "/force_reload"]]))


app = ApplicationBuilder().token("5402422929:AAFILnDKzcTW3kjcY0OII-d7qviTghQmd8g").build()

app.add_handler(CommandHandler("start", Start_))
app.add_handler(add_c("reload_memes", reload_memes))
app.add_handler(add_c("force_reload", force_reload))
app.add_handler(add_c("download_memes", download_memes))
app.add_handler(add_c("help", hel))
app.add_handler(add_c("aprove", aprove))
app.add_handler(add_c("new_meme", new_meme))

app.add_handler(add_c("memes_unchecked", memes_unchecked))
app.add_handler(add_c("memes_checked", memes_checked))
app.add_handler(add_c("new_a", new_account))
app.add_handler(CallbackQueryHandler(button))
print("Starting")
app.run_polling()



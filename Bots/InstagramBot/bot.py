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

async def recargar_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    send_c("if_reload")
    await update.message.reply_text("Reloaded")

async def download_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        await update.message.reply_text(send_c("aprove_meme", args=f"&file_name={data[1]}", j=True))
    else:
       await update.message.reply_text( send_c("disaprove_meme", args=f"&file_name={data[1]}", j=True))

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
        await update.message.reply_text("No hay memes disponibles", reply_markup=ReplyKeyboardMarkup([["/recargar_memes"], ["/start"]]))
    else:
        for meme in memes:
            try:

                keyboard = InlineKeyboardMarkup([[ InlineKeyboardButton("👍", callback_data="YES:::"+meme['file_name'])], [InlineKeyboardButton("👎", callback_data="NO:::"+meme['file_name']) ]])

                if meme["isvideo"]:
                    await context.bot.reply_video(chat_id=update.effective_chat.id, photo=open(MEMES_LOCATION+meme["file_name"], "rb"))
                    await update.message.reply_video(open(MEMES_LOCATION+meme["file_name"], "rb"), reply_markup=keyboard)
                else:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(MEMES_LOCATION+meme["file_name"], "rb"), reply_markup=keyboard)
            except:
                pass
            else:
                break
def add_c(n, f):
    available_commands.append(n)
    return CommandHandler(n,f)

async def Start_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/aprove", "/new_meme"], ["/recargar_memes", "/download_memes"], ["/memes_unchecked", "/memes_checked"], ["/help"]]))


app = ApplicationBuilder().token("5402422929:AAFILnDKzcTW3kjcY0OII-d7qviTghQmd8g").build()

app.add_handler(CommandHandler("start", Start_))
app.add_handler(add_c("recargar_memes", recargar_memes))
app.add_handler(add_c("download_memes", download_memes))
app.add_handler(add_c("help", hel))
app.add_handler(add_c("aprove", aprove))
app.add_handler(add_c("new_meme", new_meme))

app.add_handler(add_c("memes_unchecked", memes_unchecked))
app.add_handler(add_c("memes_checked", memes_checked))
app.add_handler(CallbackQueryHandler(button))
print("Starting")
app.run_polling()



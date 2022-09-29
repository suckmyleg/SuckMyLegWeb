from telegram import *
from telegram.ext import *
import requests
import json
import time

MEMES_LOCATION = "/var/www/html/Apis/InstagramBot/Content/Memes/"

available_commands = []

bots_selected = {}

def send_c(c, args="", j=False):
    url = f"http://192.168.1.104:8080/Apis/Gym/?c={c}"+args
    print(url)
    r = requests.get(url).content.decode("utf-8")

    if r == "Apy busy or off":
        return False

    #print(r)
    if j:
        return r
    try:
        return json.loads(r)
    except:
        return r

def get_last(username, data):
    send_c("get_last", f"&username={username}&data={data}")

class Person:
    def __init__(self, username):
        self.username = username
        self.data = {}

    def get_height(self):
        return self.get("height")
    def get_weight(self):
        return self.get("weight")
    def get_arm_radius(self):
        return self.get("arm_radius")
    def get_body_radius(self):
        return self.get("body_radius")
    def get_leg_radius(self):
        return self.get("leg_radius")
    def get_machines_settings(self):
        return self.get("machines_settings")
    def get_machines_prs(self):
        return self.get("machines_prs")

    def get(self, data):
        try:
            return self.data[data]
        except:
            value = get_last(self.username, data)
            self.data[data] = value
            return value

def get_bots_available():
    bots = []

    for b in send_c("info_account"):
        if b["status_code"] == 2:
            bots.append(b)
    return bots

async def bot_selected(update, context):
    try:
        return bots_selected[update.effective_chat.id]
    except:
        await select_bot(update, context)
        return False
async def memes_unchecked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    unchecked = send_c("get_memes_to_aprove")

    if unchecked == False:
        await update.message.reply_text("Cant connect to server")
    else:
        await update.message.reply_text(len(unchecked))

async def memes_checked(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    aproved = send_c("get_aproved_memes")

    if aproved == False:
        await update.message.reply_text("Cant connect to server")
    else:
        await update.message.reply_text(len(aproved))

async def hel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Commands:")
    for c in available_commands:
        await update.message.reply_text("--- "+c)

async def help_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for c in send_c("help"):
        await update.message.reply_text(c)

async def reload_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Reloading")
    if send_c("if_reload") == False:
        await update.message.reply_text("Couldnt reload")
    else:
        await update.message.reply_text("Reloaded")

async def force_reload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Forcing reload")
    if send_c("force_reload_requests_data") == False:
        await update.message.reply_text("Couldnt reload")
    else:
        await update.message.reply_text("Reloaded")

async def download_memes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Downloading memes")
    if send_c("download_all") == False:
        await update.message.reply_text("Couldnt download")
    else:
        await update.message.reply_text("Downloaded")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    data = query.data.split("::")

    if data[0] == "a":
        if data[1] == "YES":
            await update.effective_message.reply_text(send_c("aprove_meme", args=f"&file_name={data[2]}"))
        else:
            await update.effective_message.reply_text(send_c("disaprove_meme", args=f"&file_name={data[2]}"))

        update.message = update.effective_message

        await aprove(update, context)

    elif data[0] == "new_meme":

        username = data[1]

        await update.effective_message.reply_text("Uploading")

        await update.effective_message.reply_text(send_c("new_meme", args=f"&username={username}", j=False))

    elif data[0] == "select":
        bots_selected[update.effective_chat.id] = data[1] 

        await update.effective_message.reply_text(f"Selected bot {data[1]}")

async def new_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        username = context.args[0]

        send_c("new_account_to_steal", args=f"&username={username}")

        await update.message.reply_text(f"{username} added to list")
    else:
        await update.message.reply_text("Username argument missing")



async def new_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keys = []

    lans = {"es/Sp":"🇪🇸", "es/Ar":"🇦🇷", "en/En":"🇬🇧"}

    for bot in get_bots_available():
        keys.append([InlineKeyboardButton(f"🤖{bot['username']}{lans[bot['lan']]} {time.strftime('%H:%M:%S', time.gmtime(int(time.time()-bot['last_publish'])))}", callback_data=f"new_meme::{bot['username']}")])

    keyboard = InlineKeyboardMarkup(keys)

    await update.message.reply_text("Select a bot:", reply_markup=keyboard)

async def select_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keys = []

    lans = {"es/Sp":"🇪🇸", "es/Ar":"🇦🇷", "en/En":"🇬🇧"}

    for bot in get_bots_available():
        bot_keys = []

        status = "🔴"
        if bot["logged"]:
            status = "🟢"

        bot_keys.append(InlineKeyboardButton(f"{status} {bot['username']} {lans[bot['lan']]} {time.strftime('%H:%M:%S', time.gmtime(int(time.time()-bot['last_publish'])))}", callback_data=f"select::{bot['username']}"))
        keys.append(bot_keys)

    keyboard = InlineKeyboardMarkup(keys)

    await update.message.reply_text("Bots:", reply_markup=keyboard)


async def selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sel = await bot_selected(update, context)

    await update.message.reply_text(sel)

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
                print("k", meme['file_name'], f"a::NO::{meme['file_name']}")
                keyboard = InlineKeyboardMarkup([
                    [ InlineKeyboardButton("👍", callback_data=f"a::YES::{meme['file_name']}") ], 
                    [ InlineKeyboardButton("👎", callback_data=f"a::NO::{meme['file_name']}") ]
                    ])

                print("c")
                if meme["isvideo"]:
                    await update.message.reply_text(f"From: {meme['account']}  likes: {meme['likes']}  views: {meme['views']} ")
                    await update.message.reply_text(meme["url"], reply_markup=keyboard)
                else:
                    print("i")
                    await update.message.reply_text(f"From: {meme['account']}  likes: {meme['likes']}  views: {meme['views']} ")
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get(meme["url"]).content, reply_markup=keyboard)
            except Exception as e:
                #await update.message.reply_text(f"{str(e)} {json.dumps(meme)}")
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
app.add_handler(add_c("selected", selected))

app.add_handler(add_c("memes_unchecked", memes_unchecked))
app.add_handler(add_c("memes_checked", memes_checked))
app.add_handler(add_c("new_a", new_account))
app.add_handler(add_c("select_bot", select_bot))
app.add_handler(CallbackQueryHandler(button))
print("Starting")
app.run_polling()



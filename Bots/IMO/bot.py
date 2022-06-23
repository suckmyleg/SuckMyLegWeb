from telegram import *
from telegram.ext import *
import requests
import json
import time

last_scan = 0

delay_scan = 5*60

available_commands = []

def send_c(c, args="", j=False):
    url = f"http://192.168.1.104:8080/Apis/IMO/?c={c}"+args
    print(url)
    r = requests.get(url).content.decode("utf-8")

    #print(r)
    if j:
        return r
    return json.loads(r)

def get_qrs():
    return send_c("get_qrs")

def time_to_wait():
    passed = time.time() - last_scan

    if passed < delay_scan and passed >= 0:
        return passed
    return False

def check_available():
    if until_pay() <= 0:
        return False
    return True

def until_pay():
    return send_c("get_max_handle_ammount") - send_c("get_money_handled")

async def qrs_available_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(len(get_qrs()))

async def get_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for qr in get_qrs():
        await update.message.reply_text(qr["type"])

async def hel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Commands:")
    for c in available_commands:
        await update.message.reply_text("--- "+c)

async def help_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for c in send_c("help"):
        await update.message.reply_text(c)

async def get_qr_to_do(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get_qr_to_do", j=True))

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get", j=True))

async def total_money(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("total_money", j=True))

async def my_money(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("my_money", j=True))

async def get_money_paid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get_money_paid", j=True))

async def get_money_handled(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get_money_handled", j=True))

async def get_max_handle_ammount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get_max_handle_ammount", j=True))

async def get_max_handle_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(send_c("get_max_handle_days", j=True))

async def qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tt = time_to_wait()

    if not check_available():
        await update.message.reply_text(f"Escaneado de qr bloqueado hasta que se transfieran los {send_c('get_money_handled')} euros a la cuenta")
    elif not tt == False:
        await update.message.reply_text(f"{tt} segundos hasta el siguiente escaneo")
    else:
        last_scan = time.time()

        keyboard = []
        types = []
        i = 0

        qrs = get_qrs()

        if len(qrs) == 0:
            await update.message.reply_text("No hay codigos qr disponible por hoy")
        else:
            for q in qrs:
                if not q["type"] in types:
                    keyboard.append(["/"+q["type"]])
                    types.append(q["type"])

            markup = ReplyKeyboardMarkup(keyboard)

            await update.message.reply_text("Selecciona tipo qr", reply_markup=markup)

        

async def get_qr_free_full_hd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "free_full_hd":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))

async def get_qr_free_triple_espuma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))

async def get_qr_1e(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "1e":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))

async def get_qr_2e(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "2e":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))

async def get_qr_full_hd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "full_hd":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))

async def get_qr_triple_espuma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent = False
    for q in get_qrs():
        if q["type"] == "triple_espuma":
            sent=True
            o = send_c("get", f"&mail={q['email']}&type={q['type']}")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=requests.get("http://192.168.1.104:8081/Apps/IMO/"+o["src"]).content)
            await update.message.reply_text(o["code"])
    if not sent:
        await update.message.reply_text("Error obteniendo el codigo qr\nA lo mejor ya se ha canjeado")
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))


def add_c(n, f):
    available_commands.append(n)
    return CommandHandler(n,f)

async def Start_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(".", reply_markup=ReplyKeyboardMarkup([["/qr", "/help"], ["/dinero_propio", "/dinero_conseguido"], ["/deuda", "/dinero_pagado"], ["/codigos_disponibles"]]))


app = ApplicationBuilder().token("5498985401:AAGHsqIdKBDxn5L0Aohv9rLTJ015ik9j9yE").build()

app.add_handler(CommandHandler("start", Start_))
app.add_handler(add_c("triple_espuma", get_qr_triple_espuma))
app.add_handler(add_c("full_hd", get_qr_full_hd))
app.add_handler(add_c("2e", get_qr_2e))
app.add_handler(add_c("1e", get_qr_1e))
app.add_handler(add_c("free_triple_espuma", get_qr_free_triple_espuma))
app.add_handler(add_c("free_full_hd", get_qr_free_full_hd))
#app.add_handler(add_c("help_api", help_api))
app.add_handler(add_c("help", hel))
app.add_handler(add_c("qr", qr))
#app.add_handler(add_c("get_qr_to_do", get_qr_to_do))
app.add_handler(add_c("dinero_conseguido", total_money))
app.add_handler(add_c("dinero_propio", my_money))
app.add_handler(add_c("dinero_pagado", get_money_paid))
app.add_handler(add_c("deuda", get_money_handled))
app.add_handler(add_c("deuda_maxima", get_max_handle_ammount))
app.add_handler(add_c("codigos_disponibles", qrs_available_today))
#app.add_handler(add_c("dias_a_pagar", get_max_handle_days))
print("Starting")
app.run_polling()



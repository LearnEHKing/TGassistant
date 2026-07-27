import json
import asyncio
import random
import pyjokes
import randfacts
from quote import quote
from zoneinfo import ZoneInfo
from periods import Periods
from datetime import datetime, time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler, 
    filters
)

periods=Periods()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  add_user(app,user)
  await update.message.reply_text(context.bot_data["msg"]["/start"])
  
async def receive_message(update, context):
    sender = update.effective_user
    text = update.message.text
    abc_text="".join(c for c in text if c.isalpha())
    try :
      await context.bot.send_message(
          chat_id=sender.id,
          text=context.bot_data["msg"][abc_text.lower()]
      )
    except Exception:
      if abc_text.lower() in context.bot_data["msg"]["hlw"]:
        await context.bot.send_message(
          chat_id=sender.id,
          text=random.choice(context.bot_data["msg"]["greetings"])
        )
      else:
        await context.bot.send_message(
            chat_id=sender.id,
            text=context.bot_data["msg"]["text_reply"]
        )
    # Ignore your own messages
    if str(sender.id) !=context.bot_data["config"]["OWNER_ID"]:
        await context.bot.send_message(
            chat_id=context.bot_data["config"]["OWNER_ID"],
            text=f"📩 {sender.first_name}:\n\n{text}"
        )



async def next_period(update, context):
  date = periods.next_period(update.effective_user.id)
  if date is None:
    await update.message.reply_text(f"User history not found.")
  await update.message.reply_text(f"Next period is expected to be on {date}.")

async def next_ovulation(update, context):
  date = periods.next_ovulation(update.effective_user.id)
  if date is None:
    await update.message.reply_text(f"User histroy not found.")
  await update.message.reply_text(f"Next ovulation is expected on {date}.")

async def period_history(update, context):
    history = periods.period_history(update.effective_user.id)

    if history is None:
        await update.message.reply_text("No period history found.")
        return

    text = "\n".join(
    f"{i}. {date}"
    for i, date in enumerate(history, start=1)
    )

    await update.message.reply_text(f"Period history:\n{text}")

async def log_last_period(update, context):
  if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /log_last_period DD-MM-YYYY"
        )
        return

  try:
      date = str(datetime.strptime(context.args[0], "%d-%m-%Y").strftime("%d-%m-%Y"))
  except ValueError:
      await update.message.reply_text(
          "Invalid date. Use DD-MM-YYYY."
      )
      return
  print(date)
  periods.log_period(update.effective_user.id, date)

  await update.message.reply_text("Period date saved.")
  
async def log_period(update, context): 
  periods.log_period(update.effective_user.id, str(datetime.now().strftime("%d-%m-%Y")))
  await update.message.reply_text("Period date saved.")
  
async def joke_user(update, context): 
  await update.message.reply_text(pyjokes.get_joke())
  
async def fact_user(update, context): 
  await update.message.reply_text(f"A great fact:\n{randfacts.get_fact()}")
  
async def quote_user(update, context): 
  await update.message.reply_text(f"Quote for you...\n{random.choice(quote("love"))}")
  
async def good_morning(context):
    for user in context.bot_data["users"]:
        await context.bot.send_message(
            chat_id=user["id"],
            text=random.choice(context.bot_data["msg"]["good_morning"])
        )
      
async def good_night(context):
    for user in context.bot_data["users"]:
        await context.bot.send_message(
            chat_id=user["id"],
            text=random.choice(context.bot_data["msg"]["good_night"])
        )
      
async def jokes(context: ContextTypes.DEFAULT_TYPE):
    for user in context.bot_data["users"]:
        await context.bot.send_message(
            chat_id=user["id"],
            text=f"Todays joke.\n{pyjokes.get_joke()}"
        )
      
async def send_quote(context: ContextTypes.DEFAULT_TYPE):
    for user in context.bot_data["users"]:
        await context.bot.send_message(
            chat_id=user["id"],
            text=f"Todays quote.\n{random.choice(quote("life"))}"
        )
      
async def facts(context: ContextTypes.DEFAULT_TYPE):
    for user in context.bot_data["users"]:
        await context.bot.send_message(
            chat_id=user["id"],
            text=f"Todays fact.\n{randfacts.get_fact()}"
        )


async def daily_period_check(context):
    today = datetime.now().date()

    for user in context.bot_data["users"]:
        user_id = user["id"]

        next_period = datetime.strptime(
            periods.next_period(user_id),
            "%d-%m-%Y"
        ).date()

        if today == next_period - timedelta(days=2):
            await context.bot.send_message(
                chat_id=user_id,
                text="Your period is expected in 2 days."
            )
            await context.bot.send_message(
                  chat_id=context.bot_data["config"]["owner"],
                  text=f"{user["full_name"]}'s period is expected in 2 days."
            )
          
        if today == next_period - timedelta(days=1):
            await context.bot.send_message(
                chat_id=user_id,
                text="Your period is expected to be tomorrow. Be ready. Don't go to school tomorrow if possible."
            )
            await context.bot.send_message(
                  chat_id=context.bot_data["config"]["owner"],
                  text=f"{user["full_name"]}'s period is expected in tomorrow."
            )

        if today == next_period:
            await context.bot.send_message(
                chat_id=user_id,
                text="Your period is expected to start today. Take care of yourself. Rest well. Message me whenerver needed."
            )
            await context.bot.send_message(
                  chat_id=context.bot_data["config"]["owner"],
                  text=f"{user["full_name"]}'s period is expected in today."
            )

def dataInitialize(app):
  with open("Data/messages.json") as f:
      MESSAGES = json.load(f)
  with open("Data/users.json") as f:
    users = json.load(f)
  app.bot_data["msg"] = MESSAGES
  app.bot_data["users"] = users

def add_user(app,user):
    # Add user if not present
  if not any(u["id"]==user.id for u in app.bot_data["users"]):
    app.bot_data["users"].append({ "id":user.id, "username":user.name,"full_name":user.full_name,"join_date":str(datetime.now())})
    with open("Data/users.json", "w") as f:
      json.dump(app.bot_data["users"], f, indent=4)
      



if __name__ == '__main__':
  
  with open("Data/config.json") as f:
      CONFIG = json.load(f)
    
  app = Application.builder().token( CONFIG["TOKEN"] ).build()
  
  app.bot_data["config"] = CONFIG
  
  dataInitialize(app)

  
  app.add_handler(CommandHandler( "start", start))
  app.add_handler(CommandHandler( "next_period", next_period))
  app.add_handler(CommandHandler( "next_ovulation", next_ovulation))
  app.add_handler(CommandHandler( "period_history", period_history))
  app.add_handler(CommandHandler( "log_last_period", log_last_period))
  app.add_handler(CommandHandler( "log_period", log_period))
  app.add_handler(CommandHandler( "joke", joke_user))
  app.add_handler(CommandHandler( "random_fact", fact_user))
  app.add_handler(CommandHandler( "random_quote", quote_user))
  
  job_queue = app.job_queue
  IST = ZoneInfo("Asia/Kolkata")

  job_queue.run_daily(
      good_morning,
      time=time(hour=6, minute=0, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  
  job_queue.run_daily(
      jokes,
      time=time(hour=9, minute=00, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  job_queue.run_daily(
      jokes,
      time=time(hour=16, minute=00, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  
  job_queue.run_daily(
      good_night,
      time=time(hour=22, minute=30, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  job_queue.run_daily(
      facts,
      time=time(hour=13, minute=30, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  job_queue.run_daily(
      send_quote,
      time=time(hour=11, minute=30, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     },)
  
  job_queue.run_daily(
      daily_period_check,
      time=time(hour=7,minute=30, tzinfo=IST),
      job_kwargs={         "misfire_grace_time": 15000,     }, 
  )
  app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)
  )
  print("Bot is running...")
  app.run_polling()

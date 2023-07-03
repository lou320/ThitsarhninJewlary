#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from BACKEND import get_file_name, get_dir
from database import create_tables, add_item_to_database, fetch_items_from_database,search_by_name, remove_item_from_database,get_sold_items_from_database,mark_item_as_sold,get_items_sold_today_from_database
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

ADDING_ITEM_IMAGE,ADDING_ITEM_NAME, ADDING_BOUGHT_VALUE, ADDING_ITEM_GRAM, ADDING_BOUGHT_AYOTTWAT, ADDING_SELL_AYOTTWAT, SEARCH_BY_NAME,REMOVE_BY_ID, SOLD_ITEM  = range(9)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Welcome, I'm a bot to help Thitsar Hnin Jewelry Shop.")


async def createdatabase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    create_teble = create_tables()
    if create_teble:
        await update.message.reply_text('Database created!')
    else:
        await update.message.reply_text('Something wrong!')

    
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    await update.message.reply_text(
        "ပစ္စည်းပုံထည့်ပါ"
        ),
    return ADDING_ITEM_IMAGE


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    photo_file_name = get_file_name(file_path=photo_file.file_path)
    directory = get_dir('images')
    image = (directory+'/'+photo_file_name)
    await photo_file.download_to_drive(image)
    context.chat_data['image'] = image
    await update.message.reply_text(
        "ပစ္စည်းအမည်ထည့်ပါ"
    )

    return ADDING_ITEM_NAME

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return ConversationHandler.END

async def item_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    item_name = update.message.text
    await update.message.reply_text("ဝယ်ယူထားသောစျေးနှုန်းထည့်ပါ")
    context.chat_data['item_name'] = item_name
    return ADDING_BOUGHT_VALUE

async def bought_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    item_bought_value = update.message.text
    await update.message.reply_text("ပစ္စည်းအလေးချိန်ထည့်ပါ(Gram)")
    context.chat_data['item_bought_value'] = item_bought_value
    return ADDING_ITEM_GRAM

async def item_gram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    item_gram = update.message.text
    await update.message.reply_text("ဝယ်ရင်းပစ္စည်းအရော့တွက်ထည့်ပါ")
    context.chat_data['item_gram'] = item_gram
    return ADDING_BOUGHT_AYOTTWAT

async def bought_ayottwat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    item_bought_ayottwat = update.message.text
    await update.message.reply_text('ရောင်းမည့်အရော့တွက်ထည့်ပါ')
    context.chat_data['bought_ayottwat'] = item_bought_ayottwat
    return ADDING_SELL_AYOTTWAT

async def sell_ayottwat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    item_sell_ayottwat = update.message.text
    image = context.chat_data.get('image')
    item_name = context.chat_data.get('item_name')
    item_bought_value = context.chat_data.get('item_bought_value')
    item_item_gram = context.chat_data.get('item_gram')
    item_bought_ayottwat = context.chat_data.get('bought_ayottwat')
    try:
        item = add_item_to_database(image,item_name,item_bought_value,item_item_gram,item_bought_ayottwat,item_sell_ayottwat)
        await update.message.reply_text('ပစ္စည်းအသစ်ထည့်ခြင်းအောင်မြင်ပါသည် \n ပစ္စည်း ID: '+ str(item) )
        context.chat_data.clear()
    except Exception as e:
        try:
            os.remove(image)
        except OSError as a:
            pass
        await update.message.reply_text('ပစ္စည်းအသစ်ထည့်ခြင်းမအောင်မြင်ပါ"\nထပ်မံကြိုးစားပါ')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "လုပ်ငန်းစဉ်ပယ်ဖျက်လိုက်ပါပြီ"
    )
    image = context.chat_data.get('image')
    if image:
        try:
            os.remove(image)
        except OSError as a:
            pass
        return ConversationHandler.END
			return ConversationHandler.END

async def show_all_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ထည့်သွင်းထားသောပစ္စည်းများ"
    )
    items = fetch_items_from_database()
    for item in items:
        if item['is_sold']:
            sold = ('ရောင်းပြီး\nSoldDate:'+ str(item['sold_date']))
        else:
            sold = 'မရောင်းရသေး'
        image_path = item['image_url']
        text = f"ID#{item['id']} {item['item_name']}\n\n{sold}\n\nPostDate:{item['posted_date']}\n\nပစ္စည်းအလေးချိန် - {item['item_gram']}\n\nဝယ်ရင်းစျေး- {item['bought_value']}\n\nဝယ်ရင်းပစ္စည်းအရော့တွက် - {item['bought_ayottwat']} \n\nရောင်းမည့်အရော့တွက် - {item['sell_ayottwat']} "
        await update.message.reply_photo(photo=open(image_path, 'rb'), caption=text)


async def get_sold_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_sold_items_from_database()
    if isinstance(items, list) and len(items) > 0:
        await update.message.reply_text("ရောင်းပြီးပစ္စည်းများ")
        for item in items:
            if item['is_sold']:
                sold = ('ရောင်းပြီး\nSoldDate:'+ str(item['sold_date']))
            else:
                sold = 'မရောင်းရသေး'
            image_path = item['image_url']
            text = f"ID#{item['id']} {item['item_name']}\n\n{sold}\n\nPostDate:{item['posted_date']}\n\nပစ္စည်းအလေးချိန် - {item['item_gram']}\n\nဝယ်ရင်းစျေး- {item['bought_value']}\n\nဝယ်ရင်းပစ္စည်းအရော့တွက် - {item['bought_ayottwat']} \n\nရောင်းမည့်အရော့တွက် - {item['sell_ayottwat']} "
            await update.message.reply_photo(photo=open(image_path, 'rb'), caption=text)
    else:
        await update.message.reply_text('ရောင်းထားသောပစ္စည်းမရှိပါ')

async def get_today_sold_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_items_sold_today_from_database()
    if isinstance(items, list) and len(items) > 0:
        await update.message.reply_text("ယနေ့ရောင်းပြီးပစ္စည်းများ")
        for item in items:
            if item['is_sold']:
                sold = ('ရောင်းပြီး\nSoldDate:'+ str(item['sold_date']))
            else:
                sold = 'မရောင်းရသေး'
            image_path = item['image_url']
            text = f"ID#{item['id']} {item['item_name']}\n\n{sold}\n\nPostDate:{item['posted_date']}\n\nပစ္စည်းအလေးချိန် - {item['item_gram']}\n\nဝယ်ရင်းစျေး- {item['bought_value']}\n\nဝယ်ရင်းပစ္စည်းအရော့တွက် - {item['bought_ayottwat']} \n\nရောင်းမည့်အရော့တွက် - {item['sell_ayottwat']} "
            await update.message.reply_photo(photo=open(image_path, 'rb'), caption=text)
    else:
        await update.message.reply_text('ရောင်းထားသောပစ္စည်းမရှိပါ')

async def sold_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ရောင်းချပြီးသည့် ပစ္စည်း ID ထည့်ပါ")
    return SOLD_ITEM


async def sold_item_to_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id = update.message.text
    success = mark_item_as_sold(item_id)
    if success:
        await update.message.reply_text('Success')
    else:
        await update.message.reply_text('လုပ်ငန်းစဉ်မအောင်မြင်ပါ')
    return ConversationHandler.END

async def search_with_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ရှာဖွေရန်ပစ္စည်းအမည်ထည့်ပါ"
    )
    return SEARCH_BY_NAME
    
async def name_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_query = update.message.text
    items = search_by_name(search_query)
    if not type(items) == str:
        for item in items:
            if item['is_sold']:
                sold = ('ရောင်းပြီး\nSoldDate:'+ str(item['sold_date']))
            else:
                sold = 'မရောင်းရသေး'
            image_path = item['image_url']
            text = f"ID#{item['id']} {item['item_name']}\n\n{sold}\n\nPostDate:{item['posted_date']}\n\nပစ္စည်းအလေးချိန် - {item['item_gram']}\n\nဝယ်ရင်းစျေး- {item['bought_value']}\n\nဝယ်ရင်းပစ္စည်းအရော့တွက် - {item['bought_ayottwat']} \n\nရောင်းမည့်အရော့တွက် - {item['sell_ayottwat']} "
            await update.message.reply_photo(photo=open(image_path, 'rb'), caption=text)
    else:
        await update.message.reply_text(items)
    return ConversationHandler.END


async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ဖျက်မည့်ပစ္စည်း ID ထည့်ပါ"
    )
    return REMOVE_BY_ID
    
async def remove_itembyid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remove_id = update.message.text
    try:
        int(remove_id)
    except:
        await update.message.reply_text('ဖျက်မည့်ပစ္စည်း ID(English အက္ခရာနာမ်ပတ်)တစ်မျိုးတည်းသာထည့်သွင်းပါ')
        return REMOVE_BY_ID
    
    success = remove_item_from_database(remove_id)
    if success:
        await update.message.reply_text('ဖျက်ချင်းအောင်မြင်ပါသည်')
    else:
        await update.message.reply_text('ဖျက်ချင်းမအောင်မြင်ပါ')
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6140436066:AAFEgaSEbrZ5UkWZYb_ls8YYUq2WwaEt964").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("createdatabase", createdatabase))
    application.add_handler(CommandHandler("show_all_items", show_all_items))
    application.add_handler(CommandHandler("all_time_sold", get_sold_items))
    application.add_handler(CommandHandler("today_sold", get_today_sold_items))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_item)],
        states={
            ADDING_ITEM_IMAGE: [MessageHandler(filters.PHOTO & ~filters.COMMAND, photo), CommandHandler("skip", skip_photo)],
            ADDING_ITEM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, item_name)],
            ADDING_BOUGHT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bought_value)],
            ADDING_ITEM_GRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, item_gram)],
            ADDING_BOUGHT_AYOTTWAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bought_ayottwat)],
            ADDING_SELL_AYOTTWAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, sell_ayottwat)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    name_search_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('name_search', search_with_name)],
        states={
            SEARCH_BY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_search)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    item_remove_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('remove', remove_item)],
        states={
            REMOVE_BY_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_itembyid)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    sold_item_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('sell_item', sold_item)],
        states={
            SOLD_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, sold_item_to_database)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # Run the bot until the user presses Ctrl-C
    application.add_handler(conv_handler)
    application.add_handler(name_search_conv_handler)
    application.add_handler(item_remove_conv_handler)
    application.add_handler(sold_item_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
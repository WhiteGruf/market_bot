import telebot
from telebot import types
import product_card as pc
import time
import schedule
from threading import Thread

first_card = pc.File()
card_number = 0

def parse():
    global first_card
    while True:
        first_card = pc.File()
        time.sleep(60)

bot = telebot.TeleBot("5737635351:AAENJHaNvvjl26nx926lCOXgeMsSbsUr0SU")



#ФУНКЦИЯ ОТПРАВКИ КАРТОЧЕК ТОВАРОВ
def card_send(message,  first_card_data, size):
    global first_card
    global card_number
    
    if card_number==size:
        card_number=0
    if card_number<0:
        card_number=size-1
    
    txt=str('<strong>'+first_card_data[card_number][0]) + '</strong>    ' +str(first_card_data[card_number][2]) +"\nЦена:"+ str(first_card_data[card_number][1])+u'\U000020BD'
    
    webAppTest = types.WebAppInfo(first_card_data[card_number][4]) #создаем webappinfo - формат хранения url
    markup = types.InlineKeyboardMarkup(row_width=3)
    #Кнопки переключения товара
    item1 = types.InlineKeyboardButton(text="Назад", callback_data="previosly")
    item2 = types.InlineKeyboardButton(text=str(card_number+1)+" из " + str(size), callback_data="card number")
    item3 = types.InlineKeyboardButton(text="Вперёд", callback_data="next")
    url_btn = types.InlineKeyboardButton(text="Подробнее", web_app=webAppTest)#url_btn = types.InlineKeyboardButton(text="Подробнее", url = first_card_data[card_number][4] )
    markup.add(item1,item2,item3,url_btn)
    #bot.send_message(message.chat.id, text=txt, reply_markup=markup)
    try: 
        # bot.edit_message_caption(chat_id=message.chat.id,message_id=message.message_id,caption= txt, reply_markup=markup)  
        bot.edit_message_media(chat_id=message.chat.id,message_id=message.message_id,media=types.InputMediaPhoto(first_card_data[card_number][3], caption=txt, parse_mode='HTML'),reply_markup=markup)     
    except Exception as e:
        
        bot.send_photo(message.chat.id, photo=first_card_data[card_number][3], caption=txt, reply_markup=markup, parse_mode='HTML')
        #raise e

@bot.message_handler(commands=['start'])
def start(message):
    text = "Привет. Напиши мне, что ты ищешь и я помогу тебе это найти."
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def card(message):
    global first_card
    global card_number
    global size
    global first_card_data
    card_number = 0
    
    first_card_data = first_card.search(message.text)
    if first_card_data:
        size = len(first_card_data)
        card_send(message,  first_card_data, size)
    else:
        bot.send_message(message.chat.id, "Извините, такого товара не найдено, попробуйте что-то другое.")
@bot.callback_query_handler(func=lambda callback: True)
def work(callback):
    global card_number
    global size
    global first_card_data
    if callback.data == "previosly":
        card_number-=1
    elif callback.data == "card number":
        pass
    elif callback.data == "next":
        card_number+=1
    card_send(callback.message,  first_card_data, size)

Thread(target=parse).start()

bot.infinity_polling()
    
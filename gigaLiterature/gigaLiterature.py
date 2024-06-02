from telebot.async_telebot import AsyncTeleBot
import asyncio
bot = AsyncTeleBot('') #TelegramToken
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='', scope='GIGACHAT_API_PERS', verify_ssl_certs=False) #GigaChatToken(ends with Q==)



user_requests = {}
initial_request = SystemMessage(
        content="Ты - литературовед. Ты умный бот-литературовед, который помогает пользователю найти интересные книги! Тебя зовут gigaLiterature"
    )

def add_user(user_id):
    if user_id not in user_requests:
        user_requests[user_id] = {

            'requests': [initial_request]
        }



def add_request(user_id, new_request):
    if user_id not in user_requests:
        add_user(user_id)

    user_requests[user_id]['requests'].append(new_request)



# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привет, я умный бот-литературовед, который помогает пользователю найти интересные книги!\n
Чем я могу вам помочь?
""")

@bot.message_handler(commands=['clear'])
async def send_clear(message):
    userId = message.from_user.id
    user_requests[userId]['requests'].clear()
    add_request(userId, initial_request)
    await bot.reply_to(message, """\
    Диалог очищен!\n
Привет, я умный бот-литературовед, который помогает пользователю найти интересные книги!\n
Чем я могу вам помочь?
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def send_message(message):
    userId = message.from_user.id
    add_request(userId, HumanMessage(content=message.text))
    print(userId, 'USER: ', message.text)
    res = chat(user_requests[userId]['requests'])

    add_request(userId, res)
    print(userId, 'BOT: ', res.content)
    print(user_requests)
    await bot.reply_to(message, res.content)


asyncio.run(bot.polling())

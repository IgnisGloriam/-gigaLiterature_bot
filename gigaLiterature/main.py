from telebot.async_telebot import AsyncTeleBot
import asyncio
bot = AsyncTeleBot('')
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


# Авторизация в сервисе GigaChat
chat = GigaChat(credentials='', scope='GIGACHAT_API_PERS', verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты умный бот-литературовед, который помогает пользователю найти интересные книги."
    )
]


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привет, я умный бот-литературовед, который помогает пользователю найти интересные книги!\
Чем я могу вам помочь?
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    print('USER: ', message.text)
    messages.append(HumanMessage(content=message.text))
    res = chat(messages)
    messages.append(res)
    print('BOT: ', res.content)
    await bot.reply_to(message, res.content)


asyncio.run(bot.polling())

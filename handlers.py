from main import bot, dp
from keyboards import keyboard
from aiogram import types
from config import PAYMENTS_TOKEN
from aiogram.dispatcher.filters import Command

@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Тест WebApp!',
                           reply_markup=keyboard)

PRICE = {
    '1': [types.LabeledPrice(label='Item1', amount=4200000)],
    '2': [types.LabeledPrice(label='Item2', amount=4300000)],
    '3': [types.LabeledPrice(label='Item3', amount=4350000)],
    '4': [types.LabeledPrice(label='Item4', amount=4400000)],
    '5': [types.LabeledPrice(label='Item5', amount=4450000)],
    '6': [types.LabeledPrice(label='Item6', amount=4500000)]
}

@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(web_app_message.chat.id,
                               title='ApplePhone',
                               description='Description',
                               provider_token=PAYMENTS_TOKEN,
                               currency='UAH',
                               photo_url=f"https://boxxxxxer.github.io/payments_bot/{web_app_message.web_app_data.data}.png",
                               photo_width=416,
                               photo_height=234,
                               photo_size=416,
                               need_email=False,
                               prices=PRICE[f'{web_app_message.web_app_data.data}'],
                               start_parameter='one-month-subscription',
                               payload='test-invoice-payload')


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, '👍')

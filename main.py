from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
os.environ['DISPLAY'] = ':0'
print(os.environ['DISPLAY'])
import pywhatkit


bot = Bot(token='5356920926:AAFlcyTE4Z-zZZOnHvKS815w0ENs2miG_Lc')
dp = Dispatcher(bot, storage=MemoryStorage())

button = KeyboardButton('/Ввести_номера')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(button)


class FSMWait(StatesGroup):
    waiting_for_phones = State()
    waiting_for_text = State()


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Выберите команду', reply_markup=kb_client)


@dp.message_handler(commands=['Ввести_номера'], state='*')
async def start_command(msg: types.Message):
    await FSMWait.waiting_for_phones.set()
    await msg.answer('Введите номера телефонов')


@dp.message_handler(state=FSMWait.waiting_for_phones)
async def users_message(message: types.Message, state: FSMContext):
    await state.update_data(numbers=message.text)
    global numbers
    async with state.proxy() as data:
        data['waiting_for_phones'] = message.text
    numbers = data['waiting_for_phones']
    numbers = (numbers.replace(' ', '').split(','))

    if len(numbers) < 10:
        await message.answer('Введено менее 10 номеров')

    else:
        await FSMWait.next()
        await message.reply('Введите текст')


@dp.message_handler(state=FSMWait.waiting_for_text)
async def text_handler(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['waiting_for_text'] = message.text

    text = data['waiting_for_text']

    for i in range(len(numbers) + 1):
        pywhatkit.sendwhatmsg_instantly(phone_no=numbers[i], message=text)


executor.start_polling(dp, skip_updates=True)

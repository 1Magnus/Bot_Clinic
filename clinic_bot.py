from aiogram import Bot, Dispatcher, executor, types
from configs import TOKEN
from aiogram.dispatcher.filters import Text
from main import get_tickets
import threading

last_department = '45'
last_doctors = []
need_doctor = None
count = 0

departmentId = {'Лор': '45'}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Лор', 'Окулист', 'Надо добавить врачей']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Список врачей', reply_markup=keyboard)


@dp.message_handler(Text(equals='Лор'))
async def get_doctors(message: types.Message):
    doctors = get_tickets(departmentId.get("Лор"))
    global last_department
    last_department = departmentId.get("Лор")

    start_buttons = []
    for doctor in doctors:
        start_buttons.append(doctor.get('family'))
        await message.answer(f"{doctor.get('name')} --- {doctor.get('count_tickets')}")

    global last_doctors
    last_doctors = start_buttons

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Вот какие есть варианты: ', reply_markup=keyboard)


@dp.message_handler()
async def verify_doctor(message: types.Message):
    if message.text in last_doctors:
        ned_doctor = get_need_doctor(message.text)
        if ned_doctor.get('count_tickets') == 0:
            await message.answer('Запускаем поиск талонов...')
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Надо запустить процесс поиска билетов

    else:
        await message.answer('Что то я не понял, давай попробуем заново...')


def get_need_doctor(name_doctor):
    doctors = get_tickets(last_department)
    for doctor in doctors:
        if doctor.get('family') == name_doctor:
            return doctor


def check_ticket_doctor(doctor):
    doctor = get_need_doctor(doctor.get('family'))
    ticket = doctor.get('count_tickets')
    if ticket == 0:
        print('Билетов НЕТ!')
        return ticket






def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

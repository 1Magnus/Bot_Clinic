from aiogram import Bot, Dispatcher, executor, types
from configs import TOKEN
from aiogram.dispatcher.filters import Text
from main import get_tickets
import threading

last_department = '45'
last_doctors = []
need_doctor = None
count = 0
username = ''

departmentId = {'Лор': '45'}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

TIMER = []


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Лор', 'Окулист', 'Надо добавить врачей']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Список врачей', reply_markup=keyboard)


@dp.message_handler(commands='cancel')
async def cancel(message: types.Message = None):
    global TIMER
    for t in TIMER:
        t.cancel()
    del TIMER
    TIMER = []
    await message.answer('Поиски билетов отключены! ')


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
            global username
            username = f'{message.chat.id}'
            timer_doctor(ned_doctor)
        else:
            await message.answer(f"Талонов много, {ned_doctor.get('count_tickets')}")
    else:
        await message.answer('Что то я не понял, давай попробуем заново...')


# функции не хендлеры надо вынести в майн
def get_need_doctor(name_doctor):
    doctors = get_tickets(last_department)
    for doctor in doctors:
        if doctor.get('family') == name_doctor:
            return doctor


def check_ticket_doctor(doctor):
    doctor = get_need_doctor(doctor.get('family'))
    ticket = doctor.get('count_tickets')
    if ticket:
        inform_the_user()
        cancel()
        # print(doctor.get('count_tickets'), 'Билеты!')
    # else:
    #     print('Билетов НЕТ')
    # inform_the_user()


def timer_doctor(doctor):
    check_ticket_doctor(doctor)
    t = threading.Timer(15, timer_doctor, [doctor])
    global TIMER
    TIMER.append(t)
    t.start()


async def inform_the_user():
    # INFORM USER
    for i in range(5):
        await bot.send_message(username, 'Билеты есть!')


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

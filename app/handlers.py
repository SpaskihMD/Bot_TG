from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.sqlbase import add_database, get_photo_bynumber


import app.keyboard as kb  #клавиатура

from aiogram.fsm.context import FSMContext  #Состояния
from aiogram.fsm.state import State, StatesGroup


# Класс создания переменных состояния "записать"
class Numm(StatesGroup):
    number = State()
    photo = State()
#--------------------------------------------------------------------

#Класс состояния кнопки "Найти"
class Search(StatesGroup):
    number_id = State()
    
#--------------------------------------------------------------------

router = Router()

photoids = []

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет {message.from_user.first_name}!\nВыберите необходимую кнопку внизу.',reply_markup=kb.main)

#--------------------------------------------------------------------

#Собираем состояния из команды Запись
#Добавляем в конце данные в sql
@router.message(F.text =='Записать 📝')
async def cmd_save(message: Message, state: FSMContext):
    await state.set_state(Numm.number)
    await message.answer(f'{message.from_user.first_name} введите номер БЕЗ "Е-"⛔️')


@router.message(Numm.number)
async def cmd_number(message: Message, state: FSMContext):
    number = message.text
    await state.update_data(number=number)
    await state.set_state(Numm.photo)
    await message.answer('Пришлите фото 📸')


@router.message(Numm.photo, F.photo)
async def reg_photo(message: Message, state: FSMContext):
    photo=message.photo[-1].file_id
    await state.update_data(photo=photo)

    ###Вывод инфы собранной от пользователя
    data = await state.get_data()
    '''
    #Вывод собранной информации из FSM
    await message.answer_photo(photo=data['photo'],
                               caption=f'Е-{data['number']}')
    '''
    #передаем данные в sql
    number = data.get('number')
    await add_database(number,photo)

    #вывод строки о готовности
    await state.clear()
    await message.answer('Готово👍\nНажмите 👉 /start для возврата назад')
#--------------------------------------------------------------------

#Поиск по базе
@router.message(F.text == 'Найти 🔍')
async def cmd_poisk(message:Message, state: FSMContext):
    await state.set_state(Search.number_id)
    await message.answer(f'{message.from_user.first_name} введите номер БЕЗ "Е-"⛔️')
    

@router.message(Search.number_id)
async def fsm_num_id(message:Message, state: FSMContext):
    number_id = message.text
    await state.update_data(number_id=number_id)
    data = await state.get_data()
    
    number_id = data.get('number_id')
    
    
    photo = await get_photo_bynumber(number_id)
    
    
    for i in photo:
        await message.answer_photo(photo=i[0])
        
        
    #вывод того что получил в найти
    #await message.answer(number_id)
    await state.clear()

    await message.answer('Нажмите 👉 /start для возврата в начало')








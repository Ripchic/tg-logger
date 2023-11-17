from aiogram import types
from aiogram import Router, F
# from keyboards import client_kb
# from data_base import sqlite_db
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.dispatcher import Text


router = Router()


class FSMuser(StatesGroup):
    user_tg = State()
    user_sm = State()
    subs = State()
    Anilib = State()
    Anivost = State()


@router.message(F.text == "/start")
async def start_command(message: types.Message):
    await message.answer("Привет! Я <b>Anime Notifications Bot</b> - бот, что мило напомнит тебе о том, что вышла "
                         "серия твоего любимого аниме. <i>И даже больше</i> - напомню, что вышла твоя любимая озвучка!"
                         "\n\nКак я работаю? Очень легко! Мне нужен всего лишь ссылка на твой 'Шикимори'. Как только "
                         "ты его сбросишь, ты сможешь выбрать те уведомления, что ты хочешь получать!\n\nНа данный "
                         "момент ты можешь получать уведомления о выходе серии (с субтитрами), уведомления о выходе "
                         "озвучки от трёх студий: Анилибрия, Анимевост", parse_mode='HTML')
    await message.answer("Для того чтобы начать пользоваться ботом отправь команду... Ничего не пиши, я теперь тг бот!!!")


# @router.message(F.text == "/link")
# async def link_update(message: types.Message, state: FSMContext):
#     await state.update_data(user_tg=message.from_user.id)
#     await message.answer("Твоя ссылка на Шикимори:")
#     await state.set_state(FSMuser.user_sm)


# @router.message(F.text == "/cansel", state="*")
# async def cansel_function(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('OK')


# @router.message(FSMuser.user_sm)
# async def subs_new(message: types.Message, state: FSMContext):
#     # Проверка на то, является ли это ссылкой
#     await state.update_data(user_sm=message.text)
#     await message.answer("Нужны ли тебе уведомления об выходе новых серий с субтитрами?",
#                          reply_markup=client_kb.YesNo_kb)
#     await state.set_state(FSMuser.subs)


# @router.message(FSMuser.subs)
# async def al_new(message: types.Message, state: FSMContext):
#     if message.text == "Да":
#         await message.reply("Успешно добавлены!")
#         status = 1
#     else:
#         status = 0
#         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
#     await state.update_data(subs=status)
#     await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анилибрии",
#                          reply_markup=client_kb.YesNo_kb)
#     await state.set_state(FSMuser.Anilib)

    # async with state.proxy() as data:
    #     if message.text == "Да":
    #         await message.reply("Успешно добавлены!")
    #         status = 1
    #     else:
    #         status = 0
    #         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
    #     data['subs'] = status
    # await FSMuser.next()
    # await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анилибрии?", reply_markup=client_kb.YesNo_kb)


# @router.message(FSMuser.Anilib)
# async def av_new(message: types.Message, state: FSMContext):
#     if message.text == "Да":
#         await message.reply("Успешно добавлены!")
#         status = 1
#     else:
#         status = 0
#         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
#     await state.update_data(Anilib=status)
#     await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анивоста?",
#                          reply_markup=client_kb.YesNo_kb)
#     await state.set_state(FSMuser.Anivost)

    # async with state.proxy() as data:
    #     if message.text == "Да":
    #         await message.reply("Успешно добавлены!")
    #         status = 1
    #     else:
    #         status = 0
    #         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
    #     data['Anilib'] = status
    # await FSMuser.next()
    # await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анивоста?", reply_markup=client_kb.YesNo_kb)


# @router.message(FSMuser.Anivost)
# async def link_update_finish(message: types.Message, state: FSMContext):
#     if message.text == "Да":
#         await message.reply("Успешно добавлены!")
#         status = 1
#     else:
#         status = 0
#         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
#     await state.update_data(Anivost=status)
#     await state.set_state(FSMuser.Anivost)
#     user_data = await state.get_data()
#     print(user_data)
#     await state.clear()

    # async with state.proxy() as data:
    #     if message.text == "Да":
    #         await message.reply("Успешно добавлены!")
    #         status = 1
    #     else:
    #         status = 0
    #         await message.reply("Хорошо, эти уведомления тебе приходить не будут!")
    #     data['Anivost'] = status
    # async with state.proxy() as data:
    #     await message.reply(str(data))


    # if await sqlite_db.sql_check_user(state):
    #     await sqlite_db.sql_update_command(state)
    #     await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анивоста?",
    #                          reply_markup=client_kb.YesNo_kb)
    # else:
    #     await sqlite_db.sql_add_command(state)
    #     await message.answer("Нужны ли тебе уведомления об выходе озвучки от Анивоста?",
    #                          reply_markup=client_kb.YesNo_kb)
    # await state.finish()


# Функция для статуса и изменения уведомлений
# async def notifications_change(message: types.Message):
#     sub = "Да" if await sqlite_db.sql_check_sub(message.from_user.id) else "Нет"
#     al = "Да" if await sqlite_db.sql_check_al(message.from_user.id) else "Нет"
#     av = "Да" if await sqlite_db.sql_check_av(message.from_user.id) else "Нет"
#     await message.answer("Нажав на кнопку, ты можешь изменить уведомления, на которые ты подписан!\n\nНа данный "
#                          f"момент ты подписан на:\nСубтитры: {sub}\nАнилибрия: {al}\nАнивост: {av}",
#                          reply_markup=client_kb.notif_kb)


# async def subs_call(callback: types.CallbackQuery):
#     await sqlite_db.sql_update_subs(callback.from_user.id)
#     sub = "Да" if await sqlite_db.sql_check_sub(callback.message.from_user.id) else "Нет"
#     al = "Да" if await sqlite_db.sql_check_al(callback.message.from_user.id) else "Нет"
#     av = "Да" if await sqlite_db.sql_check_av(callback.message.from_user.id) else "Нет"
#     await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Нажав"
#                                 " на кнопку, ты можешь изменить уведомления, на которые ты подписан!\n\nНа данный "
#                                 f"момент ты подписан на:\nСубтитры: {sub}\nАнилибрия: {al}\nАнивост: {av}",
#                                 reply_markup=client_kb.notif_kb)
#     await callback.answer("Изменения прошли успешно!")


# async def al_call(callback: types.CallbackQuery):
#     await sqlite_db.sql_update_al(callback.from_user.id)
#     sub = "Да" if await sqlite_db.sql_check_sub(callback.message.from_user.id) else "Нет"
#     al = "Да" if await sqlite_db.sql_check_al(callback.message.from_user.id) else "Нет"
#     av = "Да" if await sqlite_db.sql_check_av(callback.message.from_user.id) else "Нет"
#     await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Нажав"
#                                 " на кнопку, ты можешь изменить уведомления, на которые ты подписан!\n\nНа данный "
#                                 f"момент ты подписан на:\nСубтитры: {sub}\nАнилибрия: {al}\nАнивост: {av}",
#                                 reply_markup=client_kb.notif_kb)
#     await callback.answer("Изменения прошли успешно!")


# async def av_call(callback: types.CallbackQuery):
#     await sqlite_db.sql_update_av(callback.from_user.id)
#     sub = "Да" if sqlite_db.sql_check_sub(callback.message.from_user.id) else "Нет"
#     al = "Да" if sqlite_db.sql_check_al(callback.message.from_user.id) else "Нет"
#     av = "Да" if sqlite_db.sql_check_av(callback.message.from_user.id) else "Нет"
#     await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Нажав"
#                                 " на кнопку, ты можешь изменить уведомления, на которые ты подписан!\n\nНа данный "
#                                 f"момент ты подписан на:\nСубтитры: {sub}\nАнилибрия: {al}\nАнивост: {av}",
#                                 reply_markup=client_kb.notif_kb)
#     await callback.answer("Изменения прошли успешно!")


# Функция для "Поддержать нас"


# Функция для удаления старой инфы при замене ссылки/ухода пользователя


# def register_handlers_client(dp):
#     dp.register_message(link_update, commands='link', state=None)
#     dp.register_message_handler(cansel_function, state="*", commands='cansel')
#     # dp.register_message_handler(cansel_function, Text(equals="отмена", ignore_case=True), state="*")
#     dp.register_message_handler(subs_new, state=FSMuser.user_sm)
#     dp.register_message_handler(al_new, state=FSMuser.subs)
#     dp.register_message_handler(av_new, state=FSMuser.Anilib)
#     dp.register_message_handler(link_update_finish, state=FSMuser.Anivost)
#
#     dp.register_message_handler(start_command, commands=['start'])
#     # dp.register_message_handler(notifications_change, Text(equals="уведомления", ignore_case=True))
#     dp.register_message_handler(notifications_change, commands='notification')
#     dp.register_callback_query_handler(subs_call, text="1")
#     dp.register_callback_query_handler(al_call, text="2")
#     dp.register_callback_query_handler(av_call, text="3")
    # dp.register_message_handler(link_update, commands=['link'])
    # dp.register_message_handler(course_command, commands=['fuck'])
    # dp.register_message_handler(course_table, commands=['Курс', 'course'])
    # dp.register_message_handler(echo_send)

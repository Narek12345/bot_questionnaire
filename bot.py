from aiogram import Bot, Dispatcher
from aiogram import types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from fsm import FSMClient, FSMDateReceiptSalaryCard
from keyboards import is_there_gazprombank_salary_card_keyboard, is_card_issued_or_not_keyboard

from db import User

import os

TOKEN = os.getenv("TOKEN")

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start', state=None)
async def start_cmd(message: types.Message):
	await FSMClient.initials.set()
	await message.answer("Введите пожалуйста ФИО:")


@dp.message_handler(state=FSMClient.initials)
async def get_initials(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['initials'] = message.text
	await FSMClient.next()
	await message.answer("Введите пожалуйста город проживания:")


@dp.message_handler(state=FSMClient.city)
async def get_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['city'] = message.text
	await FSMClient.next()
	await message.answer("Введите пожалуйста дату рождения в формате 01.01.2000:")


@dp.message_handler(state=FSMClient.date_of_birth)
async def get_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['date_of_birth'] = message.text
	await FSMClient.next()
	await message.answer("Введите пожалуйста номер телефона:")


@dp.message_handler(state=FSMClient.phone)
async def get_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['phone'] = message.text
	await FSMClient.next()
	await message.answer("Сколько дней вы планируете работать в неделю ?")


@dp.message_handler(state=FSMClient.amount_of_days)
async def get_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['amount_of_days'] = message.text
	await FSMClient.next()
	await message.answer("Сколько часов в день планируете работать ?")


@dp.message_handler(state=FSMClient.amount_of_hours)
async def get_city(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['username'] = message.from_user.username
		data['amount_of_hours'] = message.text

		# Добавляем в БД.
		User.add_new_user(data['initials'], data['city'], data['date_of_birth'], data['phone'], data['username'], data['amount_of_days'], data['amount_of_hours'])

	await state.finish()
	await message.answer("Есть ли зарплатная карта газпромбанка ?", reply_markup=is_there_gazprombank_salary_card_keyboard)


@dp.callback_query_handler(text="yes")
async def card_available_call(callback: types.CallbackQuery):
	await callback.message.answer('Спасибо за заявку.\nНаши операторы с вами свяжутся в ближайшее время и отправят инструкцию')
	await callback.answer()


@dp.callback_query_handler(text="no")
async def card_no_available_call(callback: types.CallbackQuery):
	await callback.message.answer('Для продолжения заполнения анкеты необходимо заполнить заявку на получение дебетовой зарплатной карты Газпромбанка https://pxl.leads.su/click/7675c82949efc3989444247ec7c5f1bd?erid=LjN8K8NZ8', reply_markup=is_card_issued_or_not_keyboard)
	await callback.answer()


@dp.callback_query_handler(text="apply_for_card", state=None)
async def apply_for_card_call(callback: types.CallbackQuery):
	await FSMDateReceiptSalaryCard.date.set()
	await callback.message.answer('Укажите дату получения зарплатной карты в формате 01.01.2000:')
	await callback.answer()


@dp.message_handler(state=FSMDateReceiptSalaryCard.date)
async def get_initials(message: types.Message, state: FSMContext):
	date_card = message.text
	await state.finish()
	await message.answer("Спасибо за заявку. Высылаю вам информацию о вакансии и обучающие материалы.\nСсылка на Гугл диск: https://drive.google.com/drive/folders/1fk-CEwvb3ghcXaNtYcdgLNac-2oZvcVF?usp=sharing\nНаш оператор с вами свяжется в ближайшее время.")


@dp.callback_query_handler(text="refuse_to_issue_card")
async def refuse_to_issue_card_call(callback: types.CallbackQuery):
	await callback.message.answer('Спасибо за проявленный интерес к нашей вакансии. До свидания.')
	await callback.answer()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

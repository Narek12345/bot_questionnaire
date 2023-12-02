from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
	initials = State()
	city = State()
	date_of_birth = State()
	phone = State()
	amount_of_days = State()
	amount_of_hours = State()


class FSMDateReceiptSalaryCard(StatesGroup):
	date = State()
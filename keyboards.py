from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yes_button = InlineKeyboardButton('Да', callback_data="yes")
no_button = InlineKeyboardButton('Нет', callback_data="no")

is_there_gazprombank_salary_card_keyboard = InlineKeyboardMarkup().add(yes_button).add(no_button)



apply_for_card_button = InlineKeyboardButton('Оформить карту', callback_data="apply_for_card")
refuse_to_issue_card_button = InlineKeyboardButton('Отказаться от оформлении', callback_data="refuse_to_issue_card")

is_card_issued_or_not_keyboard = InlineKeyboardMarkup().add(apply_for_card_button).add(refuse_to_issue_card_button)

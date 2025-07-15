from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def create_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("🇷🇺 RU", callback_data="lang_ru")],
        [InlineKeyboardButton("🇺🇸 EN", callback_data="lang_en")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_main_menu_keyboard(lang='ru', is_admin=False, is_employee=False):
    if lang == 'ru':
        buttons = [
            ["🔥 VIP Криптоклуб"],
            ["📢 Подписаться на канал"]
        ]
        if is_admin:
            buttons.append(["👥 Управление сотрудниками"])
        if is_employee:
            buttons.append(["🔗 Моя реферальная ссылка"])
    else:
        buttons = [
            ["🔥 VIP Crypto Club"],
            ["📢 Subscribe to Channel"]
        ]
        if is_admin:
            buttons.append(["👥 Employee Management"])
        if is_employee:
            buttons.append(["🔗 My Referral Link"])
    
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def create_experience_keyboard(lang='ru'):
    if lang == 'ru':
        buttons = [
            ["Новичок"],
            ["Опытный"],
            ["Профессионал"],
            ["🏠 Главное меню"]
        ]
    else:
        buttons = [
            ["Beginner"],
            ["Experienced"],
            ["Professional"],
            ["🏠 Main Menu"]
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def create_amount_keyboard(lang='ru'):
    if lang == 'ru':
        buttons = [
            ["$100-500"],
            ["$500-1000"],
            ["$1000+"],
            ["🏠 Главное меню"]
        ]
    else:
        buttons = [
            ["$100-500"],
            ["$500-1000"],
            ["$1000+"],
            ["🏠 Main Menu"]
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def create_vip_plans_keyboard(lang='ru'):
    if lang == 'ru':
        keyboard = [
            [InlineKeyboardButton("📅 1 месяц - $300", callback_data="vip_1month")],
            [InlineKeyboardButton("📅 6 месяцев - $600", callback_data="vip_6months")],
            [InlineKeyboardButton("♾️ Навсегда - $900", callback_data="vip_lifetime")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📅 1 Month - $300", callback_data="vip_1month")],
            [InlineKeyboardButton("📅 6 Months - $600", callback_data="vip_6months")],
            [InlineKeyboardButton("♾️ Lifetime - $900", callback_data="vip_lifetime")]
        ]
    return InlineKeyboardMarkup(keyboard)

def create_employee_keyboard(lang='ru'):
    if lang == 'ru':
        buttons = [
            ["➕ Добавить сотрудника"],
            ["📊 Просмотр рефералов"],
            ["📈 Статистика сотрудников"],
            ["📋 Список сотрудников"],
            ["🗑️ Удалить сотрудника"],
            ["🏠 Главное меню"]
        ]
    else:
        buttons = [
            ["➕ Add Employee"],
            ["📊 View Referrals"],
            ["📈 Employee Statistics"],
            ["📋 Employee List"],
            ["🗑️ Delete Employee"],
            ["🏠 Main Menu"]
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def create_employee_menu_keyboard(lang='ru'):
    if lang == 'ru':
        buttons = [
            ["🔗 Моя реферальная ссылка"]
        ]
    else:
        buttons = [
            ["🔗 My Referral Link"]
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
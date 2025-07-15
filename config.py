import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv('ADMIN_ID', '123456789').split(';') if admin_id.strip()]

# Для обратной совместимости
ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 123456789

# Функция проверки админа
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Состояния диалогов
LANGUAGE_SELECT = 0
MAIN_MENU = 1
TRADING_EXPERIENCE = 2
TRADING_AMOUNT = 3
TRADING_SCREENSHOT = 4
VIP_CLUB_PAYMENT = 5
VIP_PLAN_SELECT = 6
CHANNEL_JOIN = 7
ADD_EMPLOYEE = 8
EMPLOYEE_MENU = 9
DELETE_EMPLOYEE = 10
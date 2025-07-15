import logging
import uuid
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, ContextTypes, filters
)

from config import *
from keyboards import *
from database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db = Database()

# Стартовая функция
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обработка рефералов
    if context.args:
        await handle_referral(update, context)
    
    await update.message.reply_text(
        "🚀 Welcome to CRYPTOCRIP CLUB! / Добро пожаловать в CRYPTOCRIP CLUB!\n\n"
        "Please select your language / Выберите язык:",
        reply_markup=create_language_keyboard()
    )
    return LANGUAGE_SELECT

# Выбор языка
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    lang = 'ru' if query.data == 'lang_ru' else 'en'
    context.user_data['language'] = lang
    
    user_is_admin = is_admin(update.effective_user.id)
    employees = db.get_employees()
    user_is_employee = str(update.effective_user.id) in employees
    
    if lang == 'ru':
        text = "🚀 Добро пожаловать в CRYPTOCRIP CLUB!\n\nВыберите интересующий вас раздел:"
    else:
        text = "🚀 Welcome to CRYPTOCRIP CLUB!\n\nSelect the section you're interested in:"
    
    await query.edit_message_text(text)
    await query.message.reply_text(
        "Главное меню:" if lang == 'ru' else "Main menu:",
        reply_markup=create_main_menu_keyboard(lang, user_is_admin, user_is_employee)
    )
    return MAIN_MENU

# Обработчик текстовых сообщений главного меню
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        user_is_admin = is_admin(update.effective_user.id)
        employees = db.get_employees()
        user_is_employee = str(update.effective_user.id) in employees
        if lang == 'ru':
            await update.message.reply_text(
                "Главное меню:",
                reply_markup=create_main_menu_keyboard(lang, user_is_admin, user_is_employee)
            )
        else:
            await update.message.reply_text(
                "Main menu:",
                reply_markup=create_main_menu_keyboard(lang, user_is_admin, user_is_employee)
            )
        return MAIN_MENU
    
    elif text in ["🔗 Моя реферальная ссылка", "🔗 My Referral Link"]:
        employees = db.get_employees()
        user_id = str(update.effective_user.id)
        
        if user_id in employees:
            referral_link = employees[user_id].get('referral_link', '')
            if lang == 'ru':
                await update.message.reply_text(
                    f"🔗 Ваша реферальная ссылка:\n\n{referral_link}\n\nДелитесь ей с клиентами!"
                )
            else:
                await update.message.reply_text(
                    f"🔗 Your referral link:\n\n{referral_link}\n\nShare it with clients!"
                )
        else:
            if lang == 'ru':
                await update.message.reply_text("Вы не являетесь сотрудником.")
            else:
                await update.message.reply_text("You are not an employee.")
        return MAIN_MENU
    
    if text in ["🔥 VIP Криптоклуб", "🔥 VIP Crypto Club"]:
        if lang == 'ru':
            await update.message.reply_text(
                "🔒 НАБОР В ЗАКРЫТОЕ СООБЩЕСТВО\n\n"
                "<a href='https://t.me/thecryptocrip/9324'>VIP канал</a> чем он отличается от обычного?\n\n"
                "🔹В нем я делюсь оперативной информацией о своих сделках, составом портфеля, мыслями, мнением о рынке.\n\n"
                "🔹Скидываю точные сигналы на фьючерсах. Контролирую ваш риск-менеджмент, рассказываю о психологии трейдинга.\n\n"
                "✅ Ежедневно до 7 сигналов с точностью до 80-90%.\n"
                "✅ Зоны входа / Тейк-профиты / Стоп-лоссы.\n\n"
                "🔹Сигналы на споте: с точками входа, выхода, стопом и объяснениями. Пишу монеты с потенциалом Х10 и выше.\n\n"
                "🔹Сигналы на покупку новых ТОП-проектов, которые выходят на биржу, и через пару часов происходит их ПАМП.\n\n"
                "🔹Ссылки на платные полезные ресурсы + индикаторы, которые для вас будут БЕСПЛАТНЫ.\n\n"
                "🔹АВТОРСКИЙ УЧЕБНИК из 8 частей + 15 обучающих АВТОРСКИХ ВИДЕОУРОКОВ «ВСЁ, ЧТО Я ЗНАЮ» — $600, для участников VIP клуба БЕСПЛАТНО.\n\n"
                "🔹Обучающая литература — 25 платных книг, которые вы получите БЕСПЛАТНО.\n\n"
                "🔹Smart Money. Понимание действий крупных участников рынка — фондов и китов. Мгновенное определение зон ликвидности.\n\n"
                "🔹Проводим ончейн-анализ, отслеживаем поведение крупного капитала. Входим в позиции на ранних этапах, опережаем розничный спрос, «падаем на хвост» смарт-деньгам и забираем иксы вместе с ними. Заходим в актив до массового внимания. Ончейн говорит раньше, чем графики. Смарт-деньги зашли — мы следом. До хайпа. До шума.\n\n"
                "🔹Помощь в корректировке вашего портфеля.\n\n"
                "🔹Support, который ответит на все ваши вопросы.\n\n"
                "🔹Инструкция для новичков.\n\n"
                "🔹Правила входа в сделку.\n\n"
                "Сигналы вы получите раньше всех! Кто заходит в сделку раньше массы людей, зарабатывает всегда больше!\n\n"
                "❗️Вся информация доступна только участникам VIP-клуба после оплаты подписки.\n\n"
                "🤝 Ваши отзывы — <a href='https://t.me/cryptocrip_feedback'>ТУТ</a>\n\n"
                "Выберите план подписки:",
                reply_markup=create_vip_plans_keyboard(lang),
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                "🔒 RECRUITMENT TO CLOSED COMMUNITY\n\n"
                "<a href='https://t.me/thecryptocrip/9324'>VIP channel</a> how is it different from the regular one?\n\n"
                "🔹I share operational information about my trades, portfolio composition, thoughts, market opinion.\n\n"
                "🔹I post accurate futures signals. I control your risk management, talk about trading psychology.\n\n"
                "✅ Up to 7 signals daily with 80-90% accuracy.\n"
                "✅ Entry zones / Take-profits / Stop-losses.\n\n"
                "🔹Spot signals: with entry, exit points, stop and explanations. I write coins with X10+ potential.\n\n"
                "🔹Signals for buying new TOP projects that are listed on exchanges, and their PUMP happens in a couple of hours.\n\n"
                "🔹Links to paid useful resources + indicators that will be FREE for you.\n\n"
                "🔹AUTHOR'S TEXTBOOK of 8 parts + 15 educational AUTHOR'S VIDEO LESSONS 'EVERYTHING I KNOW' — $600, FREE for VIP club members.\n\n"
                "🔹Educational literature — 25 paid books that you will get for FREE.\n\n"
                "🔹Smart Money. Understanding the actions of large market participants — funds and whales. Instant identification of liquidity zones.\n\n"
                "🔹We conduct on-chain analysis, track large capital behavior. We enter positions at early stages, outpace retail demand, 'ride the tail' of smart money and take profits with them. We enter assets before mass attention. On-chain speaks earlier than charts. Smart money entered — we follow. Before hype. Before noise.\n\n"
                "🔹Help in adjusting your portfolio.\n\n"
                "🔹Support that will answer all your questions.\n\n"
                "🔹Instructions for beginners.\n\n"
                "🔹Rules for entering trades.\n\n"
                "You will get signals before everyone else! Those who enter trades before the masses always earn more!\n\n"
                "❗️All information is available only to VIP club members after subscription payment.\n\n"
                "🤝 Your reviews — <a href='https://t.me/cryptocrip_feedback'>HERE</a>\n\n"
                "Choose subscription plan:",
                reply_markup=create_vip_plans_keyboard(lang),
                parse_mode='HTML'
            )
        return VIP_PLAN_SELECT
    
    elif text in ["📢 Подписаться на канал", "📢 Subscribe to Channel"]:
        if lang == 'ru':
            await update.message.reply_text(
                "Чтобы быть в курсе актуальных новостей и получать сигналы,\n"
                "подпишитесь на наш Telegram-канал:\n\n"
                "🔗 https://t.me/thecryptocrip\n\n"
                "После подписки возвращайтесь в меню."
            )
        else:
            await update.message.reply_text(
                "To stay updated with the latest news and receive signals,\n"
                "subscribe to our Telegram channel:\n\n"
                "🔗 https://t.me/thecryptocrip\n\n"
                "After subscribing, return to the menu."
            )
        return MAIN_MENU
    
    elif text in ["👥 Управление сотрудниками", "👥 Employee Management"]:
        if update.effective_user.id == ADMIN_ID:
            if lang == 'ru':
                await update.message.reply_text(
                    "👥 Управление сотрудниками\n\n"
                    "Выберите действие:",
                    reply_markup=create_employee_keyboard(lang)
                )
            else:
                await update.message.reply_text(
                    "👥 Employee Management\n\n"
                    "Select action:",
                    reply_markup=create_employee_keyboard(lang)
                )
            return EMPLOYEE_MENU
        else:
            if lang == 'ru':
                await update.message.reply_text("У вас нет доступа к этой функции")
            else:
                await update.message.reply_text("You don't have access to this function")
            return MAIN_MENU

# Обработчики индивидуальной торговли
async def experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        is_admin = update.effective_user.id == ADMIN_ID
        await update.message.reply_text(
            "Главное меню:" if lang == 'ru' else "Main menu:",
            reply_markup=create_main_menu_keyboard(lang, is_admin)
        )
        return MAIN_MENU
    
    context.user_data['experience'] = text
    
    if lang == 'ru':
        await update.message.reply_text(
            f"Вы выбрали уровень опыта: {text}\n\n"
            "С какой суммой готовы начать?",
            reply_markup=create_amount_keyboard(lang)
        )
    else:
        await update.message.reply_text(
            f"You selected experience level: {text}\n\n"
            "What amount are you ready to start with?",
            reply_markup=create_amount_keyboard(lang)
        )
    return TRADING_AMOUNT

async def amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        is_admin = update.effective_user.id == ADMIN_ID
        await update.message.reply_text(
            "Главное меню:" if lang == 'ru' else "Main menu:",
            reply_markup=create_main_menu_keyboard(lang, is_admin)
        )
        return MAIN_MENU
    
    context.user_data['amount'] = text
    
    if lang == 'ru':
        await update.message.reply_text(
            f"Вы выбрали сумму: {text}\n\n"
            "Прикрепите скриншот из биржи с подтверждением депозита",
            reply_markup=ReplyKeyboardMarkup([["🏠 Главное меню"]], resize_keyboard=True)
        )
    else:
        await update.message.reply_text(
            f"You selected amount: {text}\n\n"
            "Attach a screenshot from the exchange confirming the deposit",
            reply_markup=ReplyKeyboardMarkup([["🏠 Main Menu"]], resize_keyboard=True)
        )
    return TRADING_SCREENSHOT

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('language', 'ru')
    
    try:
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            context.user_data['screenshot'] = photo_file.file_id
            
            # Отправка уведомления администратору
            referrer_info = ""
            if context.user_data.get('referrer_employee_name'):
                referrer_info = f"\n• От сотрудника: {context.user_data.get('referrer_employee_name')}"
            
            admin_message = (
                "📥 Новая заявка на индивидуальную торговлю\n"
                f"• Опыт: {context.user_data.get('experience')}\n"
                f"• Сумма: {context.user_data.get('amount')}\n"
                f"• От: @{update.effective_user.username or 'Без username'}"
                f"{referrer_info}"
            )
            for admin_id in ADMIN_IDS:
                await context.bot.send_photo(
                    chat_id=admin_id, 
                    photo=photo_file.file_id,
                    caption=admin_message
                )
            
            # Уведомление сотруднику
            if context.user_data.get('referrer_employee_id'):
                try:
                    employee_message = (
                        "🎉 Новая заявка от вашего реферала!\n"
                        f"Клиент: @{update.effective_user.username or 'Без username'}\n"
                        f"Опыт: {context.user_data.get('experience')}\n"
                        f"Сумма: {context.user_data.get('amount')}"
                    )
                    await context.bot.send_message(
                        chat_id=int(context.user_data['referrer_employee_id']),
                        text=employee_message
                    )
                except Exception as e:
                    logger.error(f"Не удалось уведомить сотрудника: {e}")
            
            if lang == 'ru':
                await update.message.reply_text(
                    "Спасибо, ваша заявка отправлена.\n"
                    "Ожидайте ответа в ближайшее время.",
                    reply_markup=create_main_menu_keyboard(lang, update.effective_user.id == ADMIN_ID)
                )
            else:
                await update.message.reply_text(
                    "Thank you, your application has been sent.\n"
                    "Expect a response soon.",
                    reply_markup=create_main_menu_keyboard(lang, update.effective_user.id == ADMIN_ID)
                )
            return MAIN_MENU
    except Exception as e:
        logger.error(f"Ошибка при обработке скриншота: {e}")
        if lang == 'ru':
            await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")
        else:
            await update.message.reply_text("An error occurred. Please try again.")
        return TRADING_SCREENSHOT

# Обработчик для состояния загрузки скриншота с кнопкой "Главное меню"
async def screenshot_with_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        is_admin = update.effective_user.id == ADMIN_ID
        await update.message.reply_text(
            "Главное меню:" if lang == 'ru' else "Main menu:",
            reply_markup=create_main_menu_keyboard(lang, is_admin)
        )
        return MAIN_MENU
    
    # Если не кнопка меню, обрабатываем как обычный скриншот
    return await screenshot_handler(update, context)

# VIP Club обработчики
async def vip_plan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('language', 'ru')
    
    plan_prices = {
        "vip_1month": "$300",
        "vip_6months": "$600", 
        "vip_lifetime": "$900"
    }
    
    context.user_data['vip_plan'] = query.data
    price = plan_prices[query.data]
    
    if lang == 'ru':
        await query.message.reply_text(
            f"💳 Оплата VIP Криптоклуба\n\n"
            f"Выбранный план: {price}\n\n"
            f"Переведите {price} на кошелек (USDT TRX Tron TRC20):\n\n"
            "`THTV14nt81nZewSMG53eLn58fveyEs6dR1`\n\n"
            "После оплаты пришлите скриншот чека.",
            reply_markup=ReplyKeyboardMarkup([["🏠 Главное меню"]], resize_keyboard=True),
            parse_mode='Markdown'
        )
    else:
        await query.message.reply_text(
            f"💳 VIP Crypto Club Payment\n\n"
            f"Selected plan: {price}\n\n"
            f"Transfer {price} to wallet (USDT TRX Tron TRC20):\n\n"
            "`THTV14nt81nZewSMG53eLn58fveyEs6dR1`\n\n"
            "After payment, send a screenshot of the receipt.",
            reply_markup=ReplyKeyboardMarkup([["🏠 Main Menu"]], resize_keyboard=True),
            parse_mode='Markdown'
        )
    return VIP_CLUB_PAYMENT

# Обработчик для VIP платежей с кнопкой "Главное меню"
async def vip_payment_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        is_admin = update.effective_user.id == ADMIN_ID
        await update.message.reply_text(
            "Главное меню:" if lang == 'ru' else "Main menu:",
            reply_markup=create_main_menu_keyboard(lang, is_admin)
        )
        return MAIN_MENU
    
    # Если не кнопка меню, просим прикрепить скриншот
    if lang == 'ru':
        await update.message.reply_text("Пожалуйста, прикрепите скриншот чека.")
    else:
        await update.message.reply_text("Please attach a screenshot of the receipt.")
    return VIP_CLUB_PAYMENT

async def vip_screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('language', 'ru')
    
    try:
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            
            plan_names = {
                "vip_1month": "1 месяц / 1 Month",
                "vip_6months": "6 месяцев / 6 Months",
                "vip_lifetime": "Навсегда / Lifetime"
            }
            
            plan = context.user_data.get('vip_plan', 'vip_1month')
            
            if context.user_data.get('referrer_employee_name'):
                referrer_info = f"\nРаботник приведший клиента: {context.user_data.get('referrer_employee_name')}"
            else:
                referrer_info = "\nРаботник приведший клиента: отсутствует"
            
            admin_message = (
                "📥 Новая оплата VIP Криптоклуба!\n"
                f"План: {plan_names.get(plan, 'Unknown')}\n"
                f"Клиент: @{update.effective_user.username or 'Без username'}\n"
                f"ID клиента: {update.effective_user.id}"
                f"{referrer_info}"
            )
            
            for admin_id in ADMIN_IDS:
                await context.bot.send_photo(
                    chat_id=admin_id,
                    photo=photo_file.file_id,
                    caption=admin_message
                )
            
            # Уведомление сотруднику
            if context.user_data.get('referrer_employee_id'):
                try:
                    employee_message = (
                        "🎉 Новая оплата VIP от вашего реферала!\n"
                        f"Клиент: @{update.effective_user.username or 'Без username'}\n"
                        f"План: {plan_names.get(plan, 'Unknown')}"
                    )
                    await context.bot.send_message(
                        chat_id=int(context.user_data['referrer_employee_id']),
                        text=employee_message
                    )
                except Exception as e:
                    logger.error(f"Не удалось уведомить сотрудника: {e}")
            
            if lang == 'ru':
                await update.message.reply_text(
                    "Спасибо! Мы проверим платёж и откроем доступ.\n"
                    "Ожидайте подтверждения.",
                    reply_markup=create_main_menu_keyboard(lang, update.effective_user.id == ADMIN_ID)
                )
            else:
                await update.message.reply_text(
                    "Thank you! We will verify the payment and open access.\n"
                    "Await confirmation.",
                    reply_markup=create_main_menu_keyboard(lang, update.effective_user.id == ADMIN_ID)
                )
            return MAIN_MENU
    except Exception as e:
        logger.error(f"Ошибка при обработке оплаты VIP: {e}")
        if lang == 'ru':
            await update.message.reply_text("Произошла ошибка. Попробуйте еще раз.")
        else:
            await update.message.reply_text("An error occurred. Please try again.")
        return VIP_CLUB_PAYMENT

# Система управления сотрудниками
async def employee_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'ru')
    
    # Обработка кнопки "Главное меню"
    if text in ["🏠 Главное меню", "🏠 Main Menu"]:
        is_admin = update.effective_user.id == ADMIN_ID
        await update.message.reply_text(
            "Главное меню:" if lang == 'ru' else "Main menu:",
            reply_markup=create_main_menu_keyboard(lang, is_admin)
        )
        return MAIN_MENU
    
    if text in ["➕ Добавить сотрудника", "➕ Add Employee"]:
        if lang == 'ru':
            await update.message.reply_text(
                "Введите имя и Telegram ID нового сотрудника (через запятую):",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                "Enter the name and Telegram ID of the new employee (separated by comma):",
                reply_markup=ReplyKeyboardRemove()
            )
        return ADD_EMPLOYEE
    
    elif text in ["📊 Просмотр рефералов", "📊 View Referrals"]:
        referrals = db.get_referrals()
        employees = db.get_employees()
        
        if lang == 'ru':
            referrals_text = "Рефералы по сотрудникам:\n\n"
        else:
            referrals_text = "Referrals by employees:\n\n"
            
        for employee_id, client_list in referrals.items():
            employee_name = employees.get(employee_id, {}).get('name', 'Неизвестный' if lang == 'ru' else 'Unknown')
            referrals_text += f"{employee_name}: {len(client_list)} рефералов\n"
        
        if not referrals:
            referrals_text += "Рефералов пока нет." if lang == 'ru' else "No referrals yet."
            
        await update.message.reply_text(referrals_text)
        return EMPLOYEE_MENU
    
    elif text in ["📈 Статистика сотрудников", "📈 Employee Statistics"]:
        employees = db.get_employees()
        referrals = db.get_referrals()
        
        if lang == 'ru':
            stats_text = "📈 Статистика сотрудников:\n\n"
        else:
            stats_text = "📈 Employee Statistics:\n\n"
        
        if not employees:
            stats_text += "Сотрудников пока нет." if lang == 'ru' else "No employees yet."
        else:
            for employee_id, employee_data in employees.items():
                name = employee_data.get('name', 'Неизвестный' if lang == 'ru' else 'Unknown')
                referral_count = len(referrals.get(employee_id, []))
                stats_text += f"👤 {name}\n"
                stats_text += f"   ID: {employee_id}\n"
                stats_text += f"   Рефералов: {referral_count}\n\n" if lang == 'ru' else f"   Referrals: {referral_count}\n\n"
        
        await update.message.reply_text(stats_text)
        return EMPLOYEE_MENU
    
    elif text in ["📋 Список сотрудников", "📋 Employee List"]:
        employees = db.get_employees()
        
        if lang == 'ru':
            list_text = "📋 Список сотрудников:\n\n"
        else:
            list_text = "📋 Employee List:\n\n"
        
        if not employees:
            list_text += "Сотрудников пока нет." if lang == 'ru' else "No employees yet."
        else:
            for employee_id, employee_data in employees.items():
                name = employee_data.get('name', 'Неизвестный' if lang == 'ru' else 'Unknown')
                list_text += f"👤 {name} (ID: {employee_id})\n"
        
        await update.message.reply_text(list_text)
        return EMPLOYEE_MENU
    
    elif text in ["🗑️ Удалить сотрудника", "🗑️ Delete Employee"]:
        if lang == 'ru':
            await update.message.reply_text(
                "Введите Telegram ID сотрудника для удаления:",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text(
                "Enter the Telegram ID of the employee to delete:",
                reply_markup=ReplyKeyboardRemove()
            )
        return DELETE_EMPLOYEE
    
    elif text in ["🔗 Моя реферальная ссылка", "🔗 My Referral Link"]:
        employees = db.get_employees()
        user_id = str(update.effective_user.id)
        
        if user_id in employees:
            referral_link = employees[user_id].get('referral_link', '')
            if lang == 'ru':
                await update.message.reply_text(
                    f"🔗 Ваша реферальная ссылка:\n\n{referral_link}\n\nДелитесь ей с клиентами!"
                )
            else:
                await update.message.reply_text(
                    f"🔗 Your referral link:\n\n{referral_link}\n\nShare it with clients!"
                )
        else:
            if lang == 'ru':
                await update.message.reply_text("Вы не являетесь сотрудником.")
            else:
                await update.message.reply_text("You are not an employee.")
        return MAIN_MENU

async def delete_employee_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('language', 'ru')
    telegram_id = update.message.text.strip()
    
    try:
        employees = db.get_employees()
        if telegram_id in employees:
            db.remove_employee(telegram_id)
            if lang == 'ru':
                await update.message.reply_text(
                    f"Сотрудник с ID {telegram_id} удален.",
                    reply_markup=create_main_menu_keyboard(lang, True)
                )
            else:
                await update.message.reply_text(
                    f"Employee with ID {telegram_id} deleted.",
                    reply_markup=create_main_menu_keyboard(lang, True)
                )
        else:
            if lang == 'ru':
                await update.message.reply_text(
                    f"Сотрудник с ID {telegram_id} не найден.",
                    reply_markup=create_main_menu_keyboard(lang, True)
                )
            else:
                await update.message.reply_text(
                    f"Employee with ID {telegram_id} not found.",
                    reply_markup=create_main_menu_keyboard(lang, True)
                )
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Ошибка при удалении сотрудника: {e}")
        if lang == 'ru':
            await update.message.reply_text("Произошла ошибка.")
        else:
            await update.message.reply_text("An error occurred.")
        return DELETE_EMPLOYEE

async def add_employee_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('language', 'ru')
    
    try:
        employee_data = update.message.text.split(',')
        if len(employee_data) != 2:
            if lang == 'ru':
                await update.message.reply_text("Ошибка: используйте формат 'имя,ID'")
            else:
                await update.message.reply_text("Error: use format 'name,ID'")
            return ADD_EMPLOYEE
            
        name = employee_data[0].strip()
        telegram_id = employee_data[1].strip()
        
        # Генерация уникальной реферальной ссылки
        referral_code = str(uuid.uuid4())[:8]
        referral_link = f"https://t.me/cryptocrip_bot?start={referral_code}"
        
        # Добавление сотрудника в базу данных
        db.add_employee(telegram_id, name, referral_link)
        
        # Отправка реферальной ссылки сотруднику
        try:
            if lang == 'ru':
                employee_message = (
                    f"🎉 Вы добавлены как сотрудник!\n"
                    f"Ваша реферальная ссылка:\n{referral_link}\n\n"
                    f"Делитесь ей с клиентами для получения комиссии."
                    f"Перезапустите бота"
                )
            else:
                employee_message = (
                    f"🎉 You have been added as an employee!\n"
                    f"Your referral link:\n{referral_link}\n\n"
                    f"Share it with clients to earn commission."
                )
            
            await context.bot.send_message(
                chat_id=int(telegram_id),
                text=employee_message
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение сотруднику {telegram_id}: {e}")
        
        if lang == 'ru':
            await update.message.reply_text(
                f"Сотрудник добавлен!\n"
                f"Имя: {name}\n"
                f"Telegram ID: {telegram_id}\n"
                f"Реферальная ссылка отправлена сотруднику.",
                reply_markup=create_main_menu_keyboard(lang, True)
            )
        else:
            await update.message.reply_text(
                f"Employee added!\n"
                f"Name: {name}\n"
                f"Telegram ID: {telegram_id}\n"
                f"Referral link sent to employee.",
                reply_markup=create_main_menu_keyboard(lang, True)
            )
        return MAIN_MENU
    except Exception as e:
        logger.error(f"Ошибка при добавлении сотрудника: {e}")
        if lang == 'ru':
            await update.message.reply_text("Произошла ошибка. Проверьте формат ввода.")
        else:
            await update.message.reply_text("An error occurred. Check the input format.")
        return ADD_EMPLOYEE

# Обработчик рефералов
async def handle_referral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        return
    
    referral_code = context.args[0]
    employees = db.get_employees()
    
    for employee_id, data in employees.items():
        if data['referral_link'].endswith(referral_code):
            # Сохраняем реферал в базу данных
            db.add_referral(employee_id, str(update.effective_user.id))
            # Сохраняем информацию о сотруднике в user_data
            context.user_data['referrer_employee_id'] = employee_id
            context.user_data['referrer_employee_name'] = data.get('name', 'Неизвестный')
            break

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE_SELECT: [CallbackQueryHandler(language_callback)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)],
            TRADING_EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, experience_handler)],
            TRADING_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_handler)],
            TRADING_SCREENSHOT: [MessageHandler(filters.PHOTO, screenshot_handler), MessageHandler(filters.TEXT & ~filters.COMMAND, screenshot_with_menu_handler)],
            VIP_PLAN_SELECT: [CallbackQueryHandler(vip_plan_callback)],
            VIP_CLUB_PAYMENT: [MessageHandler(filters.PHOTO, vip_screenshot_handler), MessageHandler(filters.TEXT & ~filters.COMMAND, vip_payment_menu_handler)],
            EMPLOYEE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, employee_menu_handler)],
            ADD_EMPLOYEE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_employee_handler)],
            DELETE_EMPLOYEE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_employee_handler)],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    application.add_handler(conv_handler)
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
import json
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

class TopUpStates(StatesGroup):
    waiting_amount = State()

class SupportStates(StatesGroup):
    waiting_message = State()
    waiting_reply = State()

class BuyKeyStates(StatesGroup):
    waiting_tariff = State()
    waiting_duration_type = State()
    waiting_duration_value = State()
    waiting_custom_days = State()

class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()
    waiting_take_amount = State()
    waiting_broadcast = State()
    waiting_key_duration = State()
    waiting_key_user = State()
    waiting_settings = State()
    waiting_search_query = State()
    waiting_give_balance_user = State()
    waiting_give_balance_amount = State()
    waiting_take_balance_user = State()
    waiting_take_balance_amount = State()
    waiting_give_key_user = State()
    waiting_give_key_duration = State()
    waiting_revoke_key_user = State()
    waiting_extend_subscription_user = State()
    waiting_extend_days = State()
    waiting_ban_reason = State()
    waiting_unban_user = State()
    waiting_reset_trial_user = State()
    waiting_vip_user = State()
    waiting_freeze_balance_user = State()
    waiting_unfreeze_balance_user = State()
    waiting_note_user = State()
    waiting_note_text = State()
    waiting_mass_balance_amount = State()
    waiting_export_user = State()
    waiting_change_expiry_user = State()
    waiting_change_expiry_date = State()
    
BOT_TOKEN = "8754304570:AAH45jtcXRsQm2LvGR6mNu848IRi8t8Aoww"
VPN_NAME = "Unlockme VPN"  
ALLOWED_COMMANDS = ["/s", "/start"]
AGREEMENT_URL = "https://t.me/stuffinydev"
CHANNEL_LINK = "https://t.me/stuffinydev"
CHANNEL_ID = "@stuffinydev"
SUPPORT_LINK = "https://t.me/stuffiny"
BOT_USERNAME = "unlockmevpnbot" 
STARS_RATE = 1.20  # Курс: 1₽ = 1.20 Stars
CRYPTO_BOT_TOKEN = "546120:AAPEXt3Ou9x4Rw1sl6paAF99EkJuImo4tzs"
ADMIN_IDS = [8709192653]  # ID администраторов
LOG_GROUP_ID = -5113105384  # ID группы для логов (444)
TARIFFS = {
    "vpn_bypass": {
        "name": "VPN+Обход",
        "base_price": 99,
        "prices": {
            "days": 10,      # цена за 1 день
            "months": 99,     # цена за 1 месяц
            "years": 990      # цена за 1 год
        }
    }
}
IOS_INSTRUCTION_URL = "https://telegra.ph/iOS-instruction"  # Ссылка на инструкцию iOS
ANDROID_INSTRUCTION_URL = "https://telegra.ph/Android-instruction"  # Ссылка на инструкцию Android
# Ссылки на приложения iOS
IOS_HAPP_URL = "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973"
IOS_STREISAND_URL = "https://apps.apple.com/ru/app/streisand/id6450534064"
IOS_V2RAYTUN_URL = "https://apps.apple.com/ru/app/v2raytun/id6476628951"

# Ссылки на приложения Android
ANDROID_HAPP_URL = "https://play.google.com/store/apps/details?id=com.happproxy&pcampaignid=web_share&pli=1"
ANDROID_V2RAYTUN_URL = "https://play.google.com/store/apps/details?id=com.v2raytun.android&pcampaignid=web_share"

# Ссылки на видео-инструкции
VIDEO_INSTRUCTION_IOS = "https://youtube.com/ios-instruction"  # Замени на реальную ссылку
VIDEO_INSTRUCTION_ANDROID = "https://youtube.com/android-instruction"  # Замени на реальную ссылку
DB_FILE = "database.json"
EMOJI_LOCK = "6037249452824072506"  # 🔒
EMOJI_INFO = "5258503720928288433"  # ℹ️
EMOJI_FILE = "5258328383183396223"  # 📖
EMOJI_CHECK = "5870633910337015697"  #✅ 
EMOJI_CROSS = "5870657884844462243"  # ❌
EMOJI_KEY = "6005570495603282482"  # 🔑
EMOJI_STAR = "5958376256788502078"  # ⭐️
EMOJI_WALLET = "5769126056262898415"  # 👛
EMOJI_PEOPLE = "5870772616305839506"  # 👥
EMOJI_PROFILE = "5870994129244131212"  # 👤
EMOJI_MONEY = "5904462880941545555"  # 💰
EMOJI_HEART = "5994453058656931434"  # ❤️
EMOJI_GLOBE = "5447410659077661506"  # 🌐
EMOJI_SUPPORT = "5444965061749644170"  # 👨‍💻
EMOJI_CANCEL = "5258318620722733379"  # ❌
EMOJI_EXCLAMATION = "5210952531676504517"  # ❗
EMOJI_STATS = "5258391025281408576"  # 📈
EMOJI_CALENDAR = "5890937706803894250"  # 📅
EMOJI_BACK = "5893192487324880883"  # ◁
EMOJI_DOWNLOAD = "5258336354642697821"  # ⬇️
EMOJI_PC = "5282843764451195532"  # 🖥
EMOJI_LIGHTNING = "5323761960829862762"  # ⚡️
EMOJI_SNOW = "5449449325434266744"  # ❄️
EMOJI_FIRE = "5424972470023104089"  # 🔥
EMOJI_STOP = "5348125953090403204"  # ⏹️

def init_db():
    if not os.path.exists(DB_FILE):
        save_db({"users": {}})

def load_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": {}}
    
def format_period(value: int, duration_type: str) -> str:
    """Правильное склонение: 1 день, 2 дня, 5 дней / 1 месяц / 1 год."""
    if duration_type == "days":
        if 11 <= value % 100 <= 19:
            word = "дней"
        elif value % 10 == 1:
            word = "день"
        elif 2 <= value % 10 <= 4:
            word = "дня"
        else:
            word = "дней"
    elif duration_type == "months":
        if 11 <= value % 100 <= 19:
            word = "месяцев"
        elif value % 10 == 1:
            word = "месяц"
        elif 2 <= value % 10 <= 4:
            word = "месяца"
        else:
            word = "месяцев"
    else:  # years
        if 11 <= value % 100 <= 19:
            word = "лет"
        elif value % 10 == 1:
            word = "год"
        elif 2 <= value % 10 <= 4:
            word = "года"
        else:
            word = "лет"
    return f"{value} {word}"

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_user(user_id: int):
    db = load_db()
    user_id_str = str(user_id)
    if user_id_str not in db["users"]:
        db["users"][user_id_str] = {"user_id": user_id, "registered_at": datetime.now().isoformat()}
        save_db(db)

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📖 Прочитать соглашение",
            url=AGREEMENT_URL,
            icon_custom_emoji_id=EMOJI_FILE
        )],
        [
            InlineKeyboardButton(
                text="Я согласен",
                callback_data="accept_agreement",
                icon_custom_emoji_id=EMOJI_CHECK,
                style="success"
            ),
            InlineKeyboardButton(
                text="Назад",
                callback_data="back",
                icon_custom_emoji_id=EMOJI_INFO
            )
        ]
    ])

def get_subscription_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Подписаться на канал",
            url=CHANNEL_LINK
        )],
        [InlineKeyboardButton(
            text="Я подписался",
            callback_data="check_subscription",
            icon_custom_emoji_id=EMOJI_CHECK,
            style="success"
        )]
    ])

def get_trial_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Да, хочу тестовый период (1 день)",
            callback_data="start_trial",
            style="success"
        )],
        [InlineKeyboardButton(
            text="Нет, отказаться",
            callback_data="decline_trial",
            style="danger"
        )],
        [InlineKeyboardButton(
            text="Купить подписку",
            callback_data="buy_subscription"
        )]
    ])
    
def get_profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Реферальная система",
            callback_data="referral",
            icon_custom_emoji_id=EMOJI_PEOPLE
        )],
        [InlineKeyboardButton(
            text="История покупок",  # Новая кнопка
            callback_data="purchase_history",
            icon_custom_emoji_id=EMOJI_STATS
        )],
        [InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_main",
            icon_custom_emoji_id=EMOJI_BACK
        )]
    ])
    
def get_balance_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="150₽",
                callback_data="topup_150",
                icon_custom_emoji_id=EMOJI_WALLET
            ),
            InlineKeyboardButton(
                text="300₽",
                callback_data="topup_300",
                icon_custom_emoji_id=EMOJI_WALLET
            )
        ],
        [
            InlineKeyboardButton(
                text="450₽",
                callback_data="topup_450",
                icon_custom_emoji_id=EMOJI_WALLET
            ),
            InlineKeyboardButton(
                text="900₽",
                callback_data="topup_900",
                icon_custom_emoji_id=EMOJI_WALLET
            )
        ],
        [
            InlineKeyboardButton(
                text="1500₽",
                callback_data="topup_1500",
                icon_custom_emoji_id=EMOJI_WALLET
            ),
            InlineKeyboardButton(
                text="Своя сумма",
                callback_data="topup_custom",
                icon_custom_emoji_id=EMOJI_WALLET
            )
        ],
        [InlineKeyboardButton(text="◁ Назад", callback_data="back_to_main")]
    ])

def get_payment_keyboard(amount):
    stars_amount = int(amount * STARS_RATE)
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"Telegram Stars {stars_amount}⭐️",
            callback_data=f"pay_stars_{amount}"
        )],
        [InlineKeyboardButton(
            text="ЮКасса (Карта, СБП и др.)",
            callback_data=f"pay_yookassa_{amount}"
        )],
        [InlineKeyboardButton(
            text="Криптовалюта",
            callback_data=f"pay_crypto_soon_{amount}"
        )],
        [InlineKeyboardButton(text="◁ Назад", callback_data="add_balance")]
    ])
    
def get_referral_keyboard(ref_link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Поделиться ссылкой",
            url=f"https://t.me/share/url?url={ref_link}&text=Попробуй {VPN_NAME}!"
        )],
        [InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_main",
            icon_custom_emoji_id=EMOJI_BACK
        )]
    ])
    
def get_ios_apps_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Happ",
            url=IOS_HAPP_URL,
            style="success"
        )],
        [InlineKeyboardButton(
            text="Streisand",
            url=IOS_STREISAND_URL,
            style="primary"
        )],
        [InlineKeyboardButton(
            text="V2RayTun",
            url=IOS_V2RAYTUN_URL,
            style="primary"
        )],
        [InlineKeyboardButton(
            text="Видео-инструкция",
            url=VIDEO_INSTRUCTION_IOS,
            style="primary"
        )],
        [InlineKeyboardButton(
            text="Выбрать другую платформу",
            callback_data="instruction",
            style="primary"
        )],
        [InlineKeyboardButton(
            text="◁ Назад",
            callback_data="back_to_main"
        )]
    ])

def get_android_apps_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Happ Proxy",
            url=ANDROID_HAPP_URL,
            style="success"
        )],
        [InlineKeyboardButton(
            text="V2RayTun",
            url=ANDROID_V2RAYTUN_URL,
            style="primary"
        )],
        [InlineKeyboardButton(
            text="Видео-инструкция",
            url=VIDEO_INSTRUCTION_ANDROID,
            style="primary"
        )],
        [InlineKeyboardButton(
            text="Выбрать другую платформу",
            callback_data="instruction",
            style="primary"
        )],
        [InlineKeyboardButton(
            text="◁ Назад",
            callback_data="back_to_main"
        )]
    ])
    
def get_problem_types_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Проблемы с VPN",
            callback_data="problem_vpn"
        )],
        [InlineKeyboardButton(
            text="Проблемы с оплатой",
            callback_data="problem_payment"
        )],
        [InlineKeyboardButton(
            text="Проблемы с ботом",
            callback_data="problem_bot"
        )],
        [InlineKeyboardButton(
            text="Не прошла оплата",
            callback_data="problem_payment_failed"
        )],
        [InlineKeyboardButton(
            text="Другая проблема",
            callback_data="problem_other"
        )],
        [InlineKeyboardButton(text="◁ Назад", callback_data="back_to_main")]
    ])
    
def get_admin_keyboard():
    db = load_db()
    users_count = len(db.get("users", {}))
    tickets_count = len([t for t in db.get("support_tickets", {}).values() if t.get("status") == "open"])
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'Управление пользователями ({users_count})',
            callback_data="admin_users_manage",
            icon_custom_emoji_id=EMOJI_PEOPLE
        )],
        [InlineKeyboardButton(
            text='Финансы и балансы',
            callback_data="admin_finances",
            icon_custom_emoji_id=EMOJI_MONEY
        )],
        [InlineKeyboardButton(
            text='Управление подписками',
            callback_data="admin_subscriptions",
            icon_custom_emoji_id=EMOJI_KEY
        )],
        [InlineKeyboardButton(
            text='Статистика',
            callback_data="admin_stats",
            icon_custom_emoji_id=EMOJI_STATS
        )],
        [InlineKeyboardButton(
            text='Настройки бота',
            callback_data="admin_settings",
            icon_custom_emoji_id=EMOJI_INFO
        )],
        [InlineKeyboardButton(
            text=f'Обращения поддержки ({tickets_count} новых)',
            callback_data="admin_support_tickets",
            icon_custom_emoji_id=EMOJI_SUPPORT
        )],
        [InlineKeyboardButton(
            text='Рассылка',
            callback_data="admin_broadcast",
            icon_custom_emoji_id=EMOJI_GLOBE
        )],
        [InlineKeyboardButton(
            text='Управление серверами',
            callback_data="admin_servers",
            icon_custom_emoji_id=EMOJI_PC
        )]
    ])

def get_trial_manage_keyboard():
    db = load_db()
    trial_enabled = db.get("settings", {}).get("trial_enabled", True)
    
    # Используем EMOJI_CHECK и EMOJI_CROSS для кнопок
    if trial_enabled:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Выключить тестовый период",
                callback_data="admin_trial_disable",
                icon_custom_emoji_id=EMOJI_CROSS
            )],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="admin_back",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Включить тестовый период",
                callback_data="admin_trial_enable",
                icon_custom_emoji_id=EMOJI_CHECK
            )],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="admin_back",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])

def get_apps_manage_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Happ",
            callback_data="admin_app_happ"
        )],
        [InlineKeyboardButton(
            text="Streisand",
            callback_data="admin_app_streisand"
        )],
        [InlineKeyboardButton(
            text="V2RayTun",
            callback_data="admin_app_v2raytun"
        )],
        [InlineKeyboardButton(
            text="◁ Назад",
            callback_data="admin_back"
        )]
    ])
    
def get_instruction_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="iOS",
                callback_data="instruction_ios",
                icon_custom_emoji_id=EMOJI_DOWNLOAD,
                style="primary"
            ),
            InlineKeyboardButton(
                text="Android",
                callback_data="instruction_android",
                icon_custom_emoji_id=EMOJI_DOWNLOAD,
                style="primary"
            )
        ],
        [
            InlineKeyboardButton(
                text="Другое",
                callback_data="instruction_other",
                icon_custom_emoji_id=EMOJI_PC,
                style="primary"
            ),
            InlineKeyboardButton(
                text="Инструкция по обходу",
                callback_data="instruction_bypass",
                icon_custom_emoji_id=EMOJI_FILE,
                style="primary"
            )
        ],
        [InlineKeyboardButton(
            text="◁ Назад",
            callback_data="back_to_main"
        )]
    ])
    
def get_main_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Купить ключ",
            callback_data="buy_key",
            icon_custom_emoji_id=EMOJI_KEY,
            style="success"
        )],
        [
            InlineKeyboardButton(
                text="Пополнить баланс",
                callback_data="add_balance",
                icon_custom_emoji_id=EMOJI_WALLET
            ),
            InlineKeyboardButton(
                text="Мои ключи",
                callback_data="my_keys",
                icon_custom_emoji_id=EMOJI_KEY
            )
        ],
        [
            InlineKeyboardButton(
                text="Инструкция",
                callback_data="instruction",
                icon_custom_emoji_id=EMOJI_FILE
            ),
          InlineKeyboardButton(
                text="Статус серверов",
                callback_data="server_status",
                icon_custom_emoji_id=EMOJI_STATS
            )  
        ],
        [
            InlineKeyboardButton(
                text="Пригласить друга",
                callback_data="referral",
                icon_custom_emoji_id=EMOJI_PEOPLE
            ),
            InlineKeyboardButton(
                text="Профиль",
                callback_data="profile",
                icon_custom_emoji_id=EMOJI_HEART
            )
        ],
        [InlineKeyboardButton(
            text="Наш канал",
            url=CHANNEL_LINK,
            icon_custom_emoji_id=EMOJI_GLOBE
        )],
        [
            InlineKeyboardButton(
                text="Юр. соглашение",
                url=AGREEMENT_URL,
                icon_custom_emoji_id=EMOJI_INFO
            ),
            InlineKeyboardButton(
                text="Поддержка",
                url=SUPPORT_LINK,
                icon_custom_emoji_id=EMOJI_SUPPORT
            )
        ],
        [
            InlineKeyboardButton(
                text="Сообщить о проблеме",
                callback_data="report_problem",
                icon_custom_emoji_id=EMOJI_CANCEL,
                style="danger"
            ),
            InlineKeyboardButton(
                text="О сервисе",
                callback_data="about",
                icon_custom_emoji_id=EMOJI_INFO
            )
        ]
    ])


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

from aiogram import BaseMiddleware
from typing import Callable, Any

class CallbackLogMiddleware(BaseMiddleware):
    """Логирует каждое нажатие на инлайн-кнопку в группу."""
    async def __call__(self, handler: Callable, event: Any, data: dict):
        if isinstance(event, CallbackQuery):
            uid = event.from_user.id
            btn = event.data or "—"
            # Красивые названия для популярных кнопок
            labels = {
                "back_to_main": "Главное меню",
                "profile": "Профиль",
                "buy_key": "Купить ключ",
                "add_balance": "Пополнить баланс",
                "referral": "Рефералы",
                "instruction": "Инструкция",
                "server_status": "Статус серверов",
                "report_problem": "Поддержка",
                "about": "О сервисе",
                "start_trial": "Активировать триал",
                "decline_trial": "Отклонить триал",
                "accept_agreement": "Принял соглашение",
                "check_subscription": "Проверить подписку",
                "admin_back": "Назад в админ-панель",
                "admin_users_manage": "Управление пользователями",
                "admin_subscriptions": "Подписки",
                "admin_finances": "Финансы",
                "admin_broadcast": "Рассылка",
                "admin_support_tickets": "Тикеты поддержки",
                "admin_settings": "Настройки бота",
                "admin_give_balance": "Выдать баланс",
                "purchase_history": "История операций",
            }
            label = labels.get(btn) or btn
            try:
                db = load_db()
                udata = db["users"].get(str(uid), {})
                name = udata.get("first_name", "—")
                uname = udata.get("username", "—")
                balance = udata.get("balance", 0)
                is_admin = "👑" if uid in ADMIN_IDS else ""
                ts = __import__("datetime").datetime.now().strftime("%d.%m %H:%M:%S")
                text = (
                    f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> <code>{ts}</code> {is_admin}\n'
                    f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> {name} | @{uname} | <code>{uid}</code>\n'
                    f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Баланс: <b>{balance}₽</b>\n'
                    f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Нажал: <b>{label}</b>\n'
                    f'<tg-emoji emoji-id="{EMOJI_FILE}">📋</tg-emoji> data: <code>{btn}</code>'
                )
                await bot.send_message(LOG_GROUP_ID, text, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(f"Ошибка middleware лога: {e}")
        return await handler(event, data)

dp.callback_query.middleware(CallbackLogMiddleware())

async def log_action(user_id: int, action: str, extra: str = None):
    """Детальное логирование всех действий в группу."""
    if user_id == bot.id:
        return
    try:
        db = load_db()
        user_data = db["users"].get(str(user_id), {})
        username = user_data.get("username") or "нет"
        first_name = user_data.get("first_name") or "нет имени"
        balance = user_data.get("balance", 0)
        is_admin = "👑 ADMIN" if user_id in ADMIN_IDS else "👤 user"
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        group_text = (
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> <code>{timestamp}</code>\n'
            f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> {first_name} | @{username} | <code>{user_id}</code> | {is_admin}\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Баланс: <b>{balance}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> {action}'
        )
        if extra:
            group_text += f'\n<tg-emoji emoji-id="{EMOJI_FILE}">📋</tg-emoji> {extra}'

        await bot.send_message(LOG_GROUP_ID, group_text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Ошибка лога: {e}")

@dp.callback_query(F.data == "purchase_history")
async def purchase_history(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    db = load_db()
    
    # Получаем все транзакции пользователя
    all_transactions = db.get("transactions", [])
    user_transactions = []
    
    for t in all_transactions:
        if t.get("user_id") == user_id:
            user_transactions.append(t)
    
    # Сортируем от новых к старым
    user_transactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    if not user_transactions:
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История операций</b>\n\n'
            f'У вас пока нет операций.'
        )
    else:
        text = f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История операций</b>\n\n'
        
        for t in user_transactions[:10]:  # показываем последние 10
            t_type = t.get("type", "")
            amount = t.get("amount", 0)
            timestamp = t.get("timestamp", "").replace("T", " ")[:16]
            
            if t_type == "trial_bonus":
                emoji = "🎁"
                desc = "Бонус за пробный период"
            elif t_type == "payment":
                emoji = "✅"
                desc = "Пополнение"
            elif t_type == "admin_give":
                emoji = "💰"
                desc = "Начисление"
            elif t_type == "hourly_debit":
                emoji = "⏳"
                desc = "Списание"
            else:
                emoji = "•"
                desc = t_type
            
            text += f'{emoji} <b>{desc}:</b> {amount}₽\n   {timestamp}\n\n'
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="◁ Назад в профиль",
                callback_data="profile",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await callback.answer()

@dp.message(F.text.startswith('/'))
async def handle_commands(message: Message):
    command_parts = message.text.split()
    command = command_parts[0]
    
    # Обработка реферальных ссылок
    if command == "/start" and len(command_parts) > 1:
        ref_code = command_parts[1]
        if ref_code.startswith("REF"):
            referrer_id = ref_code.replace("REF", "")
            user_id = str(message.from_user.id)
            
            # Сохраняем реферера для нового пользователя
            db = load_db()
            if user_id not in db["users"]:
                add_user(message.from_user.id)
                db = load_db()
                db["users"][user_id]["referrer"] = referrer_id
                db["users"][user_id]["referral_status"] = "pending"
                
                # Увеличиваем счетчик рефералов у реферера
                if referrer_id in db["users"]:
                    if "referrals" not in db["users"][referrer_id]:
                        db["users"][referrer_id]["referrals"] = []
                    if user_id not in db["users"][referrer_id]["referrals"]:
                        db["users"][referrer_id]["referrals"].append(user_id)
                    
                    # Уведомляем реферера
                    try:
                        await bot.send_message(
                            int(referrer_id),
                            f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Новый реферал!</b>\n\n'
                            f'По вашей ссылке зарегистрировался новый пользователь {message.from_user.first_name}.\n\n'
                            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> После его первой покупки вы получите 20₽ на баланс!',
                            parse_mode=ParseMode.HTML
                        )
                    except:
                        pass
                
                save_db(db)
        
        await cmd_start(message)
        return
    
    if command not in ALLOWED_COMMANDS:
        return

    if command == "/s":
        await admin_panel(message)
    elif command == "/start":
        await cmd_start(message)
        
@dp.message(F.text == "/clear")
async def cmd_clear(message: Message):
    """Удаляет последние ~100 сообщений в чате."""
    chat_id = message.chat.id
    current_id = message.message_id
    deleted = 0
    for msg_id in range(current_id, max(current_id - 100, 1), -1):
        try:
            await bot.delete_message(chat_id, msg_id)
            deleted += 1
        except:
            pass
    # Финальное сообщение (само удалится через 2 сек)
    try:
        note = await bot.send_message(
            chat_id,
            f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Чат очищен',
            parse_mode=ParseMode.HTML
        )
        await asyncio.sleep(2)
        await bot.delete_message(chat_id, note.message_id)
    except:
        pass

async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_id_str = str(user_id)
    
    # Проверяем, новый ли пользователь (до add_user)
    db = load_db()
    is_new_user = user_id_str not in db["users"]
    
    add_user(user_id)
    
    # Обновляем имя и username в БД
    db = load_db()  # загружаем снова после add_user
    db["users"][user_id_str]["first_name"] = message.from_user.first_name
    db["users"][user_id_str]["username"] = message.from_user.username
    save_db(db)
    
    # Если пользователь новый - уведомляем админов
    if is_new_user:
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f'<b><tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Новый пользователь</b>\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Имя: {message.from_user.first_name}\n'
                    f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Username: @{message.from_user.username}\n'
                    f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> ID: <code>{user_id}</code>',
                    parse_mode=ParseMode.HTML
                )
            except:
                pass
    
    # Логируем
    await log_action(user_id, "открыл главное меню")
    
    # Проверяем статус пользователя
    db = load_db()
    user_data = db["users"].get(user_id_str, {})
    
    # Если уже согласился и подписан - показываем главное меню
    if user_data.get("agreed") and user_data.get("subscribed"):
        try:
            member = await bot.get_chat_member(CHANNEL_ID, user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await message.answer(
                    f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> {VPN_NAME}</b>\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:',
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_main_menu_keyboard()
                )
                return
            else:
                user_data["subscribed"] = False
                db["users"][user_id_str] = user_data
                save_db(db)
                
                await message.answer(
                    f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Подписка отменена</b>\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Вы отписались от канала.\n'
                    f'Для продолжения использования {VPN_NAME} необходимо быть подписанным на наш канал.\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подпишитесь снова для доступа к сервису.',
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_subscription_keyboard()
                )
                return
        except:
            pass
    
    # Показываем юридическое соглашение
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🔒</tg-emoji> Юридическое соглашение</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Перед использованием сервиса {VPN_NAME} необходимо ознакомиться\n'
        'и согласиться с нашими условиями использования.\n'
        'Нажмите "Прочитать соглашение" чтобы ознакомиться с полным текстом.',
        parse_mode=ParseMode.HTML,
        reply_markup=get_start_keyboard()
    )

@dp.callback_query(F.data == "accept_agreement")
async def accept_agreement(callback: CallbackQuery):
    db = load_db()
    user_id_str = str(callback.from_user.id)
    if user_id_str in db["users"]:
        db["users"][user_id_str]["agreed"] = True
        save_db(db)
    
    # Логируем
    await log_action(callback.from_user.id, "принял соглашение")
    
    await callback.message.edit_text(
        '<b><tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Подписка на канал обязательна!</b>\n\n'
        f'<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Для использования {VPN_NAME} необходимо быть подписанным на наш канал.\n\n'
        '<tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> <b>На канале вы найдете:</b>\n'
        '• <tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Новости и обновления\n'
        '• <tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Важные объявления\n'
        '• <tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Советы по использованию VPN\n'
        '• <tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Информацию о технических работах',
        parse_mode=ParseMode.HTML,
        reply_markup=get_subscription_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@dp.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        allowed_statuses = ['member', 'administrator', 'creator']
        
        if member.status in allowed_statuses:
            db = load_db()
            user_id_str = str(user_id)
            if user_id_str in db["users"]:
                db["users"][user_id_str]["subscribed"] = True
                db["users"][user_id_str]["subscription_date"] = datetime.now().isoformat()
                save_db(db)
            
            # Логируем
            await log_action(user_id, "подтвердил подписку на канал")
            
            await callback.message.edit_text(
                f'<b><tg-emoji emoji-id="6037249452824072506">🛡️</tg-emoji> Попробуйте {VPN_NAME} бесплатно!</b>\n\n'
                '<tg-emoji emoji-id="5958376256788502078">⭐️</tg-emoji> Мы предоставляем тестовый период на 3 дня чтобы вы могли оценить качество нашего сервиса.\n\n'
                '<b>В тестовый период включено:</b>\n'
                '<tg-emoji emoji-id="6005570495603282482">🔑</tg-emoji> • Основной VPN ключ\n'
                '<tg-emoji emoji-id="6005570495603282482">🔑</tg-emoji> • Обход белых списков\n'
                '<tg-emoji emoji-id="5870633910337015697">✅</tg-emoji> • Полный доступ ко всем функциям\n'
                '<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> • 5 ГБ трафика для обхода белого списка\n\n'
                '<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Хотите попробовать бесплатно?',
                parse_mode=ParseMode.HTML,
                reply_markup=get_trial_keyboard()
            )
            await callback.answer("✅ Подписка подтверждена!", show_alert=False)
        else:
            await callback.answer("❌ Вы не подписаны на канал!", show_alert=True)
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        await callback.answer("❌ Ошибка проверки подписки!", show_alert=True)

@dp.callback_query(F.data == "start_trial")
async def start_trial(callback: CallbackQuery):
    db = load_db()
    user_id_str = str(callback.from_user.id)
    user_data = db["users"].get(user_id_str, {})

    if user_data.get("trial_used"):
        await callback.answer("❌ Вы уже использовали пробный период!", show_alert=True)
        return

    current_balance = user_data.get("balance", 0)
    db["users"][user_id_str]["balance"] = current_balance + 29.0
    db["users"][user_id_str]["trial_used"] = True
    db["users"][user_id_str]["trial_activated_at"] = datetime.now().isoformat()
    
    if "transactions" not in db:
        db["transactions"] = []
    db["transactions"].append({
        "type": "trial_bonus",
        "user_id": user_id_str,
        "amount": 29,
        "timestamp": datetime.now().isoformat()
    })
    save_db(db)

    await log_action(callback.from_user.id, "активировал пробный период", "+29₽")

    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Пробный период активирован!</b>\n\n'
        f'На ваш счёт зачислено 29₽.\n'
        f'Теперь средства будут списываться автоматически — примерно 1.2₽ в час.\n'
        f'Текущий баланс: {current_balance + 29}₽',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="back_to_main",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "decline_trial")
async def decline_trial(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="6037249452824072506">🛡️</tg-emoji> {VPN_NAME}</b>\n\n'
        '<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Вы отказались от тестового периода.\n\n'
        '<tg-emoji emoji-id="6037249452824072506">🛡️</tg-emoji> <b>Вы можете:</b>\n'
        '<tg-emoji emoji-id="6005570495603282482">🔑</tg-emoji> • Купить подписку на 30 дней\n'
        '<tg-emoji emoji-id="5904462880941545555">💰</tg-emoji> • Пополнить баланс\n'
        '<tg-emoji emoji-id="5870772616305839506">👥</tg-emoji> • Использовать реферальную систему\n\n'
        '<tg-emoji emoji-id="5258503720928288433">ℹ️</tg-emoji> Выберите действие:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "buy_subscription")
async def buy_subscription(callback: CallbackQuery):
    await callback.message.edit_text(
        '<b><tg-emoji emoji-id="5769126056262898415">👛</tg-emoji> Покупка подписки</b>\n\n'
        'Здесь будет информация о тарифах.',
        parse_mode=ParseMode.HTML
    )
    await callback.answer()
    
@dp.callback_query(F.data == "buy_key")
async def buy_key(callback: CallbackQuery, state: FSMContext):
    # Логируем
    await log_action(callback.from_user.id, "открыл меню покупки ключа")
    
    db = load_db()
    user_data = db["users"].get(str(callback.from_user.id), {})
    balance = user_data.get("balance", 0)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите тариф:</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Ваш баланс: {balance}₽\n\n'
        f'<b>VPN+Обход 99₽/мес</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> VPN сервера в 5 странах\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Обход белых списков (15 ГБ)\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подключение до 3 устройств',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="VPN+Обход 99₽/мес",
                callback_data="tariff_vpn_bypass",
                icon_custom_emoji_id=EMOJI_KEY
            )]
        ])
    )
    await state.set_state(BuyKeyStates.waiting_tariff)
    await callback.answer()
    
@dp.callback_query(F.data.startswith("tariff_"), BuyKeyStates.waiting_tariff)
async def select_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # сразу убираем часики
    tariff_key = callback.data.replace("tariff_", "")
    tariff = TARIFFS.get(tariff_key)
    
    if not tariff:
        await callback.message.edit_text("❌ Тариф не найден")
        await state.clear()
        return
    
    await state.update_data(selected_tariff=tariff_key)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите длительность:</b>\n\n'
        f'Тариф: {tariff["name"]}\n'
        f'Базовая цена: {tariff["base_price"]}₽/мес\n\n'
        f'<b>Доступные варианты:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Дни (от 1 до 30)\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Месяцы (от 1 до 12)\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Годы (от 1 до 3)\n\n'
        f'Выберите тип периода:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Дни",
                    callback_data="duration_days",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="Месяцы",
                    callback_data="duration_months",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="Годы",
                    callback_data="duration_years",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="buy_key",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await state.set_state(BuyKeyStates.waiting_duration_type)  # меняем состояние
    

@dp.callback_query(F.data.startswith("duration_"), BuyKeyStates.waiting_duration_type)
async def select_duration_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # убираем часики
    duration_type = callback.data.replace("duration_", "")
    await state.update_data(duration_type=duration_type)
    
    data = await state.get_data()
    tariff_key = data.get("selected_tariff")
    tariff = TARIFFS.get(tariff_key)
    
    if not tariff:
        await callback.message.edit_text("❌ Ошибка: тариф не найден")
        await state.clear()
        return
    
    # Определяем текст для единицы измерения
    if duration_type == "days":
        unit_text = "дней"
        price_per_unit = tariff["prices"]["days"]
    elif duration_type == "months":
        unit_text = "месяцев"
        price_per_unit = tariff["prices"]["months"]
    else:  # years
        unit_text = "лет"
        price_per_unit = tariff["prices"]["years"]
    
    # Формируем кнопки
    buttons = []
    if duration_type == "days":
        values = [7, 14, 21, 30]
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"7 {unit_text}",
                    callback_data="duration_value_7",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text=f"14 {unit_text}",
                    callback_data="duration_value_14",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"21 {unit_text}",
                    callback_data="duration_value_21",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text=f"30 {unit_text}",
                    callback_data="duration_value_30",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ]
        ]
    elif duration_type == "months":
        values = [1, 3, 6, 12]
        buttons = [
            [
                InlineKeyboardButton(
                    text="1 месяц",
                    callback_data="duration_value_1",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="3 месяца",
                    callback_data="duration_value_3",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ],
            [
                InlineKeyboardButton(
                    text="6 месяцев",
                    callback_data="duration_value_6",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="12 месяцев",
                    callback_data="duration_value_12",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ]
        ]
    else:  # years
        values = [1, 2, 3]
        buttons = [
            [
                InlineKeyboardButton(
                    text="1 год",
                    callback_data="duration_value_1",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="2 года",
                    callback_data="duration_value_2",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ],
            [
                InlineKeyboardButton(
                    text="3 года",
                    callback_data="duration_value_3",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ]
        ]
    
    # Кнопка "Свой вариант"
    buttons.append([
        InlineKeyboardButton(
            text="Свой вариант",
            callback_data="duration_custom",
            icon_custom_emoji_id=EMOJI_KEY
        )
    ])
    # Кнопка "Назад"
    buttons.append([
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_tariff",  # изменено на отдельный callback
            icon_custom_emoji_id=EMOJI_BACK
        )
    ])
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите количество {unit_text}</b>\n\n'
        f'Тариф: {tariff["name"]}\n'
        f'Цена за 1 {unit_text[:-1] if unit_text != "лет" else "год"}: {price_per_unit}₽',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    # ВАЖНО: меняем состояние на waiting_duration_value
    await state.set_state(BuyKeyStates.waiting_duration_value)
    
@dp.callback_query(F.data == "back_to_tariff", BuyKeyStates.waiting_duration_value)
async def back_to_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Возвращаемся к выбору тарифа
    await buy_key(callback, state)
    
@dp.callback_query(F.data.startswith("duration_value_"), BuyKeyStates.waiting_duration_value)
async def select_duration_value(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # убираем часики
    try:
        value = int(callback.data.replace("duration_value_", ""))
        
        # Проверяем наличие данных
        data = await state.get_data()
        if not data.get("selected_tariff") or not data.get("duration_type"):
            await callback.message.edit_text(
                "❌ Ошибка: данные утеряны. Начните заново.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Купить ключ", callback_data="buy_key")]
                ])
            )
            await state.clear()
            return
        
        await calculate_and_show_payment(callback, state, value)
        
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка: {str(e)}")
        await state.clear()
        
@dp.callback_query(F.data == "duration_custom", BuyKeyStates.waiting_duration_value)
async def select_custom_duration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    duration_type = data.get("duration_type")
    
    if duration_type == "days":
        unit_text = "дней (от 1 до 30)"
    elif duration_type == "months":
        unit_text = "месяцев (от 1 до 12)"
    else:
        unit_text = "лет (от 1 до 3)"
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Введите количество {unit_text}</b>\n\n'
        f'Напишите число:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Отмена",
                callback_data="buy_key",
                icon_custom_emoji_id=EMOJI_CANCEL
            )]
        ])
    )
    await state.set_state(BuyKeyStates.waiting_custom_days)
        
@dp.callback_query(F.data == "back_to_tariff_selection", BuyKeyStates.waiting_duration_value)
async def back_to_tariff_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Очищаем данные о длительности, но сохраняем выбранный тариф
    data = await state.get_data()
    tariff_key = data.get("selected_tariff")
    tariff = TARIFFS.get(tariff_key)
    
    # Показываем меню выбора длительности заново
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите длительность:</b>\n\n'
        f'Тариф: {tariff["name"]}\n'
        f'Базовая цена: {tariff["base_price"]}₽/мес\n\n'
        f'<b>Доступные варианты:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Дни (от 1 до 30)\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Месяцы (от 1 до 12)\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Годы (от 1 до 3)\n\n'
        f'Выберите тип периода:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Дни",
                    callback_data="duration_days",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="Месяцы",
                    callback_data="duration_months",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                ),
                InlineKeyboardButton(
                    text="Годы",
                    callback_data="duration_years",
                    icon_custom_emoji_id=EMOJI_CALENDAR
                )
            ],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="buy_key",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await state.set_state(BuyKeyStates.waiting_duration_type)
    
async def calculate_and_show_payment(update, state: FSMContext, value: int):
    data = await state.get_data()
    tariff_key = data.get("selected_tariff")
    duration_type = data.get("duration_type")
    tariff = TARIFFS.get(tariff_key)
    
    if not tariff:
        await state.clear()
        return
    
    # Рассчитываем цену
    price_per_unit = tariff["prices"][duration_type]
    total_price = price_per_unit * value
    
    # Получаем данные пользователя
    user_id = update.from_user.id if hasattr(update, 'from_user') else update.chat.id
    db = load_db()
    user_data = db["users"].get(str(user_id), {})
    balance = user_data.get("balance", 0)
    
    # Определяем текст для периода
    if duration_type == "days":
        period_text = f"{value} дней"
    elif duration_type == "months":
        period_text = f"{value} месяцев"
    else:  # years
        period_text = f"{value} лет"
    
    # Определяем, что за объект пришёл (CallbackQuery или Message)
    is_callback = hasattr(update, 'message') and hasattr(update, 'data')
    
    if balance >= total_price:
        # Хватает баланса – списываем и "выдаём ключ"
        db["users"][str(user_id)]["balance"] = balance - total_price
        save_db(db)
        
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Покупка успешна!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: {tariff["name"]}\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: {period_text}\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Списано: {total_price}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Остаток: {balance - total_price}₽\n\n'
            f'🔑 Ваш ключ будет отправлен отдельным сообщением.'
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="В главное меню",
                callback_data="back_to_main",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
        
        if is_callback:
            await update.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            await update.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    else:
        # Не хватает баланса – предлагаем пополнить
        need_amount = total_price - balance
        
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите способ оплаты</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Ваш баланс: {balance}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Стоимость: {total_price}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Не хватает: {need_amount}₽\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: {tariff["name"]}\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: {period_text}\n\n'
            f'Оплата производится в рублях:'
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Пополнить баланс",
                callback_data="add_balance",
                icon_custom_emoji_id=EMOJI_WALLET
            )],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="buy_key",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
        
        if is_callback:
            await update.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            await update.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    
    await state.clear()

@dp.callback_query(F.data == "duration_custom", BuyKeyStates.waiting_duration_type)
async def select_custom_duration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    duration_type = data.get("duration_type")
    
    if duration_type == "days":
        unit_text = "дней (от 1 до 30)"
    elif duration_type == "months":
        unit_text = "месяцев (от 1 до 12)"
    else:
        unit_text = "лет (от 1 до 3)"
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Введите количество {unit_text}</b>\n\n'
        f'Напишите число:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Отмена",
                callback_data="buy_key",
                icon_custom_emoji_id=EMOJI_CANCEL
            )]
        ])
    )
    await state.set_state(BuyKeyStates.waiting_custom_days)
    await callback.answer()
    
@dp.message(BuyKeyStates.waiting_custom_days)
async def process_custom_duration(message: Message, state: FSMContext):
    # Удаляем сообщение пользователя
    try:
        await message.delete()
    except:
        pass

    data = await state.get_data()
    duration_type = data.get("duration_type")

    limits = {"days": (1, 30), "months": (1, 12), "years": (1, 3)}
    limit_text = {"days": "от 1 до 30 дней", "months": "от 1 до 12 месяцев", "years": "от 1 до 3 лет"}

    try:
        value = int(message.text)
        lo, hi = limits.get(duration_type, (1, 99))
        if value < lo or value > hi:
            err = await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Введите число {limit_text.get(duration_type)}',
                parse_mode=ParseMode.HTML
            )
            await asyncio.sleep(3)
            try:
                await err.delete()
            except:
                pass
            return
        await calculate_and_show_payment(message, state, value)
    except ValueError:
        err = await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Введите целое число',
            parse_mode=ParseMode.HTML
        )
        await asyncio.sleep(3)
        try:
            await err.delete()
        except:
            pass
        
async def calculate_and_show_payment(update, state: FSMContext, value: int):
    data = await state.get_data()
    tariff_key = data.get("selected_tariff")
    duration_type = data.get("duration_type")
    tariff = TARIFFS.get(tariff_key)
    
    if not tariff:
        if hasattr(update, 'message'):
            await update.message.edit_text("❌ Ошибка: тариф не найден")
        else:
            await update.edit_text("❌ Ошибка: тариф не найден")
        await state.clear()
        return
    
    # Рассчитываем цену
    price_per_unit = tariff["prices"][duration_type]
    total_price = price_per_unit * value
    
    # Получаем данные пользователя
    user_id = update.from_user.id if hasattr(update, 'from_user') else update.chat.id
    db = load_db()
    user_data = db["users"].get(str(user_id), {})
    balance = user_data.get("balance", 0)
    
    # Определяем текст для периода
    if duration_type == "days":
        period_text = f"{value} дней"
    elif duration_type == "months":
        period_text = f"{value} месяцев"
    else:
        period_text = f"{value} лет"
    
    # Проверяем баланс
    if balance >= total_price:
        # Хватает баланса - списываем
        db["users"][str(user_id)]["balance"] = balance - total_price
        save_db(db)
        
        # Здесь будет логика выдачи ключа
        if hasattr(update, 'message'):
            message = update.message
        else:
            message = update
            
        await message.edit_text(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Покупка успешна!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: {tariff["name"]}\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: {period_text}\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Списано: {total_price}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Остаток: {balance - total_price}₽\n\n'
            f'🔑 Ваш ключ будет отправлен отдельным сообщением.',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="В главное меню",
                    callback_data="back_to_main",
                    icon_custom_emoji_id=EMOJI_BACK
                )]
            ])
        )
    else:
        # Не хватает баланса
        need_amount = total_price - balance
        
        if hasattr(update, 'message'):
            message = update.message
        else:
            message = update
        
        await message.edit_text(
            f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите способ оплаты</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Ваш баланс: {balance}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Стоимость: {total_price}₽\n'
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Не хватает: {need_amount}₽\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: {tariff["name"]}\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: {period_text}\n\n'
            f'Оплата производится в рублях:',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Пополнить баланс",
                    callback_data="add_balance",
                    icon_custom_emoji_id=EMOJI_WALLET
                )],
                [InlineKeyboardButton(
                    text="Назад",
                    callback_data="buy_key",
                    icon_custom_emoji_id=EMOJI_BACK
                )]
            ])
        )
    
    await state.clear()

@dp.callback_query(F.data == "add_balance")
async def add_balance(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "открыл меню пополнения")
    
    db = load_db()
    user_data = db["users"].get(str(callback.from_user.id), {})
    balance = user_data.get("balance", 0)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Баланс пользователя</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> <b>Текущий баланс:</b> {balance}₽\n\n'
        f'Выберите действие:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_balance_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "my_keys")
async def my_keys(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "посмотрел свои ключи")
    
    db = load_db()
    user_data = db["users"].get(str(callback.from_user.id), {})
    keys = user_data.get("keys", [])
    active = [k for k in keys if k.get("active")]

    if active:
        keys_text = ""
        for i, k in enumerate(active, 1):
            expiry = k.get("expiry", "")[:10] if k.get("expiry") else "бессрочно"
            tariff = k.get("tariff", "vpn_bypass")
            keys_text += f'{i}. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> {tariff} | до {expiry}\n'
        text = f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Мои ключи</b>\n\n{keys_text}'
    else:
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Мои ключи</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> У вас нет активных ключей.\n\n'
            f'Купите подписку для получения ключа VPN.'
        )

    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Купить ключ", callback_data="buy_key", icon_custom_emoji_id=EMOJI_KEY)],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()
@dp.callback_query(F.data == "instruction")
async def instruction(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "открыл инструкцию")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Инструкция по использованию VPN</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите вашу платформу для получения подробной инструкции:\n\n'
        f'• <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> iOS - iPhone, iPad\n'
        f'• <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Android - телефоны и планшеты\n'
        f'• <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Другое - Windows, macOS, Linux, TV\n'
        f'• <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Инструкция по обходу - как настроить и пользоваться обходом белых списков\n\n'
        f'Для каждой платформы доступны несколько приложений',
        parse_mode=ParseMode.HTML,
        reply_markup=get_instruction_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "server_status")
async def server_status(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "проверил статус серверов")
    
    from datetime import datetime
    
    current_time = datetime.now().strftime("%H:%M:%S")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Состояние серверов {VPN_NAME}</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Данные обновлены: {current_time}\n'
        f'<tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Источник: DEMO режим\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Следующая проверка через: 30 мин\n\n'
        f'<tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> <b>VPN сервера:</b>\n'
        f'🟢 🇫🇮 Финляндия (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'🟢 🇩🇪 Германия (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'🟢 🇵🇱 Польша (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'🟢 🇺🇸 США (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'🟢 🇳🇱 Нидерланды (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'<tg-emoji emoji-id="{EMOJI_GLOBE}">🌐</tg-emoji> <b>Сервера обхода:</b>\n'
        f'🟢 🇷🇺 Обход белых списков (DEMO)\n'
        f'   <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Пинг: —\n'
        f'   <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Качество: DEMO\n\n'
        f'<tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> <b>Общая статистика:</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Онлайн: DEMO режим\n'
        f'• <tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Uptime: —\n'
        f'• <tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> Средний пинг: —\n'
        f'• <tg-emoji emoji-id="{EMOJI_LOCK}">⚠️</tg-emoji> Средние потери: —\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Сеть: DEMO режим',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Обновить", callback_data="server_status", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "referral")
async def referral(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_id_str = str(user_id)
    
    # Логируем
    await log_action(user_id, "открыл реферальную систему")
    
    ref_link = f"https://t.me/{BOT_USERNAME}?start=REF{user_id}"
    
    db = load_db()
    user_data = db["users"].get(user_id_str, {})
    referrals = user_data.get("referrals", [])
    
    total_referrals = len(referrals)
    
    # Подсчет статусов рефералов
    pending_referrals = 0
    completed_referrals = 0
    
    for ref_id in referrals:
        ref_data = db["users"].get(ref_id, {})
        status = ref_data.get("referral_status", "pending")
        if status == "pending":
            pending_referrals += 1
        elif status == "completed":
            completed_referrals += 1
    
    earned = completed_referrals * 20
    
    balance = user_data.get("balance", 0)
    
    # Получаем данные о рефералах для детального отображения
    referrals_list = ""
    if referrals:
        for i, ref_id in enumerate(referrals[:5], 1):
            ref_data = db["users"].get(ref_id, {})
            ref_name = ref_data.get("first_name", "Пользователь")
            ref_status = ref_data.get("referral_status", "pending")
            
            if ref_status == "pending":
                status_text = "ожидает"
                status_emoji = EMOJI_INFO
            elif ref_status == "completed":
                status_text = "выполнен"
                status_emoji = EMOJI_CHECK
            else:
                status_text = "ждет"
                status_emoji = EMOJI_INFO
            
            referrals_list += f'{i}. {ref_name} - <tg-emoji emoji-id="{status_emoji}">✅</tg-emoji> {status_text}\n'
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Реферальная система {VPN_NAME}</b>\n\n'
        
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Приглашайте друзей и получайте бонусы!\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_STAR}">⭐️</tg-emoji> За каждого друга:</b> 20₽ на баланс\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Ваша статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Всего приглашено: {total_referrals}\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Ожидают покупки: {pending_referrals}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Принесли бонус: {completed_referrals}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Заработано: {earned}₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Ваша реферальная ссылка:</b>\n'
        f'<code>{ref_link}</code>\n\n'
    )
    
    if referrals_list:
        text += f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Последние рефералы:</b>\n{referrals_list}\n\n'
    
    text += (
        f'<b><tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> Как это работает?</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Отправьте друзьям вашу ссылку\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Друг переходит и регистрируется\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> После его первой покупки вам +20₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_STAR}">⭐️</tg-emoji> Советы:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Разместите ссылку в соцсетях\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Отправьте друзьям в личку\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> 10 друзей = 200₽ на баланс!\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Текущий баланс:</b> {balance}₽'
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Поделиться ссылкой",
                url=f"https://t.me/share/url?url={ref_link}&text=Попробуй {VPN_NAME}!",
                icon_custom_emoji_id=EMOJI_GLOBE
            )],
            [InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_main",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "Не указан"
    first_name = callback.from_user.first_name or "Не указано"
    
    # Логируем
    await log_action(user_id, "открыл профиль")
    
    db = load_db()
    user_data = db["users"].get(str(user_id), {})
    
    balance = user_data.get("balance", 0)
    hours_left = balance / 1.2 if balance > 0 else 0
    active_keys = user_data.get("active_keys", 0)
    referrals = len(user_data.get("referrals", []))
    
    reg_date = user_data.get("registered_at", "Неизвестно")
    if reg_date != "Неизвестно":
        reg_date = reg_date.replace("T", " ").split(".")[0]
    
    trial_status = user_data.get("trial_used", False)
    trial_text = f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Использован' if trial_status else f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Не использован'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Ваш профиль</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>ID:</b> <code>{user_id}</code>\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Имя:</b> {first_name}\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Username:</b> @{username}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> <b>Баланс:</b> {balance}₽ (≈ {hours_left:.1f} ч.)\n\n'
        f'<tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> <b>Статистика:</b>\n'
        f'  <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Активных ключей: {active_keys}\n'
        f'  <tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Приглашено друзей: {referrals}\n'
        f'  <tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Регистрация: {reg_date}\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Тестовый период:</b> {trial_text}',
        parse_mode=ParseMode.HTML,
        reply_markup=get_profile_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "report_problem")
async def report_problem(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "открыл форму обращения")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Сообщить о проблеме</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_CANCEL}">❌</tg-emoji> Выберите тип проблемы:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_problem_types_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    # Логируем
    await log_action(callback.from_user.id, "открыл информацию о сервисе")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> {VPN_NAME} - О нашем сервисе</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_LOCK}">🔒</tg-emoji> <b>Безопасность и Анонимность</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Современные протоколы шифрования\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Отсутствие логов активности\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Защита от утечек\n\n'
        f'<tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡</tg-emoji> <b>Высокая скорость</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Сервера в разных странах\n'
        f'• <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Неограниченный трафик для VPN\n'
        f'  <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> (Для обхода белого списка - 1 ключ - 15 ГБ трафика)\n'
        f'• <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Стабильное соединение\n'
        f'• <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Подключение подписки в 3-х приложениях\n'
        f'  (Happ, Streisand, V2RayTun)\n\n'
        f'<tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> <b>Доступ ко всему контенту</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Обход географических блокировок\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Доступ к заблокированным сайтам\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Защита в публичных сетях Wi-Fi\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Простота использования</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Легкая настройка за 2 минуты\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Поддержка почти всех устройств\n'
        f'• <tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Круглосуточная техподдержка',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()
    
@dp.callback_query(F.data == "view_agreement")
async def view_agreement(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Юридическое соглашение</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Перед использованием сервиса {VPN_NAME} необходимо ознакомиться\n'
        'и согласиться с нашими условиями использования.\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Нажмите "Прочитать соглашение" чтобы ознакомиться с полным текстом.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📖 Прочитать соглашение",
                url=AGREEMENT_URL,
                icon_custom_emoji_id=EMOJI_FILE
            )],
            [InlineKeyboardButton(text="◁ Назад", callback_data="back_to_main")]
        ])
    )
    await callback.answer()
    
@dp.callback_query(F.data.startswith("topup_"))
async def topup_amount(callback: CallbackQuery, state: FSMContext):
    amount_str = callback.data.replace("topup_", "")
    
    if amount_str == "custom":
        await callback.message.edit_text(
            f'<b><tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Введите свою сумму</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Введите сумму пополнения в рублях (от 50₽ до 10000₽):',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◁ Отмена", callback_data="add_balance", style="danger")]
            ])
        )
        await state.set_state(TopUpStates.waiting_amount)
        await callback.answer()
        return
    
    amount = int(amount_str)
    stars_amount = int(amount * 1.26)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Пополнение баланса</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> <b>Сумма:</b> {amount}₽\n\n'
        f'Выберите способ оплаты:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_payment_keyboard(amount)
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    payment_data = callback.data.replace("pay_", "")
    
    if payment_data == "crypto_soon":
        # Временно убираем криптооплату из Soon
        parts = callback.data.split("_")
        if len(parts) >= 3:
            amount = int(parts[2])
            await process_crypto_payment(callback, amount)
        return
    
    parts = payment_data.split("_")
    method = parts[0]
    amount = int(parts[1])
    
    if method == "stars":
        stars_amount = int(amount * STARS_RATE)
        
        # Создаем инвойс для Stars
        from aiogram.types import LabeledPrice
        
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Пополнение баланса {VPN_NAME}",
            description=f"Пополнение баланса на {amount}₽",
            payload=f"topup_{amount}_{callback.from_user.id}",
            provider_token="",  # Для Stars оставляем пустым
            currency="XTR",  # Telegram Stars
            prices=[LabeledPrice(label=f"Пополнение на {amount}₽", amount=stars_amount)]
        )
        await callback.answer("⭐️ Счет на оплату отправлен!")
        
    elif method == "yookassa":
        await callback.answer("💳 Оплата ЮКасса в разработке", show_alert=True)

async def process_crypto_payment(callback: CallbackQuery, amount: int):
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        url = "https://pay.send.tg/api/createInvoice"
        headers = {
            "Crypto-Pay-API-Token": CRYPTO_BOT_TOKEN
        }
        data = {
            "amount": amount,
            "currency_type": "fiat",
            "fiat": "RUB",
            "description": f"Пополнение баланса {VPN_NAME}",
            "payload": f"topup_{amount}_{callback.from_user.id}"
        }
        
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get("ok"):
                    invoice_url = result["result"]["pay_url"]
                    
                    await callback.message.edit_text(
                        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Оплата криптовалютой</b>\n\n'
                        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Сумма: {amount}₽\n\n'
                        f'Нажмите кнопку ниже для оплаты:',
                        parse_mode=ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="💎 Оплатить криптовалютой", url=invoice_url)],
                            [InlineKeyboardButton(text="◁ Назад", callback_data="add_balance")]
                        ])
                    )
                    await callback.answer()
                else:
                    await callback.answer("❌ Ошибка создания счета", show_alert=True)
            else:
                await callback.answer("❌ Ошибка связи с платежной системой", show_alert=True)

# Обработчик успешной оплаты Stars
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    parts = payload.split("_")
    amount = int(parts[1])
    user_id = parts[2]
    
    # Начисляем баланс
    db = load_db()
    if user_id not in db["users"]:
        db["users"][user_id] = {}
    
    current_balance = db["users"][user_id].get("balance", 0)
    db["users"][user_id]["balance"] = current_balance + amount
    save_db(db)
    
    # Логируем оплату
    await log_action(int(user_id), f"пополнил баланс на {amount}₽")
    
    # Уведомление админам о новой оплате
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Новая оплата</b>\n\n'
                f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Пользователь: <code>{user_id}</code>\n'
                f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Сумма: <b>{amount}₽</b>\n'
                f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Баланс после: <b>{current_balance + amount}₽</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
    
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Оплата успешна!</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> На ваш баланс зачислено: {amount}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Текущий баланс: {current_balance + amount}₽',
        parse_mode=ParseMode.HTML
    )
    
@dp.callback_query(F.data.startswith("problem_"))
async def select_problem_type(callback: CallbackQuery, state: FSMContext):
    problem_type = callback.data.replace("problem_", "")
    
    problem_names = {
        "vpn": "проблемой с VPN",
        "payment": "проблемой с оплатой",
        "bot": "проблемой с ботом",
        "payment_failed": "непрошедшей оплатой",
        "other": "другой проблемой"
    }
    
    problem_name = problem_names.get(problem_type, "проблемой")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Опишите проблему с {problem_name}:</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> • Что именно не работает?\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> • Когда началась проблема?\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> • Что вы уже пробовали сделать?\n\n'
        f'<tg-emoji emoji-id="{EMOJI_CANCEL}">❌</tg-emoji> Опишите максимально подробно:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="◁ Отмена",
                callback_data="report_problem",
                style="danger"
            )]
        ])
    )
    
    await state.update_data(problem_type=problem_type)
    await state.set_state(SupportStates.waiting_message)
    await callback.answer()

@dp.message(SupportStates.waiting_message)
async def process_support_message(message: Message, state: FSMContext):
    data = await state.get_data()
    problem_type = data.get("problem_type", "other")
    
    problem_names = {
        "vpn": "Проблема с VPN",
        "payment": "Проблема с оплатой",
        "bot": "Проблема с ботом",
        "payment_failed": "Не прошла оплата",
        "other": "Другая проблема"
    }
    
    user_id = message.from_user.id
    username = message.from_user.username or "Нет username"
    first_name = message.from_user.first_name or "Нет имени"
    
    # Логируем
    await log_action(user_id, f"отправил обращение в поддержку", f"Тип: {problem_type}")
    
    db = load_db()
    if "support_tickets" not in db:
        db["support_tickets"] = {}
    
    ticket_id = len(db["support_tickets"]) + 1
    db["support_tickets"][str(ticket_id)] = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "problem_type": problem_type,
        "message": message.text,
        "created_at": datetime.now().isoformat(),
        "status": "open"
    }
    save_db(db)
    
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f'<b><tg-emoji emoji-id="{EMOJI_CANCEL}">❌</tg-emoji> Новое обращение #{ticket_id}</b>\n\n'
                f'<b>Тип:</b> {problem_names.get(problem_type)}\n'
                f'<b>От:</b> {first_name} (@{username})\n'
                f'<b>ID:</b> <code>{user_id}</code>\n\n'
                f'<b>Сообщение:</b>\n{message.text}',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="Ответить",
                        callback_data=f"support_reply_{ticket_id}"
                    )],
                    [InlineKeyboardButton(
                        text="Закрыть обращение",
                        callback_data=f"support_close_{ticket_id}"
                    )]
                ])
            )
        except:
            pass
    
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Обращение отправлено!</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Номер обращения: #{ticket_id}\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Наша поддержка ответит вам в ближайшее время.\n\n'
        f'<tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Обычно мы отвечаем в течение 1-2 часов.',
        parse_mode=ParseMode.HTML
    )
    
    await state.clear()

@dp.callback_query(F.data.startswith("support_reply_"))
async def admin_reply_to_ticket(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    ticket_id = callback.data.replace("support_reply_", "")
    
    await callback.message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Ответ на обращение #{ticket_id}</b>\n\n'
        f'Напишите ваш ответ:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Отмена", callback_data="admin_support_tickets")]
        ])
    )
    
    await state.update_data(ticket_id=ticket_id)
    await state.set_state(SupportStates.waiting_reply)
    await callback.answer()

@dp.message(SupportStates.waiting_reply)
async def send_admin_reply(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    
    db = load_db()
    ticket = db["support_tickets"].get(ticket_id)
    
    if not ticket:
        await message.answer("❌ Обращение не найдено")
        await state.clear()
        return
    
    user_id = ticket["user_id"]
    
    # Отправляем ответ пользователю
    try:
        await bot.send_message(
            user_id,
            f'<b><tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Ответ поддержки #{ticket_id}</b>\n\n'
            f'{message.text}',
            parse_mode=ParseMode.HTML
        )
        
        # Обновляем статус
        db["support_tickets"][ticket_id]["status"] = "answered"
        db["support_tickets"][ticket_id]["admin_reply"] = message.text
        db["support_tickets"][ticket_id]["answered_at"] = datetime.now().isoformat()
        save_db(db)
        
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Ответ отправлен пользователю!',
            parse_mode=ParseMode.HTML
        )
    except:
        await message.answer("❌ Не удалось отправить ответ пользователю")
    
    await state.clear()

@dp.callback_query(F.data.startswith("support_close_"))
async def admin_close_ticket(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    ticket_id = callback.data.replace("support_close_", "")
    
    db = load_db()
    if ticket_id in db.get("support_tickets", {}):
        db["support_tickets"][ticket_id]["status"] = "closed"
        db["support_tickets"][ticket_id]["closed_at"] = datetime.now().isoformat()
        save_db(db)
        
        await callback.answer("✅ Обращение закрыто")
        await callback.message.edit_reply_markup(reply_markup=None)
    else:
        await callback.answer("❌ Обращение не найдено", show_alert=True)
    
@dp.message(TopUpStates.waiting_amount)
async def process_custom_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        
        if amount < 50 or amount > 10000:
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Сумма должна быть от 50₽ до 10000₽',
                parse_mode=ParseMode.HTML
            )
            return
        
        stars_amount = int(amount * STARS_RATE)
        
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Пополнение баланса</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> <b>Сумма:</b> {amount}₽\n\n'
            f'Выберите способ оплаты:',
            parse_mode=ParseMode.HTML,
            reply_markup=get_payment_keyboard(amount)
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пожалуйста, введите число',
            parse_mode=ParseMode.HTML
        )
        
async def calculate_and_show_payment(update, state: FSMContext, value: int):
    data = await state.get_data()
    tariff_key = data.get("selected_tariff")
    duration_type = data.get("duration_type")
    tariff = TARIFFS.get(tariff_key)

    if not tariff:
        if isinstance(update, CallbackQuery):
            await update.message.edit_text(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ошибка: тариф не найден',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Назад", callback_data="buy_key", icon_custom_emoji_id=EMOJI_BACK)]
                ])
            )
        else:
            await update.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ошибка: тариф не найден',
                parse_mode=ParseMode.HTML
            )
        await state.clear()
        return

    price_per_unit = tariff["prices"][duration_type]
    total_price = price_per_unit * value

    user_id = update.from_user.id
    db = load_db()
    user_data = db["users"].get(str(user_id), {})
    balance = user_data.get("balance", 0)

    # Правильные падежи
    period_text = format_period(value, duration_type)

    is_callback = isinstance(update, CallbackQuery)

    if balance >= total_price:
        db["users"][str(user_id)]["balance"] = balance - total_price
        save_db(db)
        await check_referral_completion(str(user_id))
        await log_action(
            user_id,
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Купил ключ',
            f'Тариф: {tariff["name"]} | Период: {period_text} | Списано: {total_price}₽'
        )

        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Покупка успешна!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: <b>{tariff["name"]}</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: <b>{period_text}</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Списано: <b>{total_price}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Остаток: <b>{balance - total_price}₽</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Ваш ключ будет отправлен отдельным сообщением.'
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Главное меню", callback_data="back_to_main", icon_custom_emoji_id=EMOJI_BACK)]
        ])
        if is_callback:
            await update.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            await update.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    else:
        need_amount = total_price - balance
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Недостаточно средств</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Ваш баланс: <b>{balance}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Стоимость: <b>{total_price}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Не хватает: <b>{need_amount}₽</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Тариф: {tariff["name"]}\n'
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Период: {period_text}'
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пополнить баланс", callback_data="add_balance", icon_custom_emoji_id=EMOJI_WALLET)],
            [InlineKeyboardButton(text="Назад", callback_data="buy_key", icon_custom_emoji_id=EMOJI_BACK)]
        ])
        if is_callback:
            await update.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            await update.answer(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    await state.clear()
    
async def check_referral_completion(user_id: str):
    """Проверяет и начисляет бонус рефереру при первой покупке пользователя"""
    db = load_db()
    user_data = db["users"].get(user_id, {})
    
    # Если у пользователя есть реферер и статус pending
    referrer_id = user_data.get("referrer")
    referral_status = user_data.get("referral_status")
    
    if referrer_id and referral_status == "pending":
        # Меняем статус
        db["users"][user_id]["referral_status"] = "completed"
        
        # Начисляем бонус рефереру
        if referrer_id in db["users"]:
            current_balance = db["users"][referrer_id].get("balance", 0)
            db["users"][referrer_id]["balance"] = current_balance + 20
            
            # Добавляем транзакцию
            if "transactions" not in db:
                db["transactions"] = []
            db["transactions"].append({
                "type": "referral_bonus",
                "user_id": referrer_id,
                "referral_id": user_id,
                "amount": 20,
                "timestamp": datetime.now().isoformat()
            })
            
            # Уведомляем реферера
            try:
                await bot.send_message(
                    int(referrer_id),
                    f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Реферальный бонус!</b>\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Ваш друг совершил первую покупку!\n'
                    f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Вам начислено <b>20₽</b> на баланс.\n\n'
                    f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Текущий баланс: {current_balance + 20}₽',
                    parse_mode=ParseMode.HTML
                )
            except:
                pass
        
        save_db(db)
        return True
    return False
@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> {VPN_NAME}</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()
    
@dp.callback_query(F.data == "instruction_other")
async def instruction_other(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_PC}">🖥</tg-emoji> Инструкция для других платформ</b>\n\n'
        f'Здесь будет инструкция для Windows, macOS, Linux, TV.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="◁ Назад",
                callback_data="instruction"
            )]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "instruction_bypass")
async def instruction_bypass(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> Инструкция по обходу белых списков</b>\n\n'
        f'Здесь будет инструкция по настройке и использованию обхода.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="◁ Назад",
                callback_data="instruction"
            )]
        ])
    )
    await callback.answer()
    
@dp.callback_query(F.data == "instruction_ios")
async def instruction_ios(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Инструкция для iOS (iPhone/iPad)</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Выберите приложение:</b>\n\n'
        f'<b>1. Happ (рекомендуется)</b>\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Самый стабильный\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Простой и красивый интерфейс\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Автоматическая настройка\n\n'
        f'<b>2. Streisand</b>\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Хорошая альтернатива\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Поддержка всех протоколов\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Расширенные настройки\n\n'
        f'<b>3. V2RayTun</b>\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Для продвинутых пользователей\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Высокая скорость\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Много настроек\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Как установить:</b>\n'
        f'1. <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Нажмите на кнопку с названием приложения выше\n'
        f'2. <tg-emoji emoji-id="{EMOJI_KEY}">🔗</tg-emoji> Откроется App Store\n'
        f'3. <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Нажмите "Получить" и установите\n'
        f'4. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> После установки вернитесь в бота\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Как добавить ключ VPN:</b>\n'
        f'1. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> В главном меню бота нажмите "Мои ключи"\n'
        f'2. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите ваш ключ\n'
        f'3. <tg-emoji emoji-id="{EMOJI_KEY}">🔗</tg-emoji> Нажмите "Ссылка на подключение"\n'
        f'4. <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Откроется сайт с кнопками\n'
        f'5. <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> На сайте выберите кнопку с названием вашего приложения\n'
        f'6. <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подписка автоматически добавится в приложение\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Видео-инструкция по настройке:</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=get_ios_apps_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "instruction_android")
async def instruction_android(callback: CallbackQuery):
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Инструкция для Android</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>Выберите приложение:</b>\n\n'
        f'<b>1. Happ Proxy (рекомендуется)</b>\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Русский интерфейс\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Простая настройка\n'
        f'   <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Высокая стабильность\n\n'
        f'<b>2. V2RayTun</b>\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Самое популярное\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Много функций\n'
        f'   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Регулярные обновления\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Как установить:</b>\n'
        f'1. <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Нажмите на кнопку с названием приложения выше\n'
        f'2. <tg-emoji emoji-id="{EMOJI_KEY}">🔗</tg-emoji> Откроется Google Play\n'
        f'3. <tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Нажмите "Установить"\n'
        f'4. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> После установки вернитесь в бота\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Как добавить ключ VPN:</b>\n'
        f'1. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> В главном меню бота нажмите "Мои ключи"\n'
        f'2. <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выберите ваш ключ\n'
        f'3. <tg-emoji emoji-id="{EMOJI_KEY}">🔗</tg-emoji> Нажмите "Ссылка на подключение"\n'
        f'4. <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Откроется сайт с кнопками\n'
        f'5. <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> На сайте выберите кнопку с названием вашего приложения\n'
        f'6. <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подписка автоматически добавится в приложение\n\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📖</tg-emoji> <b>Видео-инструкция по настройке:</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=get_android_apps_keyboard()
    )
    await callback.answer()

@dp.message(F.text == "/s")
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    db = load_db()
    users_count = len(db.get("users", {}))
    active_users = sum(1 for u in db["users"].values() if u.get("subscribed", False))
    total_balance = sum(u.get("balance", 0) for u in db["users"].values())
    open_tickets = len([t for t in db.get("support_tickets", {}).values() if t.get("status") == "open"])
    
    admin_text = (
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Админ-панель</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> <b>Общая статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Всего пользователей: {users_count}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Активных: {active_users}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Общий баланс: {total_balance}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Открытых обращений: {open_tickets}\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите раздел управления:'
    )
    
    await log_action(message.from_user.id, f'<tg-emoji emoji-id="{EMOJI_LOCK}">🔒</tg-emoji> Открыл админ-панель')
    await message.answer(admin_text, parse_mode=ParseMode.HTML, reply_markup=get_admin_keyboard())
    
@dp.callback_query(F.data == "admin_back")
async def admin_back(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users_count = len(db.get("users", {}))
    active_users = sum(1 for u in db["users"].values() if u.get("subscribed", False))
    total_balance = sum(u.get("balance", 0) for u in db["users"].values())
    open_tickets = len([t for t in db.get("support_tickets", {}).values() if t.get("status") == "open"])
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Админ-панель</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> <b>Общая статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Всего пользователей: {users_count}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Активных: {active_users}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Общий баланс: {total_balance}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_SUPPORT}">👨‍💻</tg-emoji> Открытых обращений: {open_tickets}'
    )
    
    await log_action(callback.from_user.id, f'<tg-emoji emoji-id="{EMOJI_BACK}">◁</tg-emoji> Вернулся в главную админ-панель')
    try:
        await callback.message.edit_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_admin_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise e
    finally:
        await callback.answer()

@dp.callback_query(F.data == "admin_trial_manage")
async def admin_trial_manage(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    trial_enabled = db.get("settings", {}).get("trial_enabled", True)
    status_text = "включен" if trial_enabled else "выключен"
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Управление тестовым периодом</b>\n\n'
        f'Текущий статус: <b>{status_text}</b>\n\n'
        f'Выберите действие:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_trial_manage_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "admin_trial_enable")
async def admin_trial_enable(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    if "settings" not in db:
        db["settings"] = {}
    db["settings"]["trial_enabled"] = True
    save_db(db)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Тестовый период включен</b>\n\n'
        f'Пользователи снова могут активировать тестовый период.',
        parse_mode=ParseMode.HTML,
        reply_markup=get_trial_manage_keyboard()
    )
    await callback.answer("✅ Тестовый период включен")

@dp.callback_query(F.data == "admin_trial_disable")
async def admin_trial_disable(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    if "settings" not in db:
        db["settings"] = {}
    db["settings"]["trial_enabled"] = False
    save_db(db)
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Тестовый период выключен</b>\n\n'
        f'Пользователи не смогут активировать тестовый период.',
        parse_mode=ParseMode.HTML,
        reply_markup=get_trial_manage_keyboard()
    )
    await callback.answer("❌ Тестовый период выключен")

@dp.callback_query(F.data == "admin_apps_manage")
async def admin_apps_manage(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Управление приложениями</b>\n\n'
        f'Выберите приложение для настройки видимости:',
        parse_mode=ParseMode.HTML,
        reply_markup=get_apps_manage_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("admin_app_"))
async def admin_app_settings(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    app_name = callback.data.replace("admin_app_", "")
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_LOCK}">🛡️</tg-emoji> Настройки приложения {app_name.title()}</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Функция в разработке.\n'
        f'Скоро здесь можно будет настраивать видимость приложения для отдельных пользователей.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Назад", callback_data="admin_apps_manage")]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "admin_stats")
async def admin_statistics(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    
    total_users = len(users)
    subscribed_users = sum(1 for u in users.values() if u.get("subscribed", False))
    trial_used = sum(1 for u in users.values() if u.get("trial_used", False))
    users_with_balance = sum(1 for u in users.values() if u.get("balance", 0) > 0)
    total_balance = sum(u.get("balance", 0) for u in users.values())
    
    today = datetime.now().strftime("%Y-%m-%d")
    new_today = sum(1 for u in users.values() if u.get("registered_at", "").startswith(today))
    
    transactions = db.get("transactions", [])
    today_transactions = sum(1 for t in transactions if t.get("timestamp", "").startswith(today))
    today_income = sum(t.get("amount", 0) for t in transactions if t.get("timestamp", "").startswith(today) and t.get("type") in ["admin_give", "payment"])
    
    active_keys = 0
    for u in users.values():
        keys = u.get("keys", [])
        active_keys += len([k for k in keys if k.get("active", False)])
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Статистика бота</b>\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Пользователи:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Всего: {total_users}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подписаны: {subscribed_users}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Использовали триал: {trial_used}\n'
        f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> С балансом: {users_with_balance}\n'
        f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Новых сегодня: {new_today}\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Финансы:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Общий баланс: {total_balance}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Транзакций сегодня: {today_transactions}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Доход сегодня: {today_income}₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Подписки:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Активных ключей: {active_keys}',
        
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Обновить', callback_data="admin_stats", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_back", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()
    
@dp.callback_query(F.data == "admin_users_manage")
async def admin_users_manage(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Управление пользователями</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:'
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Поиск пользователя',
            callback_data="admin_user_search",
            icon_custom_emoji_id=EMOJI_INFO
        )],
        [InlineKeyboardButton(
            text='Список всех пользователей',
            callback_data="admin_list_all_users",
            icon_custom_emoji_id=EMOJI_PEOPLE
        )],
        [InlineKeyboardButton(
            text='Активные пользователи',
            callback_data="admin_list_active_users",
            icon_custom_emoji_id=EMOJI_CHECK
        )],
        [InlineKeyboardButton(
            text='С балансом > 0',
            callback_data="admin_list_users_balance",
            icon_custom_emoji_id=EMOJI_MONEY
        )],
        [InlineKeyboardButton(
            text='С активной подпиской',
            callback_data="admin_list_subscribed",
            icon_custom_emoji_id=EMOJI_KEY
        )],
        [InlineKeyboardButton(
            text='Заблокированные',
            callback_data="admin_list_blocked",
            icon_custom_emoji_id=EMOJI_CANCEL
        )],
        [InlineKeyboardButton(
            text='Массовая рассылка',
            callback_data="admin_broadcast",
            icon_custom_emoji_id=EMOJI_GLOBE
        )],
        [InlineKeyboardButton(
            text='Массовая выдача баланса',
            callback_data="admin_mass_give_balance",
            icon_custom_emoji_id=EMOJI_MONEY
        )],
        [InlineKeyboardButton(
            text='Назад',
            callback_data="admin_back",
            icon_custom_emoji_id=EMOJI_BACK
        )]
    ])
    await callback.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    await callback.answer()
    
@dp.callback_query(F.data == "admin_user_search")
async def admin_user_search_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_INFO}">🔍</tg-emoji> Поиск пользователя</b>\n\n'
        f'Введите ID, username (без @) или имя пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_search_query)
    await callback.answer()

@dp.message(AdminStates.waiting_search_query)
async def admin_user_search_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    query = message.text.strip().lower()
    db = load_db()
    found_users = []
    for uid, data in db["users"].items():
        if query == uid:
            found_users = [(uid, data)]
            break
        if data.get("username") and query == data["username"].lower():
            found_users = [(uid, data)]
            break
        if data.get("first_name") and query in data["first_name"].lower():
            found_users.append((uid, data))
    if not found_users:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь не найден.',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🔍 Новый поиск', callback_data="admin_user_search", icon_custom_emoji_id=EMOJI_INFO)],
                [InlineKeyboardButton(text='◁ Назад', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
        return
    if len(found_users) == 1:
        uid, data = found_users[0]
        await show_user_profile(message, uid, data, state)
    else:
        buttons = []
        for uid, data in found_users[:10]:
            name = data.get("first_name", "Нет имени")
            username = data.get("username", "")
            display = f"{name} (@{username})" if username else name
            buttons.append([InlineKeyboardButton(
                text=display[:30],
                callback_data=f"admin_select_user_{uid}",
                icon_custom_emoji_id=EMOJI_PEOPLE
            )])
        buttons.append([InlineKeyboardButton(text='◁ Назад', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)])
        await message.answer(
            f'<b>Найдено несколько пользователей:</b>',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
        await state.clear()
        
async def show_user_profile(update, user_id: str, user_data: dict, state: FSMContext = None):
    name = user_data.get("first_name", "Нет имени")
    username = user_data.get("username", "Нет")
    balance = user_data.get("balance", 0)
    vip = user_data.get("vip", False)
    frozen = user_data.get("balance_frozen", False)
    blocked = user_data.get("blocked", False)
    trial_used = user_data.get("trial_used", False)
    reg_date = user_data.get("registered_at", "Неизвестно")[:10]
    keys = user_data.get("keys", [])
    active_keys = len([k for k in keys if k.get("active")])
    referrals = len(user_data.get("referrals", []))
    note = user_data.get("note", "—")
    ban_reason = user_data.get("ban_reason", "")

    subscribed_icon = f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>' if user_data.get("subscribed") else f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji>'
    blocked_icon = f'<tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji>' if blocked else f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>'
    trial_icon = f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>' if trial_used else f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji>'
    vip_icon = f'<tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji>' if vip else f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji>'
    frozen_icon = f'<tg-emoji emoji-id="{EMOJI_SNOW}">❄️</tg-emoji>' if frozen else f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>'

    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Профиль пользователя</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <b>ID:</b> <code>{user_id}</code>\n'
        f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> <b>Имя:</b> {name}\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> <b>Username:</b> @{username}\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> <b>Баланс:</b> <b>{balance}₽</b>{" 🧊заморожен" if frozen else ""}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>Подписка на канал:</b> {subscribed_icon}\n'
        f'<tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> <b>Заблокирован:</b> {blocked_icon}{f" | Причина: {ban_reason}" if blocked and ban_reason else ""}\n'
        f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> <b>Активных ключей:</b> {active_keys}\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> <b>Рефералов:</b> {referrals}\n'
        f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> <b>Регистрация:</b> {reg_date}\n'
        f'<tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji> <b>VIP:</b> {vip_icon}\n'
        f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> <b>Баланс заморожен:</b> {frozen_icon}\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> <b>Триал использован:</b> {trial_icon}\n'
        f'<tg-emoji emoji-id="{EMOJI_FILE}">📋</tg-emoji> <b>Заметка:</b> {note}\n'
    )

    buttons = [
        [
            InlineKeyboardButton(text='Выдать баланс', callback_data=f"admin_user_give_balance_{user_id}", icon_custom_emoji_id=EMOJI_MONEY),
            InlineKeyboardButton(text='Забрать баланс', callback_data=f"admin_user_take_balance_{user_id}", icon_custom_emoji_id=EMOJI_CROSS)
        ],
        [
            InlineKeyboardButton(text='Выдать ключ', callback_data=f"admin_user_give_key_{user_id}", icon_custom_emoji_id=EMOJI_KEY),
            InlineKeyboardButton(text='Забрать ключи', callback_data=f"admin_user_revoke_key_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)
        ],
        [
            InlineKeyboardButton(text='Продлить подписку', callback_data=f"admin_user_extend_{user_id}", icon_custom_emoji_id=EMOJI_CALENDAR),
            InlineKeyboardButton(text='Отменить подписку', callback_data=f"admin_user_cancel_sub_{user_id}", icon_custom_emoji_id=EMOJI_STOP)
        ],
        [
            InlineKeyboardButton(text='Заблокировать', callback_data=f"admin_user_ban_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL),
            InlineKeyboardButton(text='Разблокировать', callback_data=f"admin_user_unban_{user_id}", icon_custom_emoji_id=EMOJI_CHECK)
        ],
        [
            InlineKeyboardButton(text='Сбросить триал', callback_data=f"admin_user_reset_trial_{user_id}", icon_custom_emoji_id=EMOJI_STAR),
            InlineKeyboardButton(text='Выдать VIP', callback_data=f"admin_user_set_vip_{user_id}", icon_custom_emoji_id=EMOJI_STAR)
        ],
        [
            InlineKeyboardButton(text='Снять VIP', callback_data=f"admin_user_remove_vip_{user_id}", icon_custom_emoji_id=EMOJI_CROSS),
            InlineKeyboardButton(text='Заморозить', callback_data=f"admin_user_freeze_{user_id}", icon_custom_emoji_id=EMOJI_SNOW)
        ],
        [
            InlineKeyboardButton(text='Разморозить', callback_data=f"admin_user_unfreeze_{user_id}", icon_custom_emoji_id=EMOJI_FIRE),
            InlineKeyboardButton(text='История', callback_data=f"admin_user_history_{user_id}", icon_custom_emoji_id=EMOJI_STATS)
        ],
        [
            InlineKeyboardButton(text='Активные ключи', callback_data=f"admin_user_keys_{user_id}", icon_custom_emoji_id=EMOJI_KEY),
            InlineKeyboardButton(text='Заметка', callback_data=f"admin_user_note_{user_id}", icon_custom_emoji_id=EMOJI_FILE)
        ],
        [
            InlineKeyboardButton(text='Экспорт данных', callback_data=f"admin_user_export_{user_id}", icon_custom_emoji_id=EMOJI_DOWNLOAD),
            InlineKeyboardButton(text='Изменить срок', callback_data=f"admin_user_change_expiry_{user_id}", icon_custom_emoji_id=EMOJI_CALENDAR)
        ],
        [
            InlineKeyboardButton(text='Сбросить рефералы', callback_data=f"admin_user_reset_refs_{user_id}", icon_custom_emoji_id=EMOJI_PEOPLE),
            InlineKeyboardButton(text='Удалить', callback_data=f"admin_user_delete_{user_id}", icon_custom_emoji_id=EMOJI_CROSS)
        ],
        [
            InlineKeyboardButton(text='◁ Назад к списку', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)
        ]
    ]

    try:
        if isinstance(update, CallbackQuery):
            await update.message.edit_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
        else:
            await update.answer(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
            )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise e

@dp.callback_query(F.data.startswith("admin_user_give_balance_"))
async def admin_user_give_balance_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_give_balance_", "")
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Выдача баланса</b>\n\n'
        f'Введите сумму для начисления:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_give_balance_amount)
    await callback.answer()

@dp.message(AdminStates.waiting_give_balance_amount)
async def admin_user_give_balance_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer("❌ Сумма должна быть больше 0")
            return
        data = await state.get_data()
        user_id = data.get("target_user_id")
        db = load_db()
        old_balance = db["users"][user_id].get("balance", 0)
        db["users"][user_id]["balance"] = old_balance + amount
        if "transactions" not in db:
            db["transactions"] = []
        db["transactions"].append({
            "type": "admin_give",
            "user_id": user_id,
            "amount": amount,
            "admin_id": message.from_user.id,
            "timestamp": datetime.now().isoformat()
        })
        save_db(db)
        new_balance = old_balance + amount
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Вам начислено {amount}₽ администратором.</b>\n\n'
                f'Текущий баланс: <b>{new_balance}₽</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Выдал баланс пользователю',
            f'Target: <code>{user_id}</code> | +{amount}₽ | Было: {old_balance}₽ → Стало: {new_balance}₽'
        )
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Баланс начислен!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Пользователь: <code>{user_id}</code>\n'
            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Начислено: <b>+{amount}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> Было: {old_balance}₽ → Стало: <b>{new_balance}₽</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
                [InlineKeyboardButton(text='◁ Финансы', callback_data="admin_finances", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите число")

@dp.callback_query(F.data.startswith("admin_select_user_"))
async def admin_select_user(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_select_user_", "")
    db = load_db()
    user_data = db["users"].get(user_id)
    if not user_data:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    await show_user_profile(callback, user_id, user_data)

@dp.callback_query(F.data == "admin_list_all_users")
async def admin_list_all_users(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    
    total = len(users)
    users_list = ""
    
    for idx, (user_id, user_data) in enumerate(list(users.items())[:10], 1):
        name = user_data.get("first_name", "Нет имени")
        username = user_data.get("username", "Нет")
        balance = user_data.get("balance", 0)
        subscribed = user_data.get("subscribed", False)
        subscribed_emoji = EMOJI_CHECK if subscribed else EMOJI_CROSS
        subscribed_text = f'<tg-emoji emoji-id="{subscribed_emoji}">{"✅" if subscribed else "❌"}</tg-emoji>'
        
        users_list += f'{idx}. {subscribed_text} {name}\n   <tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> @{username} | <tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> ID: <code>{user_id}</code>\n   <tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Баланс: {balance}₽\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Список пользователей</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Всего: {total}\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Показано первых 10:\n\n{users_list}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Показать еще', callback_data="admin_list_all_users_more", icon_custom_emoji_id=EMOJI_DOWNLOAD)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "admin_list_active_users")
async def admin_list_active_users(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    
    # Считаем активными тех, кто был активен в последние 7 дней
    active_users = []
    for user_id, user_data in users.items():
        if user_data.get("subscribed"):
            active_users.append((user_id, user_data))
    
    total = len(active_users)
    users_list = ""
    
    for idx, (user_id, user_data) in enumerate(active_users[:10], 1):
        name = user_data.get("first_name", "Нет имени")
        users_list += f'{idx}. {name} (ID: <code>{user_id}</code>)\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Активные пользователи</b>\n\n'
        f'Всего активных: {total}\n'
        f'Показано первых 10:\n\n{users_list}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Назад", callback_data="admin_users_manage")]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "admin_finances")
async def admin_finances(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    transactions = db.get("transactions", [])
    
    total_balance = sum(user.get("balance", 0) for user in users.values())
    users_with_balance = sum(1 for user in users.values() if user.get("balance", 0) > 0)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_income = sum(t.get("amount", 0) for t in transactions if t.get("timestamp", "").startswith(today) and t.get("type") == "payment")
    today_outcome = sum(t.get("amount", 0) for t in transactions if t.get("timestamp", "").startswith(today) and t.get("type") == "admin_give")
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Финансы</b>\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Общая статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Пользователей с балансом: {users_with_balance}\n'
        f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Общий баланс: {total_balance} ₽\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Средний баланс: {total_balance // max(users_with_balance, 1)} ₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Сегодня:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Доход: +{today_income} ₽\n'
        f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Расход: -{today_outcome} ₽\n\n'
        
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:'
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Выдать баланс', callback_data="admin_give_balance", icon_custom_emoji_id=EMOJI_MONEY)],
            [InlineKeyboardButton(text='Забрать баланс', callback_data="admin_take_balance", icon_custom_emoji_id=EMOJI_CROSS)],
            [InlineKeyboardButton(text='История транзакций', callback_data="admin_transactions", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_back", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "admin_servers")
async def admin_servers(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_PC}">🖥</tg-emoji> Управление серверами</b>\n\n'
        f'<b><tg-emoji emoji-id="{EMOJI_GLOBE}">🌐</tg-emoji> Сервера VPN:</b>\n'
        f'🇫🇮 Финляндия - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇩🇪 Германия - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇵🇱 Польша - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇺🇸 США - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇳🇱 Нидерланды - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n\n'
        f'<b><tg-emoji emoji-id="{EMOJI_LIGHTNING}">⚡️</tg-emoji> Сервера обхода:</b>\n'
        f'🇷🇺 Обход белых списков - <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:'
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Проверить статус', callback_data="admin_check_servers", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text='Настройки серверов', callback_data="admin_server_config", icon_custom_emoji_id=EMOJI_INFO)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_back", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()
@dp.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_GLOBE}">📢</tg-emoji> Рассылка</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Отправьте сообщение для рассылки всем пользователям.\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Поддерживаются: текст, фото, видео, документы.\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> <i>Сообщение будет отправлено всем пользователям бота.</i>'
    )
    
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data="admin_back", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.answer()

@dp.message(AdminStates.waiting_broadcast)
async def admin_broadcast_send(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return

    db = load_db()
    users = db.get("users", {})
    success = 0
    failed = 0

    await log_action(
        message.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_GLOBE}">📢</tg-emoji> Запустил рассылку',
        f'Получателей: {len(users)}'
    )
    status_msg = await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_GLOBE}">📢</tg-emoji> Начинаю рассылку...</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Всего пользователей: {len(users)}',
        parse_mode=ParseMode.HTML
    )

    for user_id in users.keys():
        try:
            await bot.copy_message(
                chat_id=int(user_id),
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
        except:
            failed += 1
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Рассылка завершена!</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Успешно: {success}\n'
        f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ошибок: {failed}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ В панель', callback_data="admin_back", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await log_action(
        message.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Рассылка завершена',
        f'Успешно: {success} | Ошибок: {failed}'
    )
    await state.clear()

@dp.callback_query(F.data == "admin_subscriptions")
async def admin_subscriptions(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return

    db = load_db()
    users = db.get("users", {})
    subscribed = sum(1 for user in users.values() if user.get("subscribed", False))
    active_keys = sum(
        len([k for k in user.get("keys", []) if k.get("active", False)])
        for user in users.values()
    )

    text = (
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Управление подписками</b>\n\n'
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Подписано на канал: {subscribed}\n'
        f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Активных ключей: {active_keys}\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Выберите действие:'
    )

    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Выдать подписку', callback_data="admin_give_subscription", icon_custom_emoji_id=EMOJI_KEY)],
            [InlineKeyboardButton(text='Забрать подписку', callback_data="admin_revoke_subscription", icon_custom_emoji_id=EMOJI_CROSS)],
            [InlineKeyboardButton(text='Список активных', callback_data="admin_list_subscribed", icon_custom_emoji_id=EMOJI_PEOPLE)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_back", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data == "admin_support_tickets")
async def admin_support_tickets(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    tickets = db.get("support_tickets", {})
    
    open_tickets = sum(1 for t in tickets.values() if t.get("status") == "open")
    answered_tickets = sum(1 for t in tickets.values() if t.get("status") == "answered")
    closed_tickets = sum(1 for t in tickets.values() if t.get("status") == "closed")
    
    tickets_list = ""
    for ticket_id, ticket in list(tickets.items())[:5]:
        if ticket.get("status") == "open":
            status_emoji = "🔴"
        elif ticket.get("status") == "answered":
            status_emoji = "🟡"
        else:
            status_emoji = "🟢"
        
        tickets_list += f'{status_emoji} #{ticket_id} - {ticket.get("first_name")} ({ticket.get("problem_type")})\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_SUPPORT}">📨</tg-emoji> Обращения поддержки</b>\n\n'
        f'<b>Статистика:</b>\n'
        f'🔴 Открытых: {open_tickets}\n'
        f'🟡 Отвеченных: {answered_tickets}\n'
        f'🟢 Закрытых: {closed_tickets}\n\n'
        f'<b>Последние обращения:</b>\n{tickets_list if tickets_list else "Нет обращений"}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Назад", callback_data="admin_back")]
        ])
    )
    await callback.answer()

# === ВЫДАЧА БАЛАНСА ===
class AdminBalanceStates(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()
    
class AdminTakeBalanceStates(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()

class AdminBlockStates(StatesGroup):
    waiting_user_id = State()
    
class AdminBroadcastStates(StatesGroup):
    waiting_message = State()

@dp.callback_query(F.data == "admin_give_balance")
async def admin_give_balance_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💸</tg-emoji> Выдача баланса</b>\n\n'
        f'Введите ID пользователя или отправьте пересланное сообщение от пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='◁ Отмена',
                callback_data="admin_finances",
                icon_custom_emoji_id=EMOJI_CANCEL
            )]
        ])
    )
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminStates.waiting_user_id)
async def admin_give_balance_get_id(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        # Проверяем, может быть это пересланное сообщение
        user_id = message.text.strip()
        
        # Если это пересланное сообщение от пользователя
        if message.forward_from:
            user_id = str(message.forward_from.id)
        
        db = load_db()
        
        if user_id not in db.get("users", {}):
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь с ID {user_id} не найден',
                parse_mode=ParseMode.HTML
            )
            return
        
        user_data = db["users"][user_id]
        name = user_data.get("first_name", "Нет имени")
        username = user_data.get("username", "Нет")
        balance = user_data.get("balance", 0)
        
        await state.update_data(target_user_id=user_id)
        await state.set_state(AdminStates.waiting_amount)
        
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💸</tg-emoji> Выдача баланса</b>\n\n'
            f'<b>Пользователь:</b>\n'
            f'• Имя: {name}\n'
            f'• Username: @{username}\n'
            f'• ID: <code>{user_id}</code>\n'
            f'• Текущий баланс: {balance}₽\n\n'
            f'Введите сумму для начисления:',
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.answer(f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ошибка: {e}', parse_mode=ParseMode.HTML)

@dp.message(AdminStates.waiting_amount)
async def admin_give_balance_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        amount = int(message.text)
        
        if amount <= 0:
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Сумма должна быть больше 0',
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        user_id = data.get("target_user_id")
        
        db = load_db()
        old_balance = db["users"][user_id].get("balance", 0)
        db["users"][user_id]["balance"] = old_balance + amount
        
        # Сохраняем транзакцию
        if "transactions" not in db:
            db["transactions"] = []
        
        db["transactions"].append({
            "type": "admin_give",
            "user_id": user_id,
            "amount": amount,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.full_name,
            "timestamp": datetime.now().isoformat()
        })
        
        save_db(db)
        
        # Уведомляем пользователя
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Пополнение баланса</b>\n\n'
                f'Администратор начислил вам <b>{amount}₽</b>\n'
                f'Новый баланс: <b>{old_balance + amount}₽</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Баланс успешно начислен!</b>\n\n'
            f'<b>Пользователь:</b> <code>{user_id}</code>\n'
            f'<b>Начислено:</b> {amount}₽\n'
            f'<b>Было:</b> {old_balance}₽\n'
            f'<b>Стало:</b> {old_balance + amount}₽',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text='В финансы',
                    callback_data="admin_finances",
                    icon_custom_emoji_id=EMOJI_MONEY
                )]
            ])
        )
        
        await state.clear()
        
    except ValueError:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Введите число',
            parse_mode=ParseMode.HTML
        )

# === ЗАБРАТЬ БАЛАНС ===
@dp.callback_query(F.data == "admin_take_balance")
async def admin_take_balance_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списание баланса</b>\n\n'
        f'Введите ID пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Отмена", callback_data="admin_finances")]
        ])
    )
    await state.set_state(AdminTakeBalanceStates.waiting_user_id)
    await callback.answer()

@dp.message(AdminTakeBalanceStates.waiting_user_id)
async def admin_take_balance_get_id(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        user_id = message.text.strip()
        db = load_db()
        
        if user_id not in db.get("users", {}):
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь с ID {user_id} не найден',
                parse_mode=ParseMode.HTML
            )
            return
        
        user_data = db["users"][user_id]
        name = user_data.get("first_name", "Нет имени")
        
        await state.update_data(user_id=user_id)
        await state.set_state(AdminTakeBalanceStates.waiting_amount)
        
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списание баланса</b>\n\n'
            f'Пользователь: {name} (ID: <code>{user_id}</code>)\n'
            f'Текущий баланс: {user_data.get("balance", 0)}₽\n\n'
            f'Введите сумму для списания:',
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.answer(f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ошибка: {e}', parse_mode=ParseMode.HTML)

@dp.message(AdminTakeBalanceStates.waiting_amount)
async def admin_take_balance_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        amount = int(message.text)
        
        if amount <= 0:
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Сумма должна быть больше 0',
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        user_id = data.get("user_id")
        
        db = load_db()
        old_balance = db["users"][user_id].get("balance", 0)
        
        if old_balance < amount:
            await message.answer(
                f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Недостаточно средств!\n'
                f'На балансе: {old_balance}₽\n'
                f'Попытка списать: {amount}₽',
                parse_mode=ParseMode.HTML
            )
            return
        
        db["users"][user_id]["balance"] = old_balance - amount
        
        # Сохраняем транзакцию
        if "transactions" not in db:
            db["transactions"] = []
        
        db["transactions"].append({
            "type": "admin_take",
            "user_id": user_id,
            "amount": amount,
            "admin_id": message.from_user.id,
            "timestamp": datetime.now().isoformat()
        })
        
        save_db(db)
        
        # Уведомляем пользователя
        try:
            await bot.send_message(
                user_id,
                f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списание баланса</b>\n\n'
                f'Администратор списал с вашего баланса {amount}₽\n'
                f'Новый баланс: {old_balance - amount}₽',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Баланс успешно списан!</b>\n\n'
            f'Пользователь: <code>{user_id}</code>\n'
            f'Списано: {amount}₽\n'
            f'Было: {old_balance}₽\n'
            f'Стало: {old_balance - amount}₽',
            parse_mode=ParseMode.HTML
        )
        
        await state.clear()
        
    except ValueError:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Введите число',
            parse_mode=ParseMode.HTML
        )

# === СПИСОК ПОЛЬЗОВАТЕЛЕЙ С БАЛАНСОМ ===
@dp.callback_query(F.data == "admin_list_users_balance")
async def admin_list_users_with_balance(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    
    users_with_balance = [(uid, udata) for uid, udata in users.items() if udata.get("balance", 0) > 0]
    users_with_balance.sort(key=lambda x: x[1].get("balance", 0), reverse=True)
    
    users_list = ""
    for idx, (user_id, user_data) in enumerate(users_with_balance[:10], 1):
        name = user_data.get("first_name", "Нет имени")
        balance = user_data.get("balance", 0)
        users_list += f'{idx}. {name} - {balance}₽\n   ID: <code>{user_id}</code>\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Пользователи с балансом</b>\n\n'
        f'Всего: {len(users_with_balance)}\n'
        f'Показано ТОП-10:\n\n{users_list if users_list else "Нет пользователей с балансом"}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◁ Назад", callback_data="admin_users_manage")]
        ])
    )
    await callback.answer()

# === ИСТОРИЯ ТРАНЗАКЦИЙ ===
@dp.callback_query(F.data == "admin_transactions")
async def admin_transactions(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    transactions = db.get("transactions", [])
    
    if not transactions:
        await callback.message.edit_text(
            f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Транзакций пока нет.',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data="admin_finances", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await callback.answer()
        return
    
    total_income = sum(t.get("amount", 0) for t in transactions if t.get("type") == "payment")
    total_outcome = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_give")
    total_taken = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_take")
    
    trans_list = ""
    for idx, trans in enumerate(reversed(transactions[-10:]), 1):
        trans_type = trans.get("type", "unknown")
        amount = trans.get("amount", 0)
        user_id = str(trans.get("user_id", "unknown"))[:8]
        timestamp = trans.get("timestamp", "").replace("T", " ")[:16]
        
        if trans_type == "payment":
            emoji_id = EMOJI_CHECK
            type_text = "Оплата"
        elif trans_type == "admin_give":
            emoji_id = EMOJI_MONEY
            type_text = "Выдача"
        elif trans_type == "admin_take":
            emoji_id = EMOJI_CROSS
            type_text = "Списание"
        else:
            emoji_id = EMOJI_INFO
            type_text = trans_type
        
        trans_list += f'<tg-emoji emoji-id="{emoji_id}">✅</tg-emoji> {idx}. {type_text}: {amount}₽\n   <tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> User: {user_id}... | <tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> {timestamp}\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Статистика:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Всего доход: {total_income}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Всего выдано: {total_outcome}₽\n'
        f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Всего списано: {total_taken}₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Последние 10 транзакций:</b>\n{trans_list}',
        
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Обновить', callback_data="admin_transactions", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text='Назад', callback_data="admin_finances", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()
    
    total_income = sum(t.get("amount", 0) for t in transactions if t.get("type") == "payment")
    total_outcome = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_give")
    total_taken = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_take")
    
    trans_list = ""
    for idx, trans in enumerate(reversed(transactions[-10:]), 1):
        trans_type = trans.get("type", "unknown")
        amount = trans.get("amount", 0)
        user_id = str(trans.get("user_id", "unknown"))[:8]
        timestamp = trans.get("timestamp", "").replace("T", " ")[:16]
        
        if trans_type == "payment":
            emoji_id = EMOJI_CHECK
            type_text = "Оплата"
        elif trans_type == "admin_give":
            emoji_id = EMOJI_MONEY
            type_text = "Выдача"
        elif trans_type == "admin_take":
            emoji_id = EMOJI_CROSS
            type_text = "Списание"
        else:
            emoji_id = EMOJI_INFO
            type_text = trans_type
        
        trans_list += f'<tg-emoji emoji-id="{emoji_id}">✅</tg-emoji> {idx}. {type_text}: {amount}₽\n   <tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> User: {user_id}... | <tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> {timestamp}\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Статистика:</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Всего доход: {total_income}₽\n'
        f'• <tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Всего выдано: {total_outcome}₽\n'
        f'• <tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Всего списано: {total_taken}₽\n\n'
        
        f'<b><tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Последние 10 транзакций:</b>\n{trans_list}',
        
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Обновить',
                callback_data="admin_transactions",
                icon_custom_emoji_id=EMOJI_STATS
            )],
            [InlineKeyboardButton(
                text='Назад',
                callback_data="admin_finances",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await callback.answer()

# === ЗАБЛОКИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ ===
@dp.callback_query(F.data == "admin_list_blocked")
async def admin_list_blocked_users(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    users = db.get("users", {})
    
    blocked = [(uid, udata) for uid, udata in users.items() if udata.get("blocked", False)]
    
    users_list = ""
    for idx, (user_id, user_data) in enumerate(blocked[:10], 1):
        name = user_data.get("first_name", "Нет имени")
        users_list += f'{idx}. {name}\n   ID: <code>{user_id}</code>\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">🚫</tg-emoji> Заблокированные пользователи</b>\n\n'
        f'Всего: {len(blocked)}\n'
        f'Показано: {min(len(blocked), 10)}\n\n{users_list if users_list else "Нет заблокированных"}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Заблокировать пользователя", callback_data="admin_block_user")],
            [InlineKeyboardButton(text="✅ Разблокировать пользователя", callback_data="admin_unblock_user")],
            [InlineKeyboardButton(text="◁ Назад", callback_data="admin_users_manage")]
        ])
    )
    await callback.answer()


    
@dp.callback_query(F.data == "admin_transactions")
async def admin_transactions(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    
    db = load_db()
    transactions = db.get("transactions", [])
    
    if not transactions:
        await callback.message.edit_text(
            f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
            f'Транзакций пока нет.',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text='Назад',
                    callback_data="admin_finances",
                    icon_custom_emoji_id=EMOJI_BACK
                )]
            ])
        )
        await callback.answer()
        return
    
    # Статистика
    total_income = sum(t.get("amount", 0) for t in transactions if t.get("type") == "payment")
    total_outcome = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_give")
    total_taken = sum(t.get("amount", 0) for t in transactions if t.get("type") == "admin_take")
    
    # Последние 10 транзакций
    trans_list = ""
    for idx, trans in enumerate(reversed(transactions[-10:]), 1):
        trans_type = trans.get("type", "unknown")
        amount = trans.get("amount", 0)
        user_id = str(trans.get("user_id", "unknown"))[:8]
        timestamp = trans.get("timestamp", "").replace("T", " ")[:16]
        
        if trans_type == "payment":
            emoji = "✅"
            type_text = "Оплата"
        elif trans_type == "admin_give":
            emoji = "💰"
            type_text = "Выдача"
        elif trans_type == "admin_take":
            emoji = "❌"
            type_text = "Списание"
        else:
            emoji = "•"
            type_text = trans_type
        
        trans_list += f'{emoji} {idx}. {type_text}: {amount}₽\n   User: {user_id}... | {timestamp}\n\n'
    
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
        
        f'<b>Статистика:</b>\n'
        f'• <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Всего доход: {total_income}₽\n'
        f'• <tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Всего выдано: {total_outcome}₽\n'
        f'• <tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Всего списано: {total_taken}₽\n\n'
        
        f'<b>Последние 10 транзакций:</b>\n{trans_list}',
        
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Обновить',
                callback_data="admin_transactions",
                icon_custom_emoji_id=EMOJI_STATS
            )],
            [InlineKeyboardButton(
                text='Назад',
                callback_data="admin_finances",
                icon_custom_emoji_id=EMOJI_BACK
            )]
        ])
    )
    await callback.answer()

# ===== ФОНОВЫЕ ЗАДАЧИ =====
# ===== БЛОКИРОВКА / РАЗБЛОКИРОВКА ПОЛЬЗОВАТЕЛЕЙ =====

@dp.callback_query(F.data == "admin_block_user")
async def admin_block_user_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Блокировка пользователя</b>\n\n'
        f'Введите ID пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_list_blocked", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.update_data(block_action="block")
    await state.set_state(AdminBlockStates.waiting_user_id)
    await callback.answer()


@dp.callback_query(F.data == "admin_unblock_user")
async def admin_unblock_user_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Разблокировка пользователя</b>\n\n'
        f'Введите ID пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_list_blocked", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.update_data(block_action="unblock")
    await state.set_state(AdminBlockStates.waiting_user_id)
    await callback.answer()


@dp.message(AdminBlockStates.waiting_user_id)
async def admin_block_unblock_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    user_id = message.text.strip()
    data = await state.get_data()
    action = data.get("block_action", "block")
    db = load_db()
    if user_id not in db["users"]:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь <code>{user_id}</code> не найден.',
            parse_mode=ParseMode.HTML
        )
        await state.clear()
        return
    if action == "block":
        db["users"][user_id]["blocked"] = True
        save_db(db)
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Заблокировал пользователя (список)',
            f'Target: <code>{user_id}</code>'
        )
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Вы были заблокированы администратором.</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Пользователь <code>{user_id}</code> заблокирован.</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='◁ К списку', callback_data="admin_list_blocked", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
    else:
        db["users"][user_id]["blocked"] = False
        db["users"][user_id].pop("ban_reason", None)
        save_db(db)
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Разблокировал пользователя (список)',
            f'Target: <code>{user_id}</code>'
        )
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Вы были разблокированы!</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Пользователь <code>{user_id}</code> разблокирован.</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='◁ К списку', callback_data="admin_list_blocked", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
    await state.clear()


# ===== ВЫДАЧА / ОТЗЫВ ПОДПИСКИ =====

@dp.callback_query(F.data == "admin_give_subscription")
async def admin_give_subscription_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выдача подписки</b>\n\n'
        f'Введите ID пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_give_key_user)
    await callback.answer()


@dp.message(AdminStates.waiting_give_key_user)
async def admin_give_subscription_get_id(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    user_id = message.text.strip()
    db = load_db()
    if user_id not in db["users"]:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь не найден.',
            parse_mode=ParseMode.HTML
        )
        return
    await state.update_data(target_user_id=user_id)
    await state.set_state(AdminStates.waiting_give_key_duration)
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Введите количество дней подписки:</b>',
        parse_mode=ParseMode.HTML
    )


@dp.message(AdminStates.waiting_give_key_duration)
async def admin_give_key_duration_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        days = int(message.text)
        if days <= 0:
            await message.answer("❌ Введите положительное число")
            return
        data = await state.get_data()
        user_id = data.get("target_user_id")
        db = load_db()
        if user_id not in db["users"]:
            await message.answer("❌ Пользователь не найден")
            await state.clear()
            return
        if "keys" not in db["users"][user_id]:
            db["users"][user_id]["keys"] = []
        key_entry = {
            "key": f"admin_key_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "tariff": "vpn_bypass",
            "active": True,
            "created_at": datetime.now().isoformat(),
            "expiry": (datetime.now() + timedelta(days=days)).isoformat(),
            "given_by_admin": True
        }
        db["users"][user_id]["keys"].append(key_entry)
        save_db(db)
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выдал ключ пользователю',
            f'Target: <code>{user_id}</code> | Дней: {days}'
        )
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Вам выдана подписка на {days} дней!</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Подписка выдана на {days} дней!\n\nПользователь: <code>{user_id}</code></b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
                [InlineKeyboardButton(text='◁ Назад', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите целое число")


@dp.callback_query(F.data == "admin_revoke_subscription")
async def admin_revoke_subscription_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Отзыв подписки</b>\n\n'
        f'Введите ID пользователя:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_revoke_key_user)
    await callback.answer()


@dp.message(AdminStates.waiting_revoke_key_user)
async def admin_revoke_subscription_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    user_id = message.text.strip()
    db = load_db()
    if user_id not in db["users"]:
        await message.answer(
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Пользователь не найден.',
            parse_mode=ParseMode.HTML
        )
        await state.clear()
        return
    keys = db["users"][user_id].get("keys", [])
    revoked = 0
    for k in keys:
        if k.get("active"):
            k["active"] = False
            revoked += 1
    save_db(db)
    await log_action(
        message.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Отозвал подписку у пользователя',
        f'Target: <code>{user_id}</code> | Отозвано ключей: {revoked}'
    )
    try:
        await bot.send_message(
            int(user_id),
            f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ваши ключи были отозваны администратором.</b>',
            parse_mode=ParseMode.HTML
        )
    except:
        pass
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Отозвано ключей: {revoked}\n\n'
        f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Пользователь: <code>{user_id}</code></b>',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
            [InlineKeyboardButton(text='◁ Назад', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await state.clear()


@dp.callback_query(F.data == "admin_list_subscribed")
async def admin_list_subscribed(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    db = load_db()
    users = db.get("users", {})
    subscribed_users = [
        (uid, udata) for uid, udata in users.items()
        if any(k.get("active") for k in udata.get("keys", []))
    ]
    users_list = ""
    for idx, (uid, udata) in enumerate(subscribed_users[:15], 1):
        name = udata.get("first_name", "Нет имени")
        username = udata.get("username", "")
        active_keys = sum(1 for k in udata.get("keys", []) if k.get("active"))
        users_list += f'{idx}. {name} (@{username})\n   <code>{uid}</code> | ключей: {active_keys}\n\n'
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Пользователи с активными ключами</b>\n\n'
        f'Всего: {len(subscribed_users)}\n\n{users_list if users_list else "Нет активных подписок"}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Назад', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


# ===== ДЕЙСТВИЯ С ПРОФИЛЕМ ПОЛЬЗОВАТЕЛЯ =====

@dp.callback_query(F.data.startswith("admin_user_take_balance_"))
async def admin_user_take_balance_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_take_balance_", "")
    db = load_db()
    balance = db["users"].get(user_id, {}).get("balance", 0)
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списание баланса</b>\n\n'
        f'ID: <code>{user_id}</code>\n'
        f'Текущий баланс: <b>{balance}₽</b>\n\n'
        f'Введите сумму для списания:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_take_balance_amount)
    await callback.answer()


@dp.message(AdminStates.waiting_take_balance_amount)
async def admin_user_take_balance_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer("❌ Сумма должна быть больше 0")
            return
        data = await state.get_data()
        user_id = data.get("target_user_id")
        db = load_db()
        old_balance = db["users"][user_id].get("balance", 0)
        new_balance = max(0, old_balance - amount)
        db["users"][user_id]["balance"] = new_balance
        if "transactions" not in db:
            db["transactions"] = []
        db["transactions"].append({
            "type": "admin_take",
            "user_id": user_id,
            "amount": amount,
            "admin_id": message.from_user.id,
            "timestamp": datetime.now().isoformat()
        })
        save_db(db)
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Администратор списал {amount}₽.</b>\nНовый баланс: {new_balance}₽',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списал баланс у пользователя',
            f'Target: <code>{user_id}</code> | -{amount}₽ | Было: {old_balance}₽ → Стало: {new_balance}₽'
        )
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Баланс списан!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Пользователь: <code>{user_id}</code>\n'
            f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Списано: <b>-{amount}₽</b>\n'
            f'<tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> Было: {old_balance}₽ → Стало: <b>{new_balance}₽</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
                [InlineKeyboardButton(text='◁ Финансы', callback_data="admin_finances", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите число")


@dp.callback_query(F.data.startswith("admin_user_give_key_"))
async def admin_user_give_key_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_give_key_", "")
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Выдача ключа</b>\n\n'
        f'ID: <code>{user_id}</code>\n\n'
        f'Введите количество дней:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_give_key_duration)
    await callback.answer()


@dp.callback_query(F.data.startswith("admin_user_revoke_key_"))
async def admin_user_revoke_key(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_revoke_key_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    keys = db["users"][user_id].get("keys", [])
    revoked = 0
    for k in keys:
        if k.get("active"):
            k["active"] = False
            revoked += 1
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Отозвал ключи у пользователя',
        f'Target ID: <code>{user_id}</code> | Отозвано: {revoked}'
    )
    if revoked > 0:
        try:
            await bot.send_message(
                int(user_id),
                f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ваши ключи были отозваны администратором.</b>',
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        await callback.answer(f"✅ Отозвано {revoked} ключей")
    else:
        await callback.answer("ℹ️ Активных ключей нет")
    user_data = db["users"].get(user_id, {})
    await show_user_profile(callback, user_id, user_data)


@dp.callback_query(F.data.startswith("admin_user_extend_"))
async def admin_user_extend_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_extend_", "")
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Продление подписки</b>\n\n'
        f'ID: <code>{user_id}</code>\n\nВведите количество дней:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_extend_days)
    await callback.answer()


@dp.message(AdminStates.waiting_extend_days)
async def admin_user_extend_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        days = int(message.text)
        if days <= 0:
            await message.answer("❌ Введите положительное число")
            return
        data = await state.get_data()
        user_id = data.get("target_user_id")
        db = load_db()
        keys = db["users"][user_id].get("keys", [])
        changed = 0
        for k in keys:
            if k.get("active"):
                if k.get("expiry"):
                    current = datetime.fromisoformat(k["expiry"])
                    base = max(current, datetime.now())
                else:
                    base = datetime.now()
                k["expiry"] = (base + timedelta(days=days)).isoformat()
                changed += 1
        save_db(db)
        await log_action(
            message.from_user.id,
            f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Продлил подписку пользователю',
            f'Target: <code>{user_id}</code> | +{days} дней | Изменено ключей: {changed}'
        )
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Продлено на {days} дней!</b>\n\n'
            f'<tg-emoji emoji-id="{EMOJI_PROFILE}">👤</tg-emoji> Пользователь: <code>{user_id}</code>\n'
            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Изменено ключей: <b>{changed}</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
                [InlineKeyboardButton(text='◁ Назад', callback_data="admin_subscriptions", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите целое число")


@dp.callback_query(F.data.startswith("admin_user_cancel_sub_"))
async def admin_user_cancel_sub(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_cancel_sub_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    revoked = 0
    for k in db["users"][user_id].get("keys", []):
        if k.get("active"):
            k["active"] = False
            revoked += 1
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Отменил подписку пользователю',
        f'Target ID: <code>{user_id}</code> | Отозвано ключей: {revoked}'
    )
    try:
        await bot.send_message(
            int(user_id),
            f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ваша подписка отменена администратором.</b>',
            parse_mode=ParseMode.HTML
        )
    except:
        pass
    await callback.answer(f"✅ Отменено {revoked} ключей")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_ban_"))
async def admin_user_ban_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_ban_", "")
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Блокировка</b>\n\n'
        f'ID: <code>{user_id}</code>\n\nВведите причину (или "-" чтобы пропустить):',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_ban_reason)
    await callback.answer()


@dp.message(AdminStates.waiting_ban_reason)
async def admin_user_ban_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    data = await state.get_data()
    user_id = data.get("target_user_id")
    reason = message.text if message.text != "-" else "Без причины"
    db = load_db()
    if user_id not in db["users"]:
        await message.answer("❌ Пользователь не найден")
        await state.clear()
        return
    db["users"][user_id]["blocked"] = True
    db["users"][user_id]["ban_reason"] = reason
    db["users"][user_id]["banned_at"] = datetime.now().isoformat()
    save_db(db)
    await log_action(
        message.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Заблокировал пользователя',
        f'Target: <code>{user_id}</code> | Причина: {reason}'
    )
    try:
        await bot.send_message(
            int(user_id),
            f'<b><tg-emoji emoji-id="{EMOJI_CANCEL}">🚫</tg-emoji> Вы заблокированы.</b>\n\nПричина: {reason}',
            parse_mode=ParseMode.HTML
        )
    except:
        pass
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Пользователь <code>{user_id}</code> заблокирован.</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Причина: {reason}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)],
            [InlineKeyboardButton(text='◁ Список заблок.', callback_data="admin_list_blocked", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await state.clear()


@dp.callback_query(F.data.startswith("admin_user_unban_"))
async def admin_user_unban(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_unban_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["blocked"] = False
    db["users"][user_id].pop("ban_reason", None)
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Разблокировал пользователя',
        f'Target ID: <code>{user_id}</code>'
    )
    try:
        await bot.send_message(
            int(user_id),
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Вы были разблокированы!</b>',
            parse_mode=ParseMode.HTML
        )
    except:
        pass
    await callback.answer("✅ Разблокирован")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_reset_trial_"))
async def admin_user_reset_trial(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_reset_trial_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["trial_used"] = False
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji> Сбросил триал пользователю',
        f'Target ID: <code>{user_id}</code>'
    )
    await callback.answer("✅ Тестовый период сброшен")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_set_vip_"))
async def admin_user_set_vip(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_set_vip_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["vip"] = True
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji> Выдал VIP пользователю',
        f'Target ID: <code>{user_id}</code>'
    )
    try:
        await bot.send_message(
            int(user_id),
            f'<b><tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji> Вам выдан VIP статус!</b>',
            parse_mode=ParseMode.HTML
        )
    except:
        pass
    await callback.answer("✅ VIP выдан")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_remove_vip_"))
async def admin_user_remove_vip(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_remove_vip_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["vip"] = False
    save_db(db)
    await callback.answer("✅ VIP снят")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_freeze_"))
async def admin_user_freeze(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_freeze_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["balance_frozen"] = True
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_SNOW}">❄️</tg-emoji> Заморозил баланс пользователя',
        f'Target ID: <code>{user_id}</code>'
    )
    await callback.answer("✅ Баланс заморожен")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_unfreeze_"))
async def admin_user_unfreeze(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_unfreeze_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    db["users"][user_id]["balance_frozen"] = False
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_FIRE}">🔥</tg-emoji> Разморозил баланс пользователя',
        f'Target ID: <code>{user_id}</code>'
    )
    await callback.answer("✅ Баланс разморожен")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


@dp.callback_query(F.data.startswith("admin_user_history_"))
async def admin_user_history(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_history_", "")
    db = load_db()
    transactions = [t for t in db.get("transactions", []) if str(t.get("user_id", "")) == user_id]
    transactions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    if not transactions:
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\n'
            f'Пользователь: <code>{user_id}</code>\n\nНет транзакций.'
        )
    else:
        text = f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📊</tg-emoji> История транзакций</b>\n\nПользователь: <code>{user_id}</code>\n\n'
        for t in transactions[:10]:
            t_type = t.get("type", "")
            amount = t.get("amount", 0)
            ts = t.get("timestamp", "").replace("T", " ")[:16]
            text += f'• {t_type}: <b>{amount}₽</b> | {ts}\n'

    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("admin_user_keys_"))
async def admin_user_keys(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_keys_", "")
    db = load_db()
    keys = db["users"].get(user_id, {}).get("keys", [])
    active_keys = [k for k in keys if k.get("active")]

    if not active_keys:
        text = (
            f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Активные ключи</b>\n\n'
            f'Пользователь: <code>{user_id}</code>\n\nАктивных ключей нет.'
        )
    else:
        text = f'<b><tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Активные ключи</b>\n\nПользователь: <code>{user_id}</code>\n\n'
        for idx, k in enumerate(active_keys, 1):
            expiry = k.get("expiry", "")[:10] if k.get("expiry") else "Бессрочно"
            tariff = k.get("tariff", "Нет")
            text += f'{idx}. Тариф: <b>{tariff}</b>\n   Срок до: {expiry}\n\n'

    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("admin_user_delete_"))
async def admin_user_delete_confirm(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    # avoid conflict with admin_user_delete_confirm_ prefix
    raw = callback.data.replace("admin_user_delete_", "")
    if raw.startswith("confirm_"):
        user_id = raw.replace("confirm_", "")
        db = load_db()
        if user_id in db["users"]:
            del db["users"][user_id]
            save_db(db)
            await callback.message.edit_text(
                f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Пользователь <code>{user_id}</code> удалён.</b>',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='◁ К списку', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)]
                ])
            )
        else:
            await callback.answer("❌ Пользователь не найден", show_alert=True)
        await callback.answer()
        return
    user_id = raw
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Удаление пользователя</b>\n\n'
        f'ID: <code>{user_id}</code>\n\n'
        f'⚠️ Действие необратимо! Вы уверены?',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Да, удалить', callback_data=f"admin_user_delete_confirm_{user_id}", icon_custom_emoji_id=EMOJI_CHECK)],
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("admin_user_note_"))
async def admin_user_note_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_note_", "")
    db = load_db()
    existing = db["users"].get(user_id, {}).get("note", "Нет заметки")
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_FILE}">📋</tg-emoji> Заметка</b>\n\n'
        f'ID: <code>{user_id}</code>\n'
        f'Текущая: {existing}\n\n'
        f'Введите новую заметку:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_note_text)
    await callback.answer()


@dp.message(AdminStates.waiting_note_text)
async def admin_user_note_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    data = await state.get_data()
    user_id = data.get("target_user_id")
    db = load_db()
    if user_id in db["users"]:
        db["users"][user_id]["note"] = message.text
        save_db(db)
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Заметка сохранена!</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)]
        ])
    )
    await state.clear()


@dp.callback_query(F.data.startswith("admin_user_export_"))
async def admin_user_export(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    from aiogram.types import BufferedInputFile
    user_id = callback.data.replace("admin_user_export_", "")
    db = load_db()
    user_data = db["users"].get(user_id)
    if not user_data:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    export_text = json.dumps(user_data, ensure_ascii=False, indent=2)
    await callback.message.answer_document(
        document=BufferedInputFile(export_text.encode("utf-8"), filename=f"user_{user_id}.json"),
        caption=f'<b><tg-emoji emoji-id="{EMOJI_DOWNLOAD}">⬇️</tg-emoji> Данные пользователя <code>{user_id}</code></b>',
        parse_mode=ParseMode.HTML
    )
    await callback.answer("✅ Данные экспортированы")


@dp.callback_query(F.data.startswith("admin_user_change_expiry_"))
async def admin_user_change_expiry_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_change_expiry_", "")
    db = load_db()
    active_keys = [k for k in db["users"].get(user_id, {}).get("keys", []) if k.get("active")]
    if not active_keys:
        await callback.answer("❌ Нет активных ключей", show_alert=True)
        return
    await state.update_data(target_user_id=user_id)
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> Изменить срок ключа</b>\n\n'
        f'ID: <code>{user_id}</code>\n\n'
        f'Введите дату в формате <b>ГГГГ-ММ-ДД</b>\nПример: 2025-12-31',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_change_expiry_date)
    await callback.answer()


@dp.message(AdminStates.waiting_change_expiry_date)
async def admin_user_change_expiry_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    data = await state.get_data()
    user_id = data.get("target_user_id")
    try:
        new_date = datetime.strptime(message.text.strip(), "%Y-%m-%d")
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте ГГГГ-ММ-ДД")
        return
    db = load_db()
    changed = 0
    for k in db["users"][user_id].get("keys", []):
        if k.get("active"):
            k["expiry"] = new_date.isoformat()
            changed += 1
    save_db(db)
    await message.answer(
        f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Срок изменён!</b>\n\nИзменено ключей: {changed}\nНовая дата: {message.text.strip()}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='К профилю', callback_data=f"admin_select_user_{user_id}", icon_custom_emoji_id=EMOJI_PROFILE)]
        ])
    )
    await state.clear()


@dp.callback_query(F.data.startswith("admin_user_reset_refs_"))
async def admin_user_reset_refs(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    user_id = callback.data.replace("admin_user_reset_refs_", "")
    db = load_db()
    if user_id not in db["users"]:
        await callback.answer("❌ Пользователь не найден", show_alert=True)
        return
    old_count = len(db["users"][user_id].get("referrals", []))
    db["users"][user_id]["referrals"] = []
    save_db(db)
    await log_action(
        callback.from_user.id,
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Сбросил рефералов пользователю',
        f'Target ID: <code>{user_id}</code> | Было рефералов: {old_count}'
    )
    await callback.answer("✅ Рефералы сброшены")
    await show_user_profile(callback, user_id, db["users"].get(user_id, {}))


# ===== МАССОВАЯ ВЫДАЧА БАЛАНСА =====

@dp.callback_query(F.data == "admin_mass_give_balance")
async def admin_mass_give_balance_start(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    db = load_db()
    users_count = len(db.get("users", {}))
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Массовая выдача баланса</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Будет начислено всем <b>{users_count}</b> пользователям.\n\n'
        f'Введите сумму для начисления каждому:',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Отмена', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_CANCEL)]
        ])
    )
    await state.set_state(AdminStates.waiting_mass_balance_amount)
    await callback.answer()


@dp.message(AdminStates.waiting_mass_balance_amount)
async def admin_mass_give_balance_process(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer("❌ Сумма должна быть больше 0")
            return
        db = load_db()
        users = db.get("users", {})
        success = 0
        for user_id in users:
            db["users"][user_id]["balance"] = db["users"][user_id].get("balance", 0) + amount
            success += 1
            try:
                await bot.send_message(
                    int(user_id),
                    f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Вам начислено {amount}₽ от администратора!</b>',
                    parse_mode=ParseMode.HTML
                )
            except:
                pass
        save_db(db)
        await message.answer(
            f'<b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> Начислено {amount}₽ для {success} пользователей!</b>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='◁ Назад', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)]
            ])
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите число")


# ===== СЕРВЕРЫ И НАСТРОЙКИ =====

@dp.callback_query(F.data == "admin_check_servers")
async def admin_check_servers(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_STATS}">📈</tg-emoji> Статус серверов</b>\n\n'
        f'🇫🇮 Финляндия — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇩🇪 Германия — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇵🇱 Польша — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇺🇸 США — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇳🇱 Нидерланды — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>\n'
        f'🇷🇺 Обход — <b><tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji> ONLINE</b>',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔄 Обновить', callback_data="admin_check_servers", icon_custom_emoji_id=EMOJI_STATS)],
            [InlineKeyboardButton(text='◁ Назад', callback_data="admin_servers", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data.in_({"admin_server_config", "admin_server_settings"}))
async def admin_server_config(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_PC}">🖥</tg-emoji> Настройки серверов</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Управление серверами через панель.\n\n'
        f'Здесь в будущем будет управление IP-адресами, портами и конфигурациями серверов.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Назад', callback_data="admin_servers", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data == "admin_price_settings")
async def admin_price_settings(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    prices = TARIFFS.get("vpn_bypass", {}).get("prices", {})
    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Настройки цен</b>\n\n'
        f'<b>Тариф VPN+Обход:</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> 1 день: <b>{prices.get("days", 10)}₽</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> 1 месяц: <b>{prices.get("months", 99)}₽</b>\n'
        f'<tg-emoji emoji-id="{EMOJI_CALENDAR}">📅</tg-emoji> 1 год: <b>{prices.get("years", 990)}₽</b>\n\n'
        f'<tg-emoji emoji-id="{EMOJI_INFO}">ℹ️</tg-emoji> Для изменения цен отредактируйте переменную TARIFFS в коде.',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='◁ Назад', callback_data="admin_settings", icon_custom_emoji_id=EMOJI_BACK)]
        ])
    )
    await callback.answer()


# ===== ПАГИНАЦИЯ ПОЛЬЗОВАТЕЛЕЙ =====

@dp.callback_query(F.data.startswith("admin_list_all_users_more"))
async def admin_list_all_users_more(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    raw = callback.data.replace("admin_list_all_users_more", "").strip("_")
    page = int(raw) if raw.isdigit() else 1
    per_page = 10
    offset = page * per_page

    db = load_db()
    users = list(db.get("users", {}).items())
    total = len(users)
    page_users = users[offset:offset + per_page]

    if not page_users:
        await callback.answer("Больше нет пользователей", show_alert=True)
        return

    users_list = ""
    for idx, (user_id, user_data) in enumerate(page_users, offset + 1):
        name = user_data.get("first_name", "Нет имени")
        username = user_data.get("username", "Нет")
        balance = user_data.get("balance", 0)
        sub = f'<tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>' if user_data.get("subscribed") else f'<tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji>'
        users_list += f'{idx}. {sub} {name} (@{username})\n   <code>{user_id}</code> | {balance}₽\n\n'

    nav_buttons = []
    if offset > 0:
        prev_page = page - 1
        nav_buttons.append(InlineKeyboardButton(text='← Назад', callback_data=f"admin_list_all_users_more_{prev_page}", icon_custom_emoji_id=EMOJI_BACK))
    if offset + per_page < total:
        nav_buttons.append(InlineKeyboardButton(text='Вперёд →', callback_data=f"admin_list_all_users_more_{page + 1}", icon_custom_emoji_id=EMOJI_DOWNLOAD))

    keyboard = []
    if nav_buttons:
        keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton(text='◁ В управление', callback_data="admin_users_manage", icon_custom_emoji_id=EMOJI_BACK)])

    await callback.message.edit_text(
        f'<b><tg-emoji emoji-id="{EMOJI_PEOPLE}">👥</tg-emoji> Список пользователей</b>\n\n'
        f'Всего: {total} | Страница {page + 1}\n\n{users_list}',
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
    await callback.answer()
    
async def hourly_billing():
    """Каждый час списывает 1.2₽ у всех пользователей с балансом > 0"""
    while True:
        await asyncio.sleep(3600)  # ждём 1 час
        try:
            db = load_db()
            changed = False
            
            for user_id, user_data in db["users"].items():
                balance = user_data.get("balance", 0)
                if balance <= 0:
                    continue
                
                # Списываем 1.2₽
                new_balance = balance - 1.2
                if new_balance < 0:
                    new_balance = 0
                    
                db["users"][user_id]["balance"] = new_balance
                changed = True
                
                # Если баланс стал 0 - уведомление
                if new_balance == 0 and balance > 0:
                    try:
                        await bot.send_message(
                            int(user_id),
                            f'<b><tg-emoji emoji-id="{EMOJI_CROSS}">❌</tg-emoji> Ваш баланс закончился</b>\n\n'
                            f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> Средства на балансе полностью израсходованы.\n\n'
                            f'<tg-emoji emoji-id="{EMOJI_KEY}">🔑</tg-emoji> Подписка приостановлена. Чтобы продолжить пользоваться VPN, пополните баланс.',
                            parse_mode=ParseMode.HTML,
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(
                                    text="Пополнить баланс",
                                    callback_data="add_balance",
                                    icon_custom_emoji_id=EMOJI_MONEY
                                )]
                            ])
                        )
                    except:
                        pass
                
                # Уведомление за 24 часа до окончания
                hours_left = new_balance / 1.2
                if 0 < hours_left <= 24:
                    last_notify = user_data.get("last_24h_notify")
                    if not last_notify:
                        try:
                            hours_int = int(hours_left)
                            if hours_int == 1:
                                time_text = "1 день"
                            elif 2 <= hours_int <= 4:
                                time_text = f"{hours_int} дня"
                            else:
                                time_text = f"{hours_int} дней"
                            
                            await bot.send_message(
                                int(user_id),
                                f'<b><tg-emoji emoji-id="{EMOJI_EXCLAMATION}">⚠️</tg-emoji> Внимание! Заканчивается баланс</b>\n\n'
                                f'<tg-emoji emoji-id="{EMOJI_MONEY}">💰</tg-emoji> На вашем балансе осталось примерно на <b>{time_text}</b>.\n\n'
                                f'<tg-emoji emoji-id="{EMOJI_WALLET}">👛</tg-emoji> Пополните баланс, чтобы продолжать пользоваться VPN без перерыва.',
                                parse_mode=ParseMode.HTML,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(
                                        text="Пополнить баланс",
                                        callback_data="add_balance",
                                        icon_custom_emoji_id=EMOJI_MONEY
                                    )]
                                ])
                            )
                            db["users"][user_id]["last_24h_notify"] = True
                            changed = True
                        except:
                            pass
            
            if changed:
                save_db(db)
                
        except Exception as e:
            print(f"Ошибка в hourly_billing: {e}")

async def daily_reminders():
    """Каждый день в 10:00 проверяет ключи, оставшиеся <= 3 дня."""
    while True:
        now = datetime.now()
        target = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        sleep_seconds = (target - now).total_seconds()
        await asyncio.sleep(sleep_seconds)
        
        try:
            db = load_db()
            changed = False
            for user_id, user_data in db["users"].items():
                keys = user_data.get("keys", [])
                for key in keys:
                    if key.get("active") and key.get("expiry"):
                        expiry = datetime.fromisoformat(key["expiry"])
                        days_left = (expiry - now).days
                        if 0 < days_left <= 3:
                            if not key.get("reminder_sent"):
                                try:
                                    await bot.send_message(
                                        int(user_id),
                                        f'<b>🔔 Ваша подписка скоро закончится</b>\n\n'
                                        f'Осталось {days_left} дня(ей).\n'
                                        f'Продлите подписку, чтобы не терять доступ.',
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                            [InlineKeyboardButton(text="💰 Продлить", callback_data="buy_key")]
                                        ])
                                    )
                                    key["reminder_sent"] = True
                                    changed = True
                                except:
                                    pass
            if changed:
                save_db(db)
        except Exception as e:
            print(f"Ошибка в daily_reminders: {e}")

async def daily_stats():
    """Каждый день в 23:59 отправляет админам статистику за день."""
    while True:
        now = datetime.now()
        target = now.replace(hour=23, minute=59, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        sleep_seconds = (target - now).total_seconds()
        await asyncio.sleep(sleep_seconds)
        
        try:
            db = load_db()
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            transactions = db.get("transactions", [])
            income = sum(t.get("amount", 0) for t in transactions if t.get("timestamp", "").startswith(yesterday) and t.get("type") == "payment")
            new_users = sum(1 for u in db["users"].values() if u.get("registered_at", "").startswith(yesterday))
            
            text = (
                f'<b>📊 Статистика за {yesterday}</b>\n\n'
                f'💰 Доход: {income}₽\n'
                f'👥 Новых пользователей: {new_users}'
            )
            for admin_id in ADMIN_IDS:
                try:
                    await bot.send_message(admin_id, text, parse_mode=ParseMode.HTML)
                except:
                    pass
        except Exception as e:
            print(f"Ошибка в daily_stats: {e}")

# ===== ФУНКЦИЯ MAIN =====
async def main():
    init_db()
    asyncio.create_task(hourly_billing())
    asyncio.create_task(daily_reminders())
    asyncio.create_task(daily_stats())
    print("Бот запущен!")
    await dp.start_polling(bot)

# ===== ЗАПУСК =====
if __name__ == "__main__":

    asyncio.run(main())

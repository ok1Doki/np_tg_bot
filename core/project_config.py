import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TELEGRAM_TOKEN = os.environ.get("telegram_token")
OPENAI_API_KEY = os.environ.get("openai_api_key")
OPENAI_API_BASE = os.environ.get("openai_api_base")

WELCOME_MESSAGE = '👩🏼‍🎓 Привіт, я <b>Розумний помічник</b>. Як я можу тобі допомогти?'
PROMPT_START = '''Як вдосконалений чат-бот Асистент, вашою основною метою є надання клієнтам Нової Пошти допомоги 
наскільки це можливо. Це може включати відповіді на запитання, надання корисної інформації або виконання завдань на 
основі введених користувачем даних. Щоб ефективно допомагати користувачам, важливо давати докладні та ретельні 
відповіді. Використовуйте приклади та докази для підтримки своїх тверджень і обґрунтування рекомендацій чи рішень. 
Завжди пам'ятайте про пріоритети потреб та задоволення користувача. Вашою основною метою є надання корисного та 
приємного досвіду користувачеві.'''


def setup_openai_config():
    import openai
    openai.api_key = OPENAI_API_KEY
    openai.organization = os.getenv('OPENAI_ORG_ID')
    logging.error(OPENAI_API_BASE is not None and OPENAI_API_BASE != "")
    if OPENAI_API_BASE is not None and OPENAI_API_BASE != "":
        openai.api_base = OPENAI_API_BASE


def setup_app_config():
    load_dotenv()
    setup_openai_config()

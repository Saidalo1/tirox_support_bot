from re import match

from config import default_language
from models import session, UserLanguage
from translations import translators


def get_user_language(user_id):
    user = session.query(UserLanguage).filter_by(chat_id=user_id).first()
    if user is None:
        user = UserLanguage(user_id, default_language)
        session.add(user)
        session.commit()
    return user.language


def update_user_language(user_id, language):
    user = session.query(UserLanguage).filter_by(chat_id=user_id).first()
    if user is None:
        user = UserLanguage(user_id, language)
        session.add(user)
        session.commit()
    else:
        if user.language != language:
            user.language = language
            session.commit()
    return user.language


def get_translate(language, phrase):
    return translators[language if language else default_language].gettext(phrase)


def is_valid_name(name):
    if len(name) < 3 or len(name) > 30 or not match(r'^[a-zA-Zа-яА-ЯёЁ]+$', name):
        return False
    return True


def information_message(user_full_name, user_phone_number, message_text):
    return f' ✨ Новое сообщение ✨\n' \
           f'👤 Имя: {user_full_name} \n' \
           f'📞 Контакт: {user_phone_number} \n' \
           f'💬 Сообщение: {message_text} \n'

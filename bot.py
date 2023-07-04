from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes
from aiogram.utils import executor

from config import languages, lang_values, dp
from fsm_contexts import BotStates
from handlers import start, select_language, incorrect_select_language, consultation, got_name, incorrect_got_name, \
    got_contact, got_message, back_to_main_menu, \
    start_in_state, about_us
from utils import get_translate, is_valid_name

# Add LifetimeControllerMiddleware to ensure the storage is cleared correctly on restart
dp.middleware.setup(LoggingMiddleware())

# Register the handlers
dp.register_message_handler(start, commands='start')

# Start in state
dp.register_message_handler(start_in_state, commands='start', state='*')

# Selected language
dp.register_message_handler(select_language, lambda message: message.text in languages,
                            content_types=ContentTypes.TEXT, state=BotStates.choose_language)
dp.register_message_handler(incorrect_select_language, state=BotStates.choose_language)

dp.register_message_handler(back_to_main_menu,
                            lambda message: message.text in (get_translate(language, 'BACK') for language in
                                                             lang_values), state='*')
# Selected category
dp.register_message_handler(consultation,
                            lambda message: message.text in (get_translate(language, 'CONSULT') for language in
                                                             lang_values),
                            content_types=ContentTypes.TEXT, state=BotStates.choose_category)
# Selected category
dp.register_message_handler(about_us,
                            lambda message: message.text in (get_translate(language, 'ABOUT_US_BUTTON') for language in
                                                             lang_values),
                            content_types=ContentTypes.TEXT, state=BotStates.choose_category)

# Got name
dp.register_message_handler(got_name, lambda message: is_valid_name(message.text), content_types=ContentTypes.TEXT,
                            state=BotStates.send_name)
dp.register_message_handler(incorrect_got_name, content_types=ContentTypes.TEXT, state=BotStates.send_name)

# Got Contact
dp.register_message_handler(got_contact, content_types=ContentTypes.CONTACT, state=BotStates.send_phone)
# dp.register_message_handler(incorrect_got_contact, content_types=ContentTypes.TEXT, state=BotStates.send_name)

# Got Address
dp.register_message_handler(got_message, content_types=ContentTypes.TEXT, state=BotStates.send_address)
# dp.register_message_handler(incorrect_got_contact, content_types=ContentTypes.TEXT, state=BotStates.send_name)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

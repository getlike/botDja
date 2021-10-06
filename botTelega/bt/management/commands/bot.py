from django.core.management.base import BaseCommand

from django.conf import settings

from telegram import Bot, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater
from telegram.utils.request import Request

from bt.models import Message, Profile


def lod_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:

            error_message = f'Произошла ошибка:{e}'
            print(error_message)
            raise e
    return inner


@lod_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id = chat_id,
        defaults = {
            'name':update.message.from_user.username,
        }

    )
    Message(
        profile=p,
        text=text,
    ).save()

    reply_text = "Ваш ID = {}\n\n{}".format(chat_id, text)
    update.message.reply_text(
        text=reply_text
    )


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        # 1 -- правильное подключени
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            # base_url=settings.PROXY_URL,
        )
        print(bot.get_me())

        # 2 - обработчики
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        #3 - запустить бесконечную обработку
        updater.start_polling()
        updater.idle()

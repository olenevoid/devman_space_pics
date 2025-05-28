from os import makedirs, environ
from dotenv import load_dotenv
from helpers import IMAGE_FOLDER_NAME
from fetch_spacex_images import fetch_spacex_images
import nasa
import telegram


def init_bot(token: str) -> telegram.Bot:
    bot = telegram.Bot(token)
    return bot


def test_load_images(nasa_api_key):
    fetch_spacex_images('605b4b95aa5433645e37d041')
    nasa.fetch_apod_images(nasa_api_key, 3)
    nasa.fetch_epic_images(nasa_api_key, 3)


def send_message_to_channel(bot, channel_id):
    bot.send_message(chat_id=channel_id, text='hello, world')


def main():
    makedirs(IMAGE_FOLDER_NAME, exist_ok=True)

    load_dotenv()

    nasa_api_key = environ['NASA_API_KEY']
    tg_bot_token = environ['TG_BOT_TOKEN']
    tg_channel_id = environ['TG_CHANNEL_ID']

    bot = init_bot(tg_bot_token)

    send_message_to_channel(bot, tg_channel_id)


if __name__ == '__main__':
    main()

from image_helpers import get_all_images
from time import sleep
from argparse import ArgumentParser
import random
from dotenv import load_dotenv
from os import getenv, environ
from telegram_bot import send_image


DEFAULT_DELAY = 240


def post_images(images, tg_bot_token, tg_channel_id, delay=DEFAULT_DELAY):
    for image in images:
        print(f'Публикация изображения {image}')
        send_image(tg_bot_token, tg_channel_id, image)
        print(f'Ожидание {delay} минут')
        sleep(delay*60)


def main():
    load_dotenv()
    tg_bot_token = environ['TG_BOT_TOKEN']
    tg_channel_id = environ['TG_CHANNEL_ID']

    delay = getenv('POSTING_DELAY', default=DEFAULT_DELAY)

    parser = ArgumentParser(
        description='Публикует изображения в бесконечном цикле'
    )

    parser.add_argument(
        '-d',
        '--delay',
        help='Задержка в минутах. По умолчанию 240 (4 часа)'
    )

    args = parser.parse_args()

    while True:
        images = get_all_images()
        random.shuffle(images)
        if args.delay:
            post_images(images, tg_bot_token, tg_channel_id, args.delay)
        else:
            post_images(images, tg_bot_token, tg_channel_id, delay)


if __name__ == '__main__':
    main()

from argparse import ArgumentParser
from image_helpers import get_all_images
from telegram_bot import send_image
import random
from os import environ
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_bot_token = environ['TG_BOT_TOKEN']
    tg_channel_id = environ['TG_CHANNEL_ID']

    parser = ArgumentParser(
        description=(
            'Публикует указанное изображение. Если не использованы '
            'аргументы, публикует случайное изображение.'
        )
    )
    parser.add_argument(
        '-i',
        '--image',
        help=' Путь к изображению для публикации',
        default=random.choice(get_all_images())
    )

    args = parser.parse_args()

    send_image(tg_bot_token, tg_channel_id, args.image)

    print('Изображение опубликовано')


if __name__ == '__main__':
    main()

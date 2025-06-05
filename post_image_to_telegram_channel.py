from argparse import ArgumentParser
from image_helpers import get_all_images
from telegram_bot import send_image
import random
from os import environ
from dotenv import load_dotenv


def post_image(image_path: str):
    bot = ImagePosterBot()
    bot.send_image(image_path)


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
        help=' Путь к изображению для публикации'
    )

    args = parser.parse_args()

    if args.image:
        send_image(tg_bot_token, tg_channel_id, args.image)
    else:
        image_path = random.choice(get_all_images())
        send_image(tg_bot_token, tg_channel_id, image_path)

    print('Изображение опубликовано')


if __name__ == '__main__':
    main()

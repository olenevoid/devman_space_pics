from argparse import ArgumentParser
from image_helpers import get_all_images
from telegram_bot import ImagePosterBot
import random


def post_random_image():
    image_path = random.choice(get_all_images())
    post_image(image_path)


def post_image(image_path: str):
    bot = ImagePosterBot()
    bot.send_image(image_path)


def main():
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
        post_image(args.image)
    else:
        post_random_image()

    print('Изображение опубликовано')


if __name__ == '__main__':
    main()

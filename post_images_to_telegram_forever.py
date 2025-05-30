from post_image_to_telegram_channel import post_image
from image_helpers import get_all_images
from time import sleep
from argparse import ArgumentParser
import random
from dotenv import load_dotenv
from os import getenv


DEFAULT_DELAY = 240


def post_images(images, delay = DEFAULT_DELAY):
    for image in images:
        print(f'Публикация изображения {image}')
        post_image(image)
        print(f'Ожидание {delay} минут')
        sleep(delay*60)


def get_delay():
    delay = getenv('POSTING_DELAY')
    if delay:
        return int(delay)
    return DEFAULT_DELAY


def main():
    load_dotenv()

    delay = get_delay()

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
            post_images(images, args.delay)
        else:
            post_images(images, delay)
        


if __name__ == '__main__':
    main()

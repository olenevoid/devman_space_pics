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
    post_random_image()


if __name__ == '__main__':
    main()

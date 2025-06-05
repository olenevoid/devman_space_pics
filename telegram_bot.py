from os import environ
from dotenv import load_dotenv
from telegram import Bot


class ImagePosterBot():
    def __init__(self):
        load_dotenv()
        self.tg_bot_token = environ['TG_BOT_TOKEN']
        self.tg_channel_id = environ['TG_CHANNEL_ID']
        self.bot = Bot(self.tg_bot_token)

    def send_image(self, image_path):
        image = open(image_path, 'rb')
        self.bot.send_photo(chat_id=self.tg_channel_id, photo=image)


def send_image(tg_bot_token, tg_channel_id, image_path):
    bot = Bot(tg_bot_token)

    with open(image_path, 'rb') as image:
        bot.send_photo(tg_channel_id, image)


def main():
    bot = ImagePosterBot().bot
    print(bot.get_me())


if __name__ == '__main__':
    main()

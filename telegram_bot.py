from telegram import Bot


def send_image(tg_bot_token, tg_channel_id, image_path):
    bot = Bot(tg_bot_token)

    with open(image_path, 'rb') as image:
        bot.send_photo(tg_channel_id, image)

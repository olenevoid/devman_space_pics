from helpers import IMAGE_FOLDER_NAME
from os import path
from .fetch_apod_images import _fetch_nasa_apod_images
from .fetch_epic_images import _fetch_nasa_epic_images


NASA_FOLDER = path.join(IMAGE_FOLDER_NAME, 'nasa')


def fetch_apod_images(api_key, count, folder=NASA_FOLDER):
    return _fetch_nasa_apod_images(api_key, count, folder)


def fetch_epic_images(api_key, limit, folder=NASA_FOLDER):
    return _fetch_nasa_epic_images(api_key, folder, limit)

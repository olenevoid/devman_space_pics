from helpers import IMAGE_FOLDER_NAME
from os import path
from .fetch_apod_images import _fetch_nasa_apod_images
from .fetch_epic_images import _fetch_nasa_epic_images


NASA_FOLDER = path.join(IMAGE_FOLDER_NAME, 'nasa')
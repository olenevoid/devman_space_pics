import requests
from helpers import get_filename_from_url, save_image, IMAGE_FOLDER_NAME
from os import path, makedirs


SPACEX_FOLDER = path.join(IMAGE_FOLDER_NAME, 'spacex')


def get_spacex_image_urls(launch_id: str):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    json_dict: dict = response.json()

    return json_dict['links']['flickr']['original']


def fetch_spacex_images(launch_id: str):
    makedirs(SPACEX_FOLDER, exist_ok=True)

    image_urls = get_spacex_image_urls(launch_id)
    for image_url in image_urls:
        filename = path.join(SPACEX_FOLDER, get_filename_from_url(image_url))
        save_image(image_url, filename)
        
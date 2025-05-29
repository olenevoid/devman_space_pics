from os import makedirs, path
from helpers import get_filename_from_url, save_image
import requests


def get_last_nasa_epic_date_with_photos(api_key: str):
    url = 'https://api.nasa.gov/EPIC/api/natural/available'

    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()[-1]


def get_nasa_epic_image_urls(api_key: str, date: str):

    url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'

    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    image_urls = []
    date_with_slashes = date.replace('-', '/')

    for image_data in data:
        filename = f'{image_data["image"]}.png'
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date_with_slashes}/png/{filename}'
        image_urls.append(image_url)

    return image_urls


def fetch_nasa_epic_images(api_key, folder = NASA_FOLDER, limit = None):
    makedirs(folder, exist_ok=True)

    last_date = get_last_nasa_epic_date_with_photos(api_key)
    image_urls = get_nasa_epic_image_urls(api_key, last_date)

    params = {'api_key': api_key}

    if (limit is not None) and (limit < len(image_urls)):
        image_urls = image_urls[:limit]

    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename, params)

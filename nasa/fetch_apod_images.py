from os import makedirs, path
from nasa import NASA_FOLDER
from helpers import get_filename_from_url, save_image
import requests


def get_nasa_apod_image_urls(api_key: str, count: int):
    url = 'https://api.nasa.gov/planetary/apod'

    params = {
        'count': count,
        'api_key': api_key
        }
    
    response = requests.get(url, params=params)
    response.raise_for_status()

    json_dict = response.json()

    image_urls = [item['hdurl'] for item in json_dict]

    return image_urls


def fetch_nasa_apod_images(api_key: str, count: int):
    makedirs(NASA_FOLDER, exist_ok=True)

    image_urls = get_nasa_apod_image_urls(api_key, count)
    
    for image_url in image_urls:
        filename = path.join(NASA_FOLDER, get_filename_from_url(image_url))
        save_image(image_url, filename)
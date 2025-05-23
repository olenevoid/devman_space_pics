import requests
from os import makedirs, path, environ
from dotenv import load_dotenv
from helpers import save_image, get_filename_from_url, IMAGE_FOLDER_NAME


NASA_FOLDER = path.join(IMAGE_FOLDER_NAME, 'nasa')


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


def get_last_nasa_epic_date_with_photos(api_key: str):
    url = f'https://api.nasa.gov/EPIC/api/natural/available'

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
        filename = f'{image_data['image']}.png'
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{date_with_slashes}/png/{filename}'
        image_urls.append(image_url)

    return image_urls
  

def fetch_nasa_apod_images(api_key: str, count: int):
    makedirs(NASA_FOLDER, exist_ok=True)

    image_urls = get_nasa_apod_image_urls(api_key, count)
    
    for image_url in image_urls:
        filename = path.join(NASA_FOLDER, get_filename_from_url(image_url))
        save_image(image_url, filename)


def fetch_nasa_epic_images(api_key: str, limit: int | None = None):
    makedirs(NASA_FOLDER, exist_ok=True)
    
    last_date = get_last_nasa_epic_date_with_photos(api_key)
    image_urls = get_nasa_epic_image_urls(api_key, last_date)

    params = {'api_key': api_key}

    if (limit is not None) and (limit < len(image_urls)):
        image_urls = image_urls[:limit]

    for image_url in image_urls:
        filename = path.join(NASA_FOLDER, get_filename_from_url(image_url))
        save_image(image_url, filename, params) 


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']
    makedirs(IMAGE_FOLDER_NAME, exist_ok=True)
    
    fetch_spacex_images('605b4b95aa5433645e37d041')
    fetch_nasa_apod_images(nasa_api_key, 3)    
    fetch_nasa_epic_images(nasa_api_key, 3)
    

if __name__ == '__main__':
    main()
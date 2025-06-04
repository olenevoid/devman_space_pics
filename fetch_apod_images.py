from dotenv import load_dotenv
from os import makedirs, path, environ
from image_helpers import get_filename_from_url, save_image, IMAGE_FOLDER_NAME
import requests
from argparse import ArgumentParser


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


def fetch_nasa_apod_images(api_key, count, folder=NASA_FOLDER):
    makedirs(folder, exist_ok=True)

    image_urls = get_nasa_apod_image_urls(api_key, count)

    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename)


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']

    parser = ArgumentParser(
        description='Загружает фотографии с запусков SpaceX'
    )
    parser.add_argument(
        '-a',
        '--api_key',
        help='API-ключ NASA',
        type=str,
        default=nasa_api_key
    )
    parser.add_argument(
        '-c',
        '--count',
        help='Количество загружаемых снимков',
        type=int,
        default=3
    )
    parser.add_argument(
        '-f',
        '--folder',
        help='Папка для сохранения',
        default=NASA_FOLDER
    )

    args = parser.parse_args()

    print('Идет загрузка фотографий дня NASA')
    
    fetch_nasa_apod_images(args.api_key, args.count, args.folder)

    print('Загрузка фотографий завершена')


if __name__ == '__main__':
    main()

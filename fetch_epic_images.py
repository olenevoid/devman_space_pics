from dotenv import load_dotenv
from os import makedirs, path, environ
from image_helpers import get_filename_from_url, save_image, IMAGE_FOLDER_NAME
import requests
from argparse import ArgumentParser


NASA_FOLDER = path.join(IMAGE_FOLDER_NAME, 'nasa')


def get_last_nasa_epic_date_with_photos(api_key: str):
    url = 'https://api.nasa.gov/EPIC/api/natural/available'

    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()[-1]


def get_nasa_epic_data(api_key: str, date: str):
    url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'

    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def get_nasa_epic_image_urls(nasa_epic_data: dict, date: str):
    image_urls = []
    date_with_slashes = date.replace('-', '/')

    for image_data in nasa_epic_data:
        filename = f'{image_data["image"]}.png'
        image_url = 'https://api.nasa.gov/EPIC/archive/natural/{0}/png/{1}'
        image_url = image_url.format(date_with_slashes, filename)

        image_urls.append(image_url)

    return image_urls


def fetch_nasa_epic_images(
        api_key,
        date,
        folder=NASA_FOLDER,
        limit=None):

    makedirs(folder, exist_ok=True)

    nasa_epic_data = get_nasa_epic_data(api_key, date)

    image_urls = get_nasa_epic_image_urls(nasa_epic_data, date)

    params = {'api_key': api_key}

    if (limit is not None) and (limit < len(image_urls)):
        image_urls = image_urls[:limit]

    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename, params)


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']

    parser = ArgumentParser(
        description='Загружает фотографий Земли'
    )
    parser.add_argument(
        '-a',
        '--api_key',
        help='API-ключ NASA',
        default=nasa_api_key
    )
    parser.add_argument(
        '-L',
        '--limit',
        help='Задает лимит на скачивание',
        type=int,
        default=None
    )
    parser.add_argument(
        '-d',
        '--date',
        help='Дата в формате YYYY-MM-DD',
        default=get_last_nasa_epic_date_with_photos()
    )
    parser.add_argument(
        '-f',
        '--folder',
        help='Папка для сохранения',
        default=NASA_FOLDER
    )

    args = parser.parse_args()

    print('Идет загрузка фотографий')

    if args.folder is not None:
        fetch_nasa_epic_images(
            args.api_key,
            date=args.date,
            folder=args.folder,
            limit=args.limit)
    else:
        fetch_nasa_epic_images(args.api_key, date=args.date, limit=args.limit)

    print('Загрузка фотографий завершена')


if __name__ == '__main__':
    main()

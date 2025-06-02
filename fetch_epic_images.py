from os import makedirs, path
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
        image_url = 'https://api.nasa.gov/EPIC/archive/natural/{0}/png/{1}'
        image_url = image_url.format(date_with_slashes, filename)
        print(image_url)

        image_urls.append(image_url)

    return image_urls


def fetch_nasa_epic_images(api_key, folder=NASA_FOLDER, limit=None):
    makedirs(folder, exist_ok=True)

    last_date = get_last_nasa_epic_date_with_photos(api_key)
    image_urls = get_nasa_epic_image_urls(api_key, last_date)

    params = {'api_key': api_key}

    if (limit is not None) and (limit < len(image_urls)):
        image_urls = image_urls[:limit]

    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename, params)


def main():
    parser = ArgumentParser(
        description='Загружает фотографии с запусков SpaceX'
    )
    parser.add_argument('api_key', help='API-ключ NASA', type=str)
    parser.add_argument('-f', '--folder', help='Папка для сохранения')
    parser.add_argument('limit', help='Задает лимит на скачивание', type=int)

    args = parser.parse_args()

    print(f'Идет загрузка фотографий запуска {args.api_key}')

    if args.folder is not None:
        fetch_nasa_epic_images(args.api_key, args.folder, limit=args.limit)
    else:
        fetch_nasa_epic_images(args.api_key, limit=args.limit)

    print('Загрузка фотографий завершена')


if __name__ == '__main__':
    main()

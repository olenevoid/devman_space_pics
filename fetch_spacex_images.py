import requests
from image_helpers import get_filename_from_url, save_image, IMAGE_FOLDER_NAME
from os import path, makedirs
from argparse import ArgumentParser


SPACEX_FOLDER = path.join(IMAGE_FOLDER_NAME, 'spacex')


def get_all_launches():
    url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(url)
    response.raise_for_status()

    launches: list = response.json()
    launches.reverse()
    return launches


def get_latest_lanuch_images():
    launches = get_all_launches()

    for launch in launches:
        if len(launch['links']['flickr']['original']) > 0:
            return launch['links']['flickr']['original']


def _get_spacex_image_urls(launch_id: str):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    json_dict: dict = response.json()

    return json_dict['links']['flickr']['original']


def fetch_spacex_images(launch_id: str, folder: str = SPACEX_FOLDER):
    makedirs(folder, exist_ok=True)

    image_urls = _get_spacex_image_urls(launch_id)
    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename)


def main():
    parser = ArgumentParser(
        description='Загружает фотографии с запусков SpaceX'
    )
    parser.add_argument('launch_id', help='id запуска', type=str)
    parser.add_argument('-f', '--folder', help='Папка для сохранения')

    args = parser.parse_args()

    print(f'Идет загрузка фотографий запуска {args.launch_id}')

    if args.folder is not None:
        fetch_spacex_images(args.launch_id, args.folder)
    else:
        fetch_spacex_images(args.launch_id)

    print('Загрузка фотографий завершена')


if __name__ == '__main__':
    main()

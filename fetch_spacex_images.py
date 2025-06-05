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


def get_latest_lanuch_image_urls(launches: dict):
    for launch in launches:
        if len(launch['links']['flickr']['original']) > 0:
            return launch['links']['flickr']['original']


def _get_spacex_image_urls(launch_id: str):
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    launches: dict = response.json()

    return launches['links']['flickr']['original']


def fetch_spacex_images(launch_id: str = None, folder: str = None):
    makedirs(folder, exist_ok=True)

    if launch_id:
        image_urls = _get_spacex_image_urls(launch_id)
    else:
        launches = get_all_launches()
        image_urls = get_latest_lanuch_image_urls(launches)

    for image_url in image_urls:
        filename = path.join(folder, get_filename_from_url(image_url))
        save_image(image_url, filename)


def main():
    parser = ArgumentParser(
        description='Загружает фотографии с запусков SpaceX'
    )
    parser.add_argument('-L', '--launch_id', help='id запуска')
    parser.add_argument(
        '-f',
        '--folder',
        help='Папка для сохранения',
        default=SPACEX_FOLDER
    )

    args = parser.parse_args()

    if args.launch_id:
        print(f'Идет загрузка фотографий запуска {args.launch_id}')
    else:
        print('Идет загрузка фотографий последнего запуска')
    
    fetch_spacex_images(args.launch_id, args.folder)

    print('Загрузка фотографий завершена')


if __name__ == '__main__':
    main()

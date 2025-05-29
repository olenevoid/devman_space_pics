import requests
from urllib.parse import urlparse, unquote
from os import path, listdir


IMAGE_FOLDER_NAME = 'images'


def save_image(url: str, filename: str, params: dict = None):

    response = requests.get(url, params=params)

    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_filename_from_url(url):
    parsed_url = urlparse(url)

    name = parsed_url.path.split('/')[-1]
    name = unquote(name)

    if path.splitext(name)[1] == '':
        name = name+'.jpeg'

    return name


def get_all_images():
    directories = listdir(IMAGE_FOLDER_NAME)
    images = []

    for directory in directories:
        path_ = path.join(IMAGE_FOLDER_NAME, directory)
        images += get_images(path_)

    return images


def get_images(directory: str):
    images = []

    for filename in listdir(directory):
        path_ = path.join(directory, filename)

        if path.isfile(path_):
            images.append(path_)

    return images

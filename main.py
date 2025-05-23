from os import makedirs, environ
from dotenv import load_dotenv
from helpers import IMAGE_FOLDER_NAME
from fetch_spacex_images import fetch_spacex_images
from nasa.fetch_apod_images import fetch_nasa_apod_images
from nasa.fetch_epic_images import fetch_nasa_epic_images


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']
    makedirs(IMAGE_FOLDER_NAME, exist_ok=True)
    
    fetch_spacex_images('605b4b95aa5433645e37d041')
    fetch_nasa_apod_images(nasa_api_key, 3)    
    fetch_nasa_epic_images(nasa_api_key, 3)
    

if __name__ == '__main__':
    main()

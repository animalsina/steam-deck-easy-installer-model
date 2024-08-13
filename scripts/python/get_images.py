import requests
import argparse
import os
import shutil
from urllib.parse import urlparse
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration parameters
SEARCH_URL = config.get('settings', 'search_url')
ASSETS_URL = config.get('settings', 'assets_url')
TEMP_DIR_NAME = "steam_images"

def get_game_id(game_name):
    search_url = f"{SEARCH_URL}?term={game_name}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to retrieve game ID for '{game_name}'. Status code: {response.status_code}")
        return None

    data = response.json()
    if data.get('success') and data['data']:
        return data['data'][0]['id']
    else:
        print(f"No game ID found for '{game_name}'.")
        return None

def get_game_images(game_id):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "game_id": [game_id],
        "order": "score_desc",
        "asset_type": "logo",  # Placeholder value, will be updated in the loop
        "page": 0,
        "limit": 48
    }

    asset_types = ["logo", "icon", "grid", "hero"]
    images_by_type = {}

    for asset_type in asset_types:
        payload['asset_type'] = asset_type
        response = requests.post(ASSETS_URL, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve images for asset type '{asset_type}' and game ID '{game_id}'. Status code: {response.status_code}")
            continue

        data = response.json()
        if data.get('success') and 'data' in data and 'assets' in data['data']:
            assets = data['data']['assets']
            if assets:
                images_by_type[asset_type] = {
                    'url': assets[0]['url'],
                }

    return images_by_type

def get_file_extension_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1].lstrip('.')  # Remove the dot from the extension

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to download image from '{image_url}'. Status code: {response.status_code}")

def clean_temp_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Retrieve and download images of a game from SteamGridDB.")
    parser.add_argument('game_name', type=str, help="Name of the game to search for")
    parser.add_argument('app_id', type=str, help="Application ID for naming images")
    args = parser.parse_args()

    game_name = args.game_name
    app_id = args.app_id

    game_id = get_game_id(game_name)
    if not game_id:
        return

    temp_dir = os.path.join(os.getcwd(), TEMP_DIR_NAME)
    clean_temp_directory(temp_dir)
    print(f"Temporary directory created at: {temp_dir}")

    images_by_type = get_game_images(game_id)
    if not images_by_type:
        return

    for asset_type, asset_info in images_by_type.items():
        image_url = asset_info['url']
        extension = get_file_extension_from_url(image_url)
        image_filename = os.path.join(temp_dir, f"{app_id}_{asset_type}.{extension}")
        print(f"Downloading {asset_type} image from {image_url} with extension {extension}")
        download_image(image_url, image_filename)

if __name__ == "__main__":
    main()

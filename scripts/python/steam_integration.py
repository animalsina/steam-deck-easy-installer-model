import os
import shutil
import subprocess
import hashlib
import vdf
import uuid
import configparser
from datetime import datetime

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration parameters
steam_games_folder = os.path.expanduser(config.get('settings', 'steam_games_folder'))
steam_root = os.path.expanduser(config.get('settings', 'steam_root'))
shortcuts_file_path = os.path.expanduser(config.get('settings', 'shortcuts_vdf'))
search_url = config.get('settings', 'search_url')
assets_url = config.get('settings', 'assets_url')

def get_steam_user_data_path(steam_root=None):
    if steam_root is None:
        steam_root = os.path.expanduser("~/.local/share/Steam/userdata")

    if not os.path.exists(steam_root):
        print(f"Default Steam path not found. Please provide the correct path.")
        steam_root = input("Enter the correct path to the Steam userdata directory: ")

    if os.path.exists(steam_root):
        user_folders = os.listdir(steam_root)
        if user_folders:
            return os.path.join(steam_root, user_folders[0])

    return None

def generate_app_id(app_name):
    hash_object = hashlib.md5(app_name.encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex[:8], 16)
    app_id = "65535" + str(hash_int % (10**6))
    return app_id

def backup_shortcuts_file(shortcuts_file_path):
    if os.path.exists(shortcuts_file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file_path = f"{shortcuts_file_path}_{timestamp}.bak"
        shutil.copy2(shortcuts_file_path, backup_file_path)
        print(f"Backup created: {backup_file_path}")

def add_or_update_shortcut(steam_user_data_path, app_name, app_id, flatpak_command, icon_path):
    steam_vdf_complete_path = os.path.join(steam_user_data_path, shortcuts_file_path)

    # Backup the existing shortcuts file if it exists
    backup_shortcuts_file(steam_vdf_complete_path)

    # Verifica se la directory del file di configurazione esiste, altrimenti creala
    shortcuts_dir = os.path.dirname(steam_vdf_complete_path)
    if not os.path.exists(shortcuts_dir):
        os.makedirs(shortcuts_dir)
        print(f"Directory {shortcuts_dir} creata.")

    # Carica o inizializza il file shortcuts.vdf
    if os.path.exists(steam_vdf_complete_path):
        with open(steam_vdf_complete_path, 'rb') as f:
            shortcuts = vdf.binary_load(f)
    else:
        shortcuts = {"shortcuts": {}}
        print(f"File {steam_vdf_complete_path} creato.")

    existing_id = None
    for shortcut_id, shortcut in shortcuts["shortcuts"].items():
        if shortcut["appid"] == app_id:
            existing_id = shortcut_id
            break

    print(f"Shortcut Path: {icon_path}")

    if icon_path is None:
        icon_path = "./"

    shortcut = {
        "appid": app_id,
        "AppName": app_name,
        "Exe": flatpak_command,
        "StartDir": "",
        "icon": icon_path,
        "ShortcutPath": "",
        "LaunchOptions": "",
        "IsHidden": 0,
        "AllowDesktopConfig": 1,
        "OpenVR": 0,
        "Devkit": 0,
        "DevkitGameID": "",
        "LastPlayTime": 0,
        "tags": {}
    }

    if existing_id:
        shortcuts["shortcuts"][existing_id] = shortcut
    else:
        shortcuts["shortcuts"][str(uuid.uuid4().int)] = shortcut

    with open(steam_vdf_complete_path, 'wb') as f:
        vdf.binary_dump(shortcuts, f)

    return app_id

def move_images(app_id, images_folder, steam_root):
    steam_grid_folder = os.path.join(steam_root, "config", "grid")

    if not os.path.exists(steam_grid_folder):
        os.makedirs(steam_grid_folder)

    for img_type in ["logo", "hero", "grid"]:
        matching_files = [f for f in os.listdir(images_folder) if f.startswith(f"{app_id}_{img_type}")]

        if matching_files:
            source_file = os.path.join(images_folder, matching_files[0])
            dest_file = os.path.join(steam_grid_folder, f"{app_id}_{img_type}{os.path.splitext(matching_files[0])[1]}")

            print(f"Copying {source_file} to {dest_file}")
            shutil.copy(source_file, dest_file)

            os.remove(source_file)
            print(f"Deleted {source_file}")
        else:
            print(f"No image found for {img_type} in {images_folder}")

def hash_app_name(app_name):
    hash_object = hashlib.md5(app_name.encode())
    return hash_object.hexdigest()

def move_icon_image(app_id, images_folder):
    icon_file = f"{hash_app_name(app_id)}.ico"
    icon_path = os.path.join(images_folder, f"{app_id}_icon.ico")
    dest_file = os.path.join(steam_games_folder, icon_file)

    if os.path.exists(icon_path):
        if not os.path.exists(steam_games_folder):
            os.makedirs(steam_games_folder)

        print(f"Copying {icon_path} to {dest_file}")

        try:
            shutil.copy2(icon_path, dest_file)
            print(f"Successfully copied {icon_path} to {dest_file}")

            original_checksum = calculate_checksum(icon_path)
            copied_checksum = calculate_checksum(dest_file)

            if original_checksum == copied_checksum:
                print("File integrity verified.")
            else:
                print("File integrity check failed.")

            os.remove(icon_path)
            print(f"Deleted {icon_path}")
            return dest_file
        except Exception as e:
            print(f"Error copying file: {e}")
            return None  # Return None if there was an error

    else:
        print(f"No icon image found to move in {icon_path} path.")
        return None

def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def run_get_images(app_name, app_id):
    script_path = os.path.join(os.getcwd(), 'scripts', 'python', 'get_images.py')
    subprocess.run(["python3", script_path, app_name, str(app_id)], check=True)

def main(app_name, flatpak_repo):
    steam_user_data_path = get_steam_user_data_path()
    if not steam_user_data_path:
        print("Unable to find the Steam user data path.")
        return

    source_images_folder = os.path.join(os.getcwd(), 'steam_images')

    app_id = generate_app_id(flatpak_repo)

    if os.path.exists(source_images_folder) and os.listdir(source_images_folder):
        print("Images already present in the source folder, skipping download.")
    else:
        run_get_images(flatpak_repo, app_id)

    icon_path = os.path.join(source_images_folder, f"{app_id}_icon.ico")
    flatpak_command = f"flatpak run {flatpak_repo}"

    move_images(app_id, source_images_folder, steam_user_data_path)
    dest_file = move_icon_image(app_id, source_images_folder)

    add_or_update_shortcut(steam_user_data_path, app_name, app_id, flatpak_command, dest_file)

    print(f"Program {app_name} added to Steam with ID {app_id}")
    try:
        shutil.rmtree(source_images_folder)
        print(f"Directory {source_images_folder} removed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: steam_integration.py <App Name> <Flatpak Repo>")
        sys.exit(1)

    app_name = sys.argv[1]
    flatpak_repo = sys.argv[2]
    main(app_name, flatpak_repo)

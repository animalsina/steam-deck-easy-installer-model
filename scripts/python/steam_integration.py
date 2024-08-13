import os
import shutil
import subprocess
import hashlib
import vdf
import uuid

# Folder configuration
home_dir = os.path.expanduser("~")
steam_games_folder = os.path.join(home_dir, "deck", ".local", "share", "Steam", "steam", "games")

# Function to get the Steam path
def get_steam_user_data_path(steam_root=None):
    if steam_root is None:
        steam_root = os.path.join(home_dir, "deck", ".local", "share", "Steam", "userdata")

    if not os.path.exists(steam_root):
        print(f"Default Steam path not found. Please provide the correct path.")
        steam_root = input("Enter the correct path to the Steam userdata directory: ")

    if os.path.exists(steam_root):
        user_folders = os.listdir(steam_root)
        if user_folders:
            return os.path.join(steam_root, user_folders[0])

    return None

# Function to generate a numeric app ID starting with 65538
def generate_app_id(app_name):
    hash_object = hashlib.md5(app_name.encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex[:8], 16)
    app_id = "65535" + str(hash_int % (10**6))
    return app_id

# Function to add or update a shortcut to Steam
def add_or_update_shortcut(steam_user_data_path, app_name, app_id, flatpak_command, icon_path):
    shortcuts_file = os.path.join(steam_user_data_path, "config", "shortcuts.vdf")

    if os.path.exists(shortcuts_file):
        with open(shortcuts_file, 'rb') as f:
            shortcuts = vdf.binary_load(f)
    else:
        shortcuts = {"shortcuts": {}}

    existing_id = None
    for shortcut_id, shortcut in shortcuts["shortcuts"].items():
        if shortcut["appid"] == app_id:
            existing_id = shortcut_id
            break

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

    with open(shortcuts_file, 'wb') as f:
        vdf.binary_dump(shortcuts, f)

    return app_id

# Function to move images while retaining the original extension
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

            # Delete the source file after copying
            os.remove(source_file)
            print(f"Deleted {source_file}")
        else:
            print(f"No image found for {img_type} in {images_folder}")

# Function to hash the app name
def hash_app_name(app_name):
    hash_object = hashlib.md5(app_name.encode())
    return hash_object.hexdigest()

# Function to move the icon image to the Steam games folder
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

            # Delete the source file after copying
            os.remove(icon_path)
            print(f"Deleted {icon_path}")

        except Exception as e:
            print(f"Error copying file: {e}")

    else:
        print("No icon image found to move.")

def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Run the get_images.py script
def run_get_images(app_name, app_id):
    script_path = os.path.join(os.path.dirname(__file__), 'get_images.py')
    subprocess.run(["python3", script_path, app_name, str(app_id)], check=True)

# Main function
def main(app_name):
    steam_user_data_path = get_steam_user_data_path()
    if not steam_user_data_path:
        print("Unable to find the Steam user data path.")
        return

    source_images_folder = os.path.join(os.getcwd(), 'steam_images')

    app_id = generate_app_id(app_name)

    if os.path.exists(source_images_folder) and os.listdir(source_images_folder):
        print("Images already present in the source folder, skipping download.")
    else:
        run_get_images(app_name, app_id)

    icon_path = os.path.join(source_images_folder, f"{app_id}_icon.ico")
    flatpak_command = f"flatpak run {app_name}"

    add_or_update_shortcut(steam_user_data_path, app_name, app_id, flatpak_command, icon_path)
    move_images(app_id, source_images_folder, steam_user_data_path)
    move_icon_image(app_id, source_images_folder)
    print(f"Program {app_name} added to Steam with ID {app_id}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: steam_integration.py <Program Name>")
        sys.exit(1)

    app_name = sys.argv[1]
    main(app_name)

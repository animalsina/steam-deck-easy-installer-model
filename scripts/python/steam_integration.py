import os
import shutil
import subprocess
import vdf
import uuid

# Folder configuration
home_dir = os.path.expanduser("~")

# Function to get the Steam path
def get_steam_user_data_path():
    steam_root = os.path.join(home_dir, ".steam", "steam", "userdata")
    user_folders = os.listdir(steam_root)

    if user_folders:
        return os.path.join(steam_root, user_folders[0], "config")
    return None

# Function to add a shortcut to Steam
def add_flatpak_shortcut(steam_user_data_path, app_name, flatpak_command, icon_path):
    shortcuts_file = os.path.join(steam_user_data_path, "shortcuts.vdf")

    if os.path.exists(shortcuts_file):
        with open(shortcuts_file, 'rb') as f:
            shortcuts = vdf.binary_load(f)
    else:
        shortcuts = {"shortcuts": {}}

    app_id = str(abs(hash(app_name)) % (10 ** 10))
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

    shortcuts["shortcuts"][str(uuid.uuid4().int)] = shortcut

    with open(shortcuts_file, 'wb') as f:
        vdf.binary_dump(shortcuts, f)

    return app_id

# Function to move images while retaining the original extension
def move_images(app_id, images_folder):
    steam_grid_folder = os.path.expanduser(f"~/.steam/root/config/grid")

    if not os.path.exists(steam_grid_folder):
        os.makedirs(steam_grid_folder)

    for img_type in ["icon", "logo", "hero", "grid"]:
        matching_files = [f for f in os.listdir(images_folder) if f.startswith(f"{img_type}_")]

        if matching_files:
            source_file = os.path.join(images_folder, matching_files[0])
            dest_file = os.path.join(steam_grid_folder, f"{app_id}_{img_type}{os.path.splitext(matching_files[0])[1]}")

            print(f"Moving {source_file} to {dest_file}")
            shutil.move(source_file, dest_file)
        else:
            print(f"No image found for {img_type} in {images_folder}")

# Run the get_images.py script
def run_get_images(app_name):
    script_path = os.path.join(os.path.dirname(__file__), 'get_images.py')
    subprocess.run(["python3", script_path, app_name], check=True)

# Main function
def main(app_name):
    # Image path in the current directory
    source_images_folder = os.path.join(os.getcwd(), 'steam_images')

    if os.path.exists(source_images_folder) and os.listdir(source_images_folder):
        print("Images already present in the source folder, skipping download.")
    else:
        # Run the script to download images if they don't already exist
        run_get_images(app_name)

    # Add the Flatpak app to Steam
    steam_user_data_path = get_steam_user_data_path()
    icon_path = os.path.join(source_images_folder, "icon_*.png")  # Modify based on the actual icon

    if steam_user_data_path:
        flatpak_command = f"flatpak run {app_name}"
        app_id = add_flatpak_shortcut(steam_user_data_path, app_name, flatpak_command, icon_path)
        move_images(app_id, source_images_folder)
        print(f"Program {app_name} added to Steam with ID {app_id}")
    else:
        print("Unable to find the Steam user data path.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: steam_integration.py <Program Name>")
        sys.exit(1)

    app_name = sys.argv[1]
    main(app_name)

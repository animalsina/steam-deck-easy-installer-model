# !! Very important alert !! 
This script is WIP, until the official release use it only if you know what you do. 
Report every problem, some command in the scripts can corrupts the files. 



# Steam Integration Project

## Overview

This project integrates Flatpak applications with Steam, allowing you to add shortcuts to Steam and configure images for the applications. It consists of a series of scripts to automate the process of installing dependencies, configuring Steam, and handling application images.

## Scripts

### `install_python.sh`

Installs Python3 and pip if they are not already installed.

### `install_python_libraries.sh`

Installs required Python libraries using pip.

### `install_flatpak_app.sh`

Installs a Flatpak application.

### `configure_steam_and_images.sh`

Configures Steam by adding shortcuts and handling images, ensuring Steam is closed during the process and restarted afterward.

### `get_images.py`

Retrieves and downloads images for a specified game from SteamGridDB based on the game name and application ID.

### `steam_integration.py`

Adds or updates a Steam shortcut for a Flatpak application, moves images to the appropriate directories, and performs various file operations related to the application's integration with Steam.

### `run.sh`

Automates the entire process by calling the relevant installation and configuration scripts. It takes a Flatpak application name as an argument and executes the installation and configuration steps.

## Setup Instructions

### Prerequisites

Ensure you have a Linux environment with the necessary permissions to install software. This project assumes you are using a Debian-based distribution (e.g., Ubuntu).

### 1. Clone the Repository

Clone this repository to your local machine:

```
git clone <repository-url>
cd <repository-directory>
```

### 2. Make Scripts Executable

Make the scripts executable:

```
chmod +x scripts/bash/install_python.sh
chmod +x scripts/bash/install_python_libraries.sh
chmod +x scripts/bash/install_flatpak_app.sh
chmod +x scripts/bash/configure_steam_and_images.sh
chmod +x bin/run.sh
```

### 3. Run the Main Script

Execute the `run.sh` script to start the installation and configuration process. Provide the Flatpak application name as an argument:

```
./bin/run.sh <flatpak-app-name>
```

This will perform the following tasks:
- Install Python3 and pip if they are not already installed.
- Install required Python libraries.
- Install the specified Flatpak application.
- Configure Steam and handle image downloads and placement.

## Usage

### Adding a New Flatpak Application

To add a new Flatpak application to Steam, simply run the `run.sh` script with the application name:

```
./bin/run.sh <flatpak-app-name>
```

Replace `<flatpak-app-name>` with the name of the Flatpak application you want to add.

## Notes

- Ensure Steam is not running while the `configure_steam_and_images.sh` script is executing. The script will automatically close and restart Steam for you.
- The `get_images.py` script retrieves images from SteamGridDB and saves them in a temporary directory before moving them to the appropriate Steam folders.
- The `steam_integration.py` script updates the Steam shortcut file to include the new Flatpak application.

## Troubleshooting

- If Steam does not restart properly or does not reflect the changes, manually close and restart Steam.
- Ensure that the Steam userdata path is correctly specified if the default location is not used.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Steam Integration Scripts - Alpha 0.0.1

This repository contains a set of scripts designed to integrate Flatpak applications with Steam, including functionalities for installing dependencies, configuring Steam shortcuts, and managing game images. Below is an overview of each script and its purpose.

## Scripts Overview

### 1. `install_python.sh`

This script checks if Python3 is installed on the system. If not, it installs Python3 and `pip`.

**Usage:**
```bash
./install_python.sh
```

2. install_flatpak.sh
This script installs Flatpak and the Flathub repository if they are not already installed.

Usage:

```bash
./install_flatpak.sh
```

3. install_python_libraries.sh
This script installs required Python libraries listed in a requirements.txt file.

Usage:

```bash
./install_python_libraries.sh
```

4. install_flatpak_app.sh
This script installs a Flatpak application based on the application name provided as an argument.

Usage:

```bash
./install_flatpak_app.sh <app_name>
```

5. configure_steam_and_images.sh
This script configures Steam to add a Flatpak application and move images to the Steam grid directory.

Usage:

```bash
./configure_steam_and_images.sh <app_name>
```

6. steam_integration.py
This Python script integrates a Flatpak application with Steam by:

Adding a shortcut to Steam.
Moving application images to the Steam grid directory.
Running the get_images.py script if images are not already present.
Usage:

```bash
python3 steam_integration.py <app_name>
```

7. get_images.py
This Python script retrieves and downloads images for a game from SteamGridDB. It searches for the game, fetches available images, and saves them to a temporary directory.

Usage:

```bash
python3 get_images.py <game_name>
```

Dependencies
Python3: Required for running Python scripts.
pip: Required for installing Python libraries.
Flatpak: Required for managing Flatpak applications.
Requests: Python library for HTTP requests (install via pip install requests).
VDF: Python library for handling Steam VDF files (install via pip install vdf).
Installation Instructions
Install Dependencies:

Run install_python.sh to install Python3 and pip.
Run install_flatpak.sh to install Flatpak.
Install Python Libraries:

Ensure a requirements.txt file is present.
Run install_python_libraries.sh.
Add Flatpak Application to Steam:

Run steam_integration.py with the application name as an argument.
Example: python3 steam_integration.py <app_name>.
Manage Images:

Run get_images.py to download game images if not already present.
Example: python3 get_images.py <game_name>.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Feel free to open issues or submit pull requests to contribute to this project.

Contact
For any questions, please contact decknewsunofficial@gmail.com.
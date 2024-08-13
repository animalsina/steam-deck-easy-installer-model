#!/bin/bash

# Import functions from external files
source install_python.sh
source install_flatpak.sh
source install_python_libraries.sh
source install_flatpak_app.sh
source configure_steam_and_images.sh

# Check that an argument has been passed to the script
if [ -z "$1" ]; then
    echo "Usage: $0 <flatpak-app-name>"
    exit 1
fi

# Flatpak app name passed as an argument
APP_NAME=$1

# Run the installations and configurations
install_python
install_flatpak
install_python_libraries
install_flatpak_app $APP_NAME
configure_steam_and_images $APP_NAME

echo "Installation and configuration completed."

#!/bin/bash

CONFIG_FILE="./config.ini"

# Function to read and print values from the configuration file
read_config() {
    local config_file=$1
    echo "Reading configuration from $config_file"
    while IFS='=' read -r key value; do
        # Remove leading and trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # Ensure the key is a valid identifier and not empty
        if [[ -n "$key" && "$key" != \#* && "$key" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
            declare -g "$key=$value"
        fi
    done < "$config_file"
}

# Load the configuration
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

read_config "$CONFIG_FILE"

# Print variables for debugging
echo "REPO_DIR: $REPO_DIR"
echo "GIT_REPO_URL: $GIT_REPO_URL"
echo "steam_games_folder: $steam_games_folder"
echo "steam_root: $steam_root"
echo "shortcuts_vdf: $shortcuts_vdf"
echo "search_url: $search_url"
echo "assets_url: $assets_url"

APP_NAME=$1
FLATPAK_REPO=$2

echo "=============="
echo "AppName: $APP_NAME"
echo "FLATPAK_REPO: $FLATPAK_REPO"
echo "=============="
echo ""

if [ -z "$APP_NAME" ]; then
    echo "Usage: $0 <app-name> <flatpak-repo>"
    exit 1
fi

if [ -z "$FLATPAK_REPO" ]; then
    echo "Error: FLATPAK_REPO argument is not set."
    exit 1
fi

install_git_if_needed() {
    if ! command -v git &> /dev/null; then
        echo "Git is not installed. Installing..."
        sudo apt update
        sudo apt install -y git
    else
        echo "Git is already installed."
    fi
}

clone_git_repo() {
    if [ -d "$REPO_DIR" ]; then
        rm -rf "$REPO_DIR"
    fi
    git clone "$GIT_REPO_URL" "$REPO_DIR"
}

make_scripts_executable() {
    chmod +x "scripts/bash/install_python.sh"
    chmod +x "scripts/bash/install_python_libraries.sh"
    chmod +x "scripts/bash/install_flatpak_app.sh"
    chmod +x "scripts/bash/configure_steam_and_images.sh"
}

run_installation() {
    # Navigate to the repository folder, but only if we're not in local mode
    if [ ! -f ".local" ]; then
        cd "$REPO_DIR" || { echo "Failed to navigate to $REPO_DIR"; exit 1; }
    else
        echo "Local mode detected, using existing directory."
    fi

    # Ensure the scripts are executable
    make_scripts_executable

    # Execute the scripts
    source scripts/bash/install_python.sh
    source scripts/bash/install_python_libraries.sh
    source scripts/bash/install_flatpak_app.sh
    source scripts/bash/configure_steam_and_images.sh

    install_python_and_pipx
    install_python_libraries
    install_flatpak_app "$FLATPAK_REPO"
    configure_steam_and_images "$APP_NAME" "$FLATPAK_REPO"

    echo "Installation and configuration completed."

    # Return to the original directory, only if we navigated into the repository
    if [ ! -f ".local" ]; then
        cd - || exit
    fi
}

cleanup() {
    # Cleanup only if not in local mode
    if [ ! -f ".local" ]; then
        rm -rf "$REPO_DIR"
        echo "Git repository directory removed."
    fi
    echo "Operation completed successfully."
}

if [ -f ".local" ]; then
    echo "Local mode detected. Skipping GitHub repository clone."
    run_installation
else
    install_git_if_needed
    clone_git_repo
    run_installation
    cleanup
fi

#!/bin/bash

# URL of the Git repository
GIT_REPO_URL="https://github.com/animalsina/steam-deck-easy-installer-model.git"

# Name of the Flatpak application (passed as an argument)
APP_NAME=$1

# Name of the directory where the repository will be cloned
REPO_DIR="temp__git_repo"


# Function to check if git is installed
install_git_if_needed() {
    if ! command -v git &> /dev/null; then
        echo "Git is not installed. Installing..."
        sudo apt update
        sudo apt install -y git
    else
        echo "Git is already installed."
    fi
}

# Function to clone the Git repository
clone_git_repo() {
    if [ -d "$REPO_DIR" ]; then
        rm -rf "$REPO_DIR"
    fi
    git clone "$GIT_REPO_URL" "$REPO_DIR"
}

# Function to make the scripts executable
make_scripts_executable() {
    chmod +x "$REPO_DIR/scripts/bash/install_python.sh"
    chmod +x "$REPO_DIR/scripts/bash/install_python_libraries.sh"
    chmod +x "$REPO_DIR/scripts/bash/install_flatpak_app.sh"
    chmod +x "$REPO_DIR/scripts/bash/configure_steam_and_images.sh"
}

# Main function to run the installation and configuration
run_installation() {
    source "$REPO_DIR/scripts/bash/install_python.sh"
    source "$REPO_DIR/scripts/bash/install_python_libraries.sh"
    source "$REPO_DIR/scripts/bash/install_flatpak_app.sh"
    source "$REPO_DIR/scripts/bash/configure_steam_and_images.sh"

    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 <flatpak-app-name>"
        exit 1
    fi

    install_python
    install_python_libraries
    install_flatpak_app "$APP_NAME"
    configure_steam_and_images "$APP_NAME"

    echo "Installation and configuration completed."
}

# Function to remove the Git repository directory
cleanup() {
    rm -rf "$REPO_DIR"
    echo "Git repository directory removed."
    echo "Operation completed successfully."
}

# Run the script
install_git_if_needed
clone_git_repo
make_scripts_executable
run_installation
cleanup

#!/bin/bash

CONFIG_FILE="./config.ini"

# Funzione per leggere e stampare i valori dal file di configurazione
read_config() {
    local config_file=$1
    echo "Reading configuration from $config_file"
    while IFS='=' read -r key value; do
        # Rimuovi spazi bianchi iniziali e finali
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        if [[ -n "$key" && "$key" != \#* ]]; then
            declare -g "$key=$value"
        fi
    done < "$config_file"
}

# Carica la configurazione
if [ ! -f "$CONFIG_FILE" ]; then
    echo "File di configurazione non trovato: $CONFIG_FILE"
    exit 1
fi

read_config "$CONFIG_FILE"

# Stampa le variabili per il debug
echo "REPO_DIR: $REPO_DIR"
echo "GIT_REPO_URL: $GIT_REPO_URL"
echo "steam_games_folder: $steam_games_folder"
echo "steam_root: $steam_root"
echo "shortcuts_vdf: $shortcuts_vdf"
echo "search_url: $search_url"
echo "assets_url: $assets_url"

APP_NAME=$1
FLATPAK_REPO=$2

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
    # Naviga alla cartella del repository
    cd "$REPO_DIR" || { echo "Failed to navigate to $REPO_DIR"; exit 1; }

    # Assicurati che gli script siano eseguibili
    make_scripts_executable

    # Esegui gli script
    source scripts/bash/install_python.sh
    source scripts/bash/install_python_libraries.sh
    source scripts/bash/install_flatpak_app.sh
    source scripts/bash/configure_steam_and_images.sh

    install_python_and_pipx
    install_python_libraries
    install_flatpak_app "$FLATPAK_REPO"
    configure_steam_and_images "$APP_NAME"

    echo "Installation and configuration completed."

    # Torna alla cartella originale
    cd - || exit
}

cleanup() {
    rm -rf "$REPO_DIR"
    echo "Git repository directory removed."
    echo "Operation completed successfully."
}

install_git_if_needed
clone_git_repo
run_installation
cleanup

#!/bin/bash

install_python_and_pipx() {
    if ! command -v python3 &>/dev/null; then
        echo "Python3 not found, installing..."
        sudo pacman -Syu --noconfirm python python-pip
    else
        echo "Python3 is already installed."
    fi

    if ! command -v pipx &>/dev/null; then
        echo "pipx not found, installing..."
        # Installa pipx utilizzando pip
        python -m pip install --user pipx
        # Aggiungi il percorso di pipx alla variabile PATH
        export PATH="$HOME/.local/bin:$PATH"
        # Verifica se pipx è stato installato correttamente
        if command -v pipx &>/dev/null; then
            echo "pipx successfully installed."
        else
            echo "Failed to install pipx."
        fi
    else
        echo "pipx is already installed."
    fi
}

# Chiamata alla funzione di installazione
install_python_and_pipx

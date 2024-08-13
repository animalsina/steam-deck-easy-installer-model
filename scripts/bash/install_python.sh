#!/bin/bash

install_python() {
    if ! command -v python3 &>/dev/null; then
        echo "Python3 not found, installing..."
        sudo apt update
        sudo apt install -y python3 python3-pip
    else
        echo "Python3 is already installed."
    fi
}

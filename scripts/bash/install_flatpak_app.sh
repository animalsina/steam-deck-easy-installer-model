#!/bin/bash

install_flatpak_app() {
    flatpak install --user -y "$1"
}
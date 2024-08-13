#!/bin/bash

install_flatpak_app() {
    APP_NAME=$1
    flatpak install --user -y $APP_NAME
}
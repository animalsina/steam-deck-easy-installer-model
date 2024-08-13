#!/bin/bash

configure_steam_and_images() {
    APP_NAME=$1

    # Run the Python script to configure Steam and add images
    python3 steam_integration.py $APP_NAME
}

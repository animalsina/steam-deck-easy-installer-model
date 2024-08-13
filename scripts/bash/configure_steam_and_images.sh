#!/bin/bash

configure_steam_and_images() {
    APP_NAME=$1

    steam_pid=$(pgrep steam)
    if [ -n "$steam_pid" ]; then
        kill "$steam_pid"
        echo "Closed Steam."
    else
        echo "Steam is not started."
    fi

    sleep 5

    # Run the Python script to configure Steam and add images
    python3 steam_integration.py $APP_NAME

    steam &
    echo "Restarted Steam."
}

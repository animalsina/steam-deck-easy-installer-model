#!/bin/bash

# Function to configure Steam and add images
configure_steam_and_images() {
    APP_NAME=$1

    # Ensure APP_NAME is provided
    if [ -z "$APP_NAME" ]; then
        echo "Usage: $0 <app-name>"
        exit 1
    fi

    # Check if Steam is running and close it if it is
    steam_pid=$(pgrep steam)
    if [ -n "$steam_pid" ]; then
        kill "$steam_pid"
        echo "Steam closed."
    else
        echo "Steam is not running."
    fi

    # Wait for a few seconds to ensure Steam is closed
    sleep 5

    # Get the absolute path to the Python script
    python_script="scripts/python/steam_integration.py"

    # Run the Python script to configure Steam and add images
    if ! python3 "$python_script" "$APP_NAME"; then
        echo "Failed to run the Python script."
        exit 1
    fi

    # Restart Steam
    steam &
    echo "Steam restarted."
}

# Example of how to call the function
# configure_steam_and_images "YourAppName"

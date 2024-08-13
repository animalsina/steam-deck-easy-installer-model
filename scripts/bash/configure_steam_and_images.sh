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
    if pgrep steam > /dev/null; then
        echo "Closing Steam..."
        pkill steam
        sleep 5  # Wait for a few seconds to ensure Steam is closed

        # Check if Steam is still running
        if pgrep steam > /dev/null; then
            echo "Steam could not be closed properly."
            exit 1
        else
            echo "Steam closed successfully."
        fi
    else
        echo "Steam is not running."
    fi

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

#!/bin/bash

close_steam() {
    local max_retries=5
    local retry_interval=5  # seconds

    for (( i=1; i<=max_retries; i++ )); do
        if pgrep steam > /dev/null; then
            echo "Attempt $i: Closing Steam..."
            pkill steam
            sleep $retry_interval  # Wait for a few seconds to ensure Steam is closed

            # Check if Steam is still running
            if pgrep steam > /dev/null; then
                echo "Steam could not be closed properly on attempt $i."
            else
                echo "Steam closed successfully on attempt $i."
                return 0  # Exit the function successfully
            fi
        else
            echo "Steam is not running. No need to close it."
            return 0  # Steam is not running, so exit successfully
        fi
    done

    # If the loop completes without successfully closing Steam
    echo "Failed to close Steam after $max_retries attempts."
    return 1  # Exit the function with an error
}

# Function to configure Steam and add images
configure_steam_and_images() {
    APP_NAME=$1
    FLATPAK_REPO=$2

    # Ensure APP_NAME is provided
    if [ -z "$APP_NAME" ] || [ -z "$FLATPAK_REPO" ]; then
        echo "Usage: $0 <app-name> <flatpak-repo>"
        exit 1
    fi

    # Check if Steam is running and close it if it is
    close_steam

    # Get the absolute path to the Python script
    python_script="scripts/python/steam_integration.py"

    # Run the Python script to configure Steam and add images
    if ! python3 "$python_script" "$APP_NAME" "$FLATPAK_REPO"; then
        echo "Failed to run the Python script."
        exit 1
    fi

    # Restart Steam in a silent mode
    nohup steam > /dev/null 2>&1 &
    echo "Steam restarted."
}

# Example of how to call the function
# configure_steam_and_images "Your App Name" "flatpak.repo"

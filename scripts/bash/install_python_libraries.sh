#!/bin/bash

install_python_libraries() {
    # Check and install python-vdf
    if ! check_package "python-vdf"; then
        install_package "python-vdf"
    fi

    # Check and install python-requests
    if ! check_package "python-requests"; then
        install_package "python-requests"
    fi
}
#!/bin/bash

# Function to check if a package is installed via pacman
check_package() {
    local package=$1
    if pacman -Q "$package" &>/dev/null; then
        echo "$package is already installed."
        return 0
    else
        echo "$package is not installed."
        return 1
    fi
}

# Function to install a package via pacman
install_package() {
    local package=$1
    echo "Installing $package..."
    sudo pacman -Syu --noconfirm "$package"
}

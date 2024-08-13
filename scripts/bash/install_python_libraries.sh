#!/bin/bash

install_python_libraries() {
  if ! command -v python3-steamgrid &>/dev/null; then
    echo "Python3 Steamgrid not found, installing..."
  sudo pacman -Syu --noconfirm python-steamgrid
    else
    echo "Python3 Steamgrid is already installed."
  fi

  if ! command -v python3-beautifulsoup4 &>/dev/null; then
    echo "Python3 beautifulsoup4 not found, installing..."
    sudo pacman -Syu --noconfirm python-beautifulsoup4
  else
    echo "Python3 beautifulsoup4 is already installed."
  fi

  if ! command -v python3-steam-shortcut &>/dev/null; then
    echo "Python3 steam-shortcut not found, installing..."
    sudo pacman -Syu --noconfirm python-steam-shortcut
  else
    echo "Python3 steam-shortcut is already installed."
  fi

  if ! command -v python3-vdf &>/dev/null; then
    echo "Python3 vdf not found, installing..."
    sudo pacman -Syu --noconfirm python-vdf
  else
    echo "Python3 vdf is already installed."
  fi

  if ! command -v python3-requests &>/dev/null; then
    echo "Python3 requests not found, installing..."
    sudo pacman -Syu --noconfirm python-requests
  else
    echo "Python3 requests is already installed."
  fi
}
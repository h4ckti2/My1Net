#!/bin/bash

read -p "Do you want to install Python 3 ? [y/n]: " answer
if [ "$answer" == "y" ]; then
  sudo apt-get install python3 -y
  sudo apt-get install python3-dev -y
  sudo apt-get install python3-pip -y
  echo "[*] Python 3 has been installed."
else
  echo "[*] Python 3 installation cancelled."
fi

echo "[*] Installing requirements..."
pip3 install -r requirements.txt

pyinstaller --onefile --icon icon\C2.ico Server.py
pyinstaller --onefile --icon icon\EXE.ico Client.py

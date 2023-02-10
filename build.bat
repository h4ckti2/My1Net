@echo off
pyinstaller --onefile --icon icon\C2.ico Server.py
pyinstaller --onefile --icon icon\EXE.ico Client.py

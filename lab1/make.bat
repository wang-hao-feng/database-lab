@echo off
dot -Tpng ER.dot -o ER.png
pyinstaller -F -w -i ./images/avatar_32x32.ico -n lab1 --add-data "./images/avatar_32x32.ico;images" ./code/GUI.py
move .\dist\lab1.exe .\lab1.exe
del .\lab1.spec
rd /s /q .\dist
del /f /s /q .\build\lab1\*.*
rd /s /q .\build\lab1
rd /s /q .\build
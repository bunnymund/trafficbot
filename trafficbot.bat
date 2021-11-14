@echo off
set PYDIR="E:\CodeLabs\Python\trafficbot"
cmd /k "cd /d %PYDIR% && venv\Scripts\activate.bat && python trafficbot.py "watchlist.txt" --hidden"
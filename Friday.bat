:wait
timeout /t 1 >nul
ping -n 1 google.com|find "TTL">nul
if errorlevel 1 goto wait


@echo off

D:\Python-projects\Personal_assistant\.venv\Scripts\python.exe D:\Python-projects\Personal_assistant\Friday.py

@pause
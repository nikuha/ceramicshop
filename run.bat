@ECHO OFF
start cmd.exe "cd C:\Users\user\PycharmProjects\ceramic-server && venv\Scripts\python ceramicshop\manage.py runserver"
start C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe "http://127.0.0.1:8000/"
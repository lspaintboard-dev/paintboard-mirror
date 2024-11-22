@echo off
start runjs.bat
:s
python manage.py runserver [::]:80
goto s
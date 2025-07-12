# vimo
2nd version



Vimo AI

Установка на Windows 10/11

    Установка гита: https://git-scm.com/

git clone https://github.com/ZhangaliMalikazhdar/vimo.git

    Установка фронта: https://nodejs.org/

    Установка бэкенда Django

на директории: ../vimo/ ->

python3 -m venv env

надо войти в витруальную среду:

env\Scripts\activate

pip install -r requirements.txt

cd back

python manage.py runserver 0.0.0.0:8000

паралельно запускаем фронт:

cd front

npm i

npm run build


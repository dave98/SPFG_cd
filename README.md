[Sgpf - Django]
======================
[Sgpf - Django]: https://github.com/dave98/SPFG_cd 

- [Installation](#installation-developer)
- [Introduction](#introduction)
- [Sgpf](#sgpf)

# Installation-Developer #

## Django ##
    1. sudo apt-get update
    2. python-pip
        2.1. sudo apt-get install python-pip   [python 2]
        2.2. sudo apt-get install python3-pip  [python 3]
    3. django
        3.1. sudo pip install django==1.9
        3.2. sudo pip3 install django==1.9
    4. django-admin --version
    5. project django-admin startproject            

## Postgres ##
    1. sudo pip install psycopg2

## MyCash ## 
    1. git clone https://github.com/dave98/SPFG_cd Sgpf    
    2. cd Sgpd/Code/sgpf    
    3. python manage.py createsuperuser
    4. python manage.py runserver
    5. web url
        5.1 localhost:8000/admin
        5.2 localhost:8000/mycash

## DataBase ##    
    1. python manage.py makemigrations mycash
    2. python manage.py migrate
    
# Introduction #    
    
# Sgpf #

* * *
[Percy Maldonado Quispe UCSP](https://github.com/percy00010)
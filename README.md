### Overview
API built with Django Rest Framework

### Demo
Here is a working live demo: https://api-images-project.herokuapp.com/
Admin user was already created with credentials: username='admin', password='Pass1212'.
### Technology
Python 3.9.7.
djangorestframework 3.12.4

### Usage
This api requires a token to be passed in a header in order to get access to certain endpoints.
Passing token in a header is a secure way to provide authentication in contrast to providing it directly in url.
To pass token into to header, you can make a curl request or use chrome extension "ModHeader"
```
Authorization : Token 0f7a6d428f59cea39c5cefb9c271435890b80fee
```
### Testing
If you wish to create new users via admin panel, remember to generate Token and add UserPlan. 


### Installation

First clone the repository from Github and switch to the new directory:
```
$ git clone https://github.com/wwlodar/api-images.git
$ cd api-images
```
Activate the virtualenv for your project.

Install project dependencies:
```
$ pip install -r requirements.txt
```
Set environment variable
```
DJANGO_SETTINGS_MODULE=config.settings.development
```
Make migrations:
```
$ python manage.py migrate
```
Load created AccountTiers:
```
$ python manage.py loaddata fixtures.json
```
Create admin user:
```
$ python manage.py createsuperuser
```
Run project: 
```
$ python manage.py runserver
```

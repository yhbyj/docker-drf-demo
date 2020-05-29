## TDD docker-drf-demo
参考：[londonappdeveloper](https://www.londonappdeveloper.com/product/build-a-backend-rest-api-with-python-django-advanced/)
环境：windows 10 + docker desktop
### docker  djangorestframework demo
```text
requirements.txt: django(3.0.6), djangorestframework(3.11.0)
Dockerfile
docker-compose.yml
```
```commandline
docker-compose build
docker-compose run docker-drf-demo sh -c "django-admin startproject demo ."
```
### flake8 and Travis-CI
```text
requirements.txt: flake8>=3.8.2,<3.9.0
.flake8
.travis.yml
```
### TDD: admin 
```commandline
docker-compose run docker-drf-demo sh -c "python manage.py startapp core"
docker-compose run docker-drf-demo sh -c "python manage.py makemigrations core"
docker-compose run docker-drf-demo sh -c "python manage.py test && flake8"
```
### django depends_on postgres
```text
requirements.txt: psycopg2>=2.7.5,<2.8.0
Dockerfile
docker-compose.yml
```
```commandline
docker-compose run docker-drf-demo sh -c "python manage.py createsuperuser"
```
### user app
```commandline
docker-compose run docker-drf-demo sh -c "python manage.py startapp user"
```
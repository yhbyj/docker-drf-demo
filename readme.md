## docker-drf-demo
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
.flake8
.travis.yml
```
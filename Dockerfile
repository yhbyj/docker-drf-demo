FROM python:3.7-alpine
MAINTAINER 6887993@qq.com

ENV PYTHONUNBUFFERED 1

#替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN mkdir /project

WORKDIR /project

COPY  ./ /project

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /project/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
#RUN pip install -r /project/requirements.txt

RUN apk del .tmp-build-deps

RUN adduser -D user

USER user

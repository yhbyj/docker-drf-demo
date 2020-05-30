FROM python:3.7-alpine
MAINTAINER 6887993@qq.com

ENV PYTHONUNBUFFERED 1

#替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
COPY  ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN apk del .tmp-build-deps

RUN mkdir /project
WORKDIR /project
COPY  ./ /project

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user

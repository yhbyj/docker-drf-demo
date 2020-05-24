FROM python:3.7-alpine
MAINTAINER 6887993@qq.com

ENV PYTHONUNBUFFERED 1

RUN mkdir /project

WORKDIR /project

COPY  ./ /project

# RUN pip install -r /project/requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install -r /project/requirements.txt

RUN adduser -D user

USER user

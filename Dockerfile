FROM python:3.9-slim

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install imagemagick -y
COPY ./imagemagick/policy.xml /etc/ImageMagick-6/policy.xml

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src

RUN mkdir out
RUN mkdir sources

CMD [ "python", "src/main.py" ]
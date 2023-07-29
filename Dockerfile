FROM python:slim

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install imagemagick -y
COPY ./imagemagick/policy.xml /etc/ImageMagick-6/policy.xml

COPY src/requirements.txt ./src/
RUN pip install -r src/requirements.txt

COPY src ./src

RUN mkdir out
RUN mkdir sources

CMD [ "python", "src/main.py" ]
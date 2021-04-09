# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /home/ubuntu/project01/SuperShop-v02

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk update \
#    && apk add gcc

#RUN apk update \
#    && apk add --no-cache build-base cairo-dev cairo cairo-tools gcc \
#    postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev freetype-dev \
#    lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN apk update \
    && apk upgrade \
    && apk add --no-cache build-base cairo-dev cairo cairo-tools gcc \
    postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev freetype-dev \
    lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libffi-dev pango-dev \
    gdk-pixbuf

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/home/ubuntu/project01/SuperShop-v02/entrypoint.sh"]

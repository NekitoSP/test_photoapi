FROM python:3.8
WORKDIR /src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=photoapi.settings

COPY . .
RUN pip install -e .

RUN ["chmod", "+x", "createsuperuser.sh"]
RUN ["chmod", "+x", "runserver.sh"]
RUN ["chmod", "+x", "runtests.sh"]


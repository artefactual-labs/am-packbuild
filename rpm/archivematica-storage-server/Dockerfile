FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV TARBALL_URL https://github.com/artefactual/archivematica-storage-service/archive/qa/0.x.tar.gz
ENV SRC /src/archivematica-storage-service

RUN apt-get update && \
    apt-get --yes install unar rsync git rpm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${SRC} /var/log/archivematica/storage-service && \
    touch /var/log/archivematica/storage-service/storage_service.log && \
    touch /var/log/archivematica/storage-service/storage_service_debug.log && \
    git clone -b qa/0.x --single-branch https://github.com/artefactual/archivematica-storage-service ${SRC} && \
    pip install --upgrade pip && \
    echo "gunicorn" >> ${SRC}/requirements/production.txt && \
    pip install rpmvenv

#Ugly hack, remove linked file from other repo
RUN rm /src/archivematica-storage-service/storage_service/static/js/vendor/base64.js
#RUN cd ${SRC} && git submodule init

ADD config.json ${SRC}/

ENV PYTHONPATH /src/archivematica-storage-service/storage_service
ENV DJANGO_SETTINGS_MODULE storage_service.settings.production

FROM python:3.8-slim

RUN \
    set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
    python3-pip \
    build-essential \
    python3-venv \
    ffmpeg \
    git \
    ; \
    rm -rf /var/lib/apt/lists/*


WORKDIR /code
RUN pip3 install -U pip && pip3 install -U wheel && pip3 install -U setuptools==59.5.0
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm -r /tmp/requirements.txt

RUN apt-get update
RUN apt-get install -y locales
RUN sed -i -e 's/# uk_UA.UTF-8 UTF-8/uk_UA.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL uk_UA.UTF-8
ENV LANG uk_UA.UTF-8
ENV LANGUAGE uk_UA:uk

COPY . /code/core

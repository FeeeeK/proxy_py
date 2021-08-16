FROM python:3.8-slim

RUN apt-get update \
    && apt-get install -y wget unzip libxml2 libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /proxy_py

RUN echo "Building proxy_py..."

COPY . /proxy_py/
RUN cp config_examples/settings.py proxy_py/settings.py
RUN echo "Installing dependencies..."
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 55555

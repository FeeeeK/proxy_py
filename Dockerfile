FROM python:3.8-slim

WORKDIR /proxy_py
RUN apt update && apt install -y gcc
RUN echo "Installing dependencies..."
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

RUN echo "Building proxy_py..."
COPY . /proxy_py/
RUN cp config_examples/settings.py proxy_py/settings.py

EXPOSE 55555

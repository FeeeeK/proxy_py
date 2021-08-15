FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y wget unzip libxml2 libpq-dev
RUN rm -rf /var/lib/apt/lists/*


WORKDIR /proxy_py

RUN echo "Building proxy_py..."

COPY . /proxy_py/
RUN python3 -m venv env
RUN cp config_examples/settings.py proxy_py/settings.py
RUN echo "Installing dependencies..."
RUN source ./env/bin/activate
RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 55555

FROM python:3.8-slim

WORKDIR /proxy_py

RUN echo "Building proxy_py..."

COPY . /proxy_py/
RUN cp config_examples/settings.py proxy_py/settings.py
RUN echo "Installing dependencies..."
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 55555

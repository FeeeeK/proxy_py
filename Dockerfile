FROM python:3.7-slim

RUN apt-get update \
	&& apt-get install -y wget unzip \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm /bin/sh \
	&& ln -s /bin/bash /bin/sh \
	&& groupadd -r user \
	&& useradd --create-home --no-log-init -r -g user user \
	&& mkdir /proxy_py \
	&& chown user:user /proxy_py

WORKDIR /proxy_py
USER user

RUN echo "Downloading proxy_py sources..." \
	&& wget https://github.com/feeeek/proxy_py/archive/my.zip -O sources.zip 2> /dev/null \
	&& unzip sources.zip && rm sources.zip \
	&& mv proxy_py-*/.[!.]* ./ && mv proxy_py-*/* ./ \
	&& rmdir proxy_py-* \
	&& python3 -m venv env \
	&& cp config_examples/settings.py proxy_py/settings.py \
	&& echo "Installing dependencies..." \
	&& source ./env/bin/activate \
	&& pip3 install -r requirements.txt --no-cache-dir

EXPOSE 55555

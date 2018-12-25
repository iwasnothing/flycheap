FROM ubuntu:latest

RUN apt-get update \
&& apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip \
&& apt-get -y install git \
&& mkdir -p /app /opt \
&& cd /app \
&& git clone https://github.com/iwasnothing/flycheap.git \
&& apt-get -y install wget \
&& wget https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip \
&& wget http://ftp.cuhk.edu.hk/pub/packages/apache.org//jmeter/binaries/apache-jmeter-5.0.tgz \
&& apt-get -y install unzip \
&& unzip chromedriver_linux64.zip \
&& tar -zxvf apache-jmeter-5.0.tgz -C /opt \
&& pip install -r flycheap/requirements.txt

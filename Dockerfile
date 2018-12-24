FROM python:3.6-alpine
RUN git clone
COPY requirements.txt /
RUN pip install -r /requirements.txt

FROM python:3.6-alpine
RUN git clone https://github.com/iwasnothing/flycheap.git
RUN wget https://chromedriver.storage.googleapis.com/index.html?path=2.45/
RUN unzip chromedriver_linux64.zip
RUN pip install -r requirements.txt

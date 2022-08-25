FROM python:3.8
ENTRYPOINT []
RUN pip3 install --no-cache --upgrade pip && pip3 install --no-cache rasa
COPY requirements.txt /
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . /app/
RUN rasa train
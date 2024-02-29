FROM python:3.11

LABEL maintainer="Ahmad Syarif Pudin <ahmadsp60@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
COPY ./app /app
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD [ "python", './app/main.py' ]
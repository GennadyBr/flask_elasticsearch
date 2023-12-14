FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip3 install --no-cache-dir --upgrade pip \
     && pip3 install --no-cache-dir -r requirements.txt

COPY . /app

#CMD python loader.py; python app.py
CMD python loader.py; gunicorn --bind 0.0.0.0:5000 app:app
#CMD python loader.py; gunicorn --bind 0.0.0.0:5000 main:app
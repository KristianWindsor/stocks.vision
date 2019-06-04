FROM python:3.6

RUN apt-get update
RUN apt-get install -y vim

COPY src /app/
COPY requirements.txt /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt
RUN pip3 install "git+https://github.com/mikeboers/Flask-ACL"

CMD python /app/app.py
FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y vim telnet

COPY src /app/
COPY requirements.txt /app/

WORKDIR /app/

RUN pip3 install -r requirements.txt
RUN pip3 install "git+https://github.com/mikeboers/Flask-ACL"

ENTRYPOINT ["/app/entrypoint.sh"]
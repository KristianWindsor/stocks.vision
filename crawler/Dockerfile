FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
	apt-get install -y telnet

COPY src /app/
WORKDIR /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
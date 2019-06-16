FROM python:3.7

ENV PYTHONUNBUFFERED=0

COPY src /app/
WORKDIR /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
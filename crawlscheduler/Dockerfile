FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

COPY src /app/
WORKDIR /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3","/app/app.py"]
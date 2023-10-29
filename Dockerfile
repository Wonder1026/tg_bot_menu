FROM python:3.11.6-alpine3.17

WORKDIR /app

COPY . /app

RUN apk add tesseract-ocr
RUN pip install -r requirements.txt


CMD ["/app/main.py"]
ENTRYPOINT ["python"]
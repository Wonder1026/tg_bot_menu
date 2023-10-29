FROM python:3.11.6-alpine3.17

WORKDIR /app

RUN wget https://github.com/Wonder1026/tg_bot_menu/archive/refs/heads/master.zip -O master.zip
RUN unzip master.zip -d /app
RUN apk add tesseract-ocr
RUN pip install -r /app/tg_bot_menu-master/requirements.txt
RUN ls -la /app

CMD ["/app/tg_bot_menu-master/main.py"]
ENTRYPOINT ["python"]
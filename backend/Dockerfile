FROM python:3.11-slim

WORKDIR /app

COPY /src/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY /src /app
EXPOSE 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
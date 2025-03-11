FROM python:3.11-slim

WORKDIR /app

COPY /src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /src /app
EXPOSE 8000

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENTRYPOINT ["./start.sh"]
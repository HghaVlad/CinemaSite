FROM python:3.11-slim

WORKDIR /app

COPY /src/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY /src /app
EXPOSE 8000

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["python3", "main.py"]
CMD ["sh", "start.sh"]
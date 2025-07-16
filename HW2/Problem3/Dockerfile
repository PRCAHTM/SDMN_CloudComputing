# -------- Dockerfile ----------
FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY server.py /app/
#If needed COPY requirements.txt /app/

EXPOSE 8000
CMD ["python", "server.py"]

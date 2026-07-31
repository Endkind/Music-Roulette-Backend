FROM python:3.12-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=80
ENV ENV=production

EXPOSE 80

CMD ["python", "main.py"]

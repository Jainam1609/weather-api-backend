FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=True
ENV PORT=8080

EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "app:app"]
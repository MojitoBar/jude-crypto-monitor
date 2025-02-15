FROM python:3.9-alpine

WORKDIR /app

# Alpine에는 기본적으로 필요한 빌드 도구들이 없어서 추가 설치 필요
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir six kafka-python

COPY src/consumer /app/consumer

CMD ["python", "-u", "consumer/price_alert_consumer.py"] 
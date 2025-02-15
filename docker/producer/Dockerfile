# 빌드 스테이지
FROM python:3.9-alpine as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/producer ./producer

# 실행 스테이지
FROM python:3.9-alpine

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY src/producer ./producer

CMD ["python", "-u", "producer/coinbase_producer.py"] 
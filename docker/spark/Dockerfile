FROM bitnami/spark:latest

USER root

# 필요한 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y curl && \
    mkdir -p /root/.postgresql && \
    rm -rf /var/lib/apt/lists/*

# PostgreSQL JDBC 드라이버 다운로드
RUN curl -O https://jdbc.postgresql.org/download/postgresql-42.2.18.jar && \
    mv postgresql-42.2.18.jar /opt/bitnami/spark/jars/

# SSL 인증서 디렉토리 생성
RUN mkdir -p /root/.postgresql

# 필요한 Python 패키지 설치
COPY requirements-spark.txt /app/requirements-spark.txt
RUN pip install -r /app/requirements-spark.txt

# 애플리케이션 코드 복사
COPY src/spark /app/spark

# Spark 애플리케이션 실행을 위한 진입점 설정
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.postgresql:postgresql:42.2.18", "/app/spark/price_processor.py"] 






















# 🪙 실시간 암호화폐 가격 모니터링 시스템

## 💡 프로젝트 소개

Coinbase API를 통해 실시간 암호화폐 가격 데이터를 수집하고, Apache Kafka와 Spark Streaming을 활용하여 데이터를 처리하며, PostgreSQL에 저장하고 Grafana로 시각화하는 실시간 모니터링 시스템을 구축했습니다.

## 🔧 기술 스택

### Data Pipeline
- **Apache Kafka**: 실시간 데이터 스트리밍
- **Apache Spark**: 스트리밍 데이터 처리
- **Python**: 데이터 수집 및 처리
- **TimescaleDB (PostgreSQL)**: 시계열 데이터 저장

### Infrastructure
- **Docker Compose**: 컨테이너 기반 인프라 구축
- **Grafana**: 실시간 데이터 시각화
- **SSL**: 보안 통신

## 🎯 프로젝트 구조

### 디렉토리 구조
```
project/
├── docker/
│   ├── consumer/
│   │   └── Dockerfile
│   ├── producer/
│   │   └── Dockerfile
│   ├── spark/
│   │   └── Dockerfile
│   └── postgres/
│       ├── postgresql.conf
│       ├── pg_hba.conf
│       └── ssl/
├── src/
│   ├── consumer/
│   │   └── price_alert_consumer.py
│   ├── producer/
│   │   └── coinbase_producer.py
│   └── spark/
│       └── price_processor.py
├── grafana/
│   └── provisioning/
├── docker-compose.yml
└── README.md
```

### 시스템 아키텍처
```
[Coinbase API] → [Kafka Producer] → [Kafka] → [Spark Streaming] → [TimescaleDB] → [Grafana Dashboard]
                                          ↓
                                  [Price Alert Consumer]
```

## 📊 주요 컴포넌트

### 1. Producer
- Coinbase API로부터 실시간 가격 데이터 수집
- Kafka 토픽으로 데이터 전송
- 경량화된 Alpine 기반 컨테이너

### 2. Spark Streaming
- Kafka 토픽에서 데이터 스트림 처리
- PostgreSQL에 데이터 저장
- SSL 보안 연결 구성

### 3. Price Alert Consumer
- 실시간 가격 변동 모니터링
- 1분 단위 가격 변동 분석
- 임계값 기반 가격 변동 알림

### 4. 데이터 시각화
- Grafana 대시보드를 통한 실시간 모니터링
- 시계열 기반 가격 추이 분석
- 커스텀 알림 설정

![Image](https://github.com/user-attachments/assets/1c4b1aaa-9bb1-4025-884a-c3a5a2750d78)

## 🚀 주요 성과

- 실시간 데이터 파이프라인 구축
- 컨테이너 기반의 확장 가능한 아키텍처 구현
- SSL을 통한 보안 강화
- 효율적인 시계열 데이터 처리

## 🎓 학습 내용

- 실시간 데이터 스트리밍 아키텍처 설계
- Docker를 활용한 마이크로서비스 구축
- 시계열 데이터베이스 활용
- 보안 설정 및 SSL 인증서 관리

## ⚠️ 트러블슈팅

## 📝 회고

이 프로젝트를 통해 실시간 데이터 처리 시스템의 전체 아키텍처를 설계하고 구현하는 경험을 했습니다. 특히 데이터의 실시간성, 시스템 안정성, 그리고 확장성을 고려한 설계의 중요성을 배웠습니다. 앞으로는 더 복잡한 실시간 데이터 처리 시스템과 머신러닝을 결합한 프로젝트를 진행하고 싶습니다.

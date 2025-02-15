# Jude Crypto Monitor Project Plan

## 프로젝트 개요
- **프로젝트 이름**: Jude Crypto Monitor
- **목표**: Coinbase API를 통해 실시간 암호화폐 가격 데이터를 수집하고, Kafka와 Spark Streaming을 사용하여 데이터를 처리한 후 PostgreSQL에 저장하고 Grafana를 통해 시각화합니다.

## 아키텍처
1. **데이터 수집**: Coinbase API를 통해 실시간 암호화폐 가격 데이터를 수집
2. **데이터 스트리밍**: Kafka를 사용하여 데이터를 스트리밍
3. **데이터 처리**: Spark Streaming을 통해 실시간 데이터 처리
4. **데이터 저장**: PostgreSQL에 데이터를 저장
5. **데이터 시각화**: Grafana를 통해 실시간 데이터 시각화

## 단계별 계획

### 1. Docker 환경 설정
- Docker 및 Docker Compose 설치
- 각 서비스(Coinbase API 연동, Kafka, Spark, PostgreSQL, Grafana)를 위한 Dockerfile 및 docker-compose.yml 작성

### 2. Coinbase API 연동
- Coinbase API 가입 및 API 키 발급
- API를 통해 암호화폐 가격 데이터를 가져오는 스크립트 작성

### 3. Kafka 설정
- Kafka 설치 및 설정
- Kafka 토픽 생성
- Coinbase API 데이터를 Kafka로 전송하는 프로듀서 구현

### 4. Spark Streaming 설정
- Spark 설치 및 설정
- Kafka에서 데이터를 수신하여 처리하는 Spark Streaming 애플리케이션 작성

### 5. PostgreSQL 데이터베이스 설정
- PostgreSQL 설치 및 데이터베이스/테이블 생성
- Spark Streaming 데이터를 PostgreSQL에 저장하는 로직 구현

### 6. Grafana 설정 및 시각화
- Grafana 설치 및 PostgreSQL 연결
- 실시간 데이터를 시각화할 대시보드 생성

### 7. 테스트 및 디버깅
- 각 단계별 테스트 진행
- 데이터 수집, 처리, 저장, 시각화의 정확성 확인

### 8. 문서화 및 최적화
- 프로젝트 문서화
- 성능 최적화 및 추가 기능 구현
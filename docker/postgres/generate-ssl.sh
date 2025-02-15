#!/bin/bash
# SSL 인증서 생성 스크립트

# 인증서 저장 디렉토리 생성
mkdir -p docker/postgres/ssl

# 개인키 생성
openssl genrsa -out docker/postgres/ssl/server.key 2048
chmod 600 docker/postgres/ssl/server.key

# 인증서 서명 요청(CSR) 생성
openssl req -new -key docker/postgres/ssl/server.key -out docker/postgres/ssl/server.csr -subj "/CN=postgres"

# 자체 서명된 인증서 생성
openssl x509 -req -in docker/postgres/ssl/server.csr -signkey docker/postgres/ssl/server.key -out docker/postgres/ssl/server.crt 
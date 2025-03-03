FROM apache/airflow:2.5.1

USER root

# PostgreSQL 클라이언트 라이브러리(libpq) 최신 버전 설치
RUN apt-get update && apt-get install -y libpq-dev

# airflow 사용자의 권한을 유지한 상태에서 패키지 설치
USER airflow

# psycopg2 최신 버전 설치
RUN pip install --no-cache-dir --upgrade psycopg2-binary
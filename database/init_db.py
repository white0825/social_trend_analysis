import psycopg2
import os
import yaml

# config.yaml 파일 경로 설정
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.yaml")

# config.yaml 읽기
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

DB_CONFIG = config["database"]

# PostgreSQL 연결
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"]
    )
    return conn

# 테이블 생성 함수
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # schema.sql 실행
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as file:
        schema_sql = file.read()
        cursor.execute(schema_sql)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL 스키마 적용 완료")

if __name__ == "__main__":
    create_tables()
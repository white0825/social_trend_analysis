import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 DAG 디렉토리
INIT_SCRIPT_PATH = os.path.join(BASE_DIR, "../database/init_db.py")  # DB 초기화 스크립트 경로

def run_init_db():
    """init_db.py 실행"""
    result = subprocess.run(["python3", INIT_SCRIPT_PATH], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

# DAG 설정
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 3),
    "retries": 1
}

dag = DAG(
    dag_id="init_db",
    default_args=default_args,
    schedule_interval=None,  # 수동 실행
    catchup=False
)

# PythonOperator를 사용하여 init_db.py 실행
init_db_task = PythonOperator(
    task_id="run_init_db_script",
    python_callable=run_init_db,
    dag=dag
)

init_db_task
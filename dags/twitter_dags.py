from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
import os
import requests

# 환경 변수에서 Twitter API Bearer Token 가져오기
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# PostgreSQL 연결 정보
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "social_trends")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin123")

# Twitter API v2 검색 함수
def fetch_tweets(query, max_results=50):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query,
        "tweet.fields": "created_at,public_metrics,text,lang",
        "max_results": max_results
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error fetching tweets:", response.text)
        return pd.DataFrame()
    tweets = response.json().get("data", [])
    return pd.DataFrame([
        {
            "post_id": tweet["id"],
            "created_at": tweet["created_at"],
            "content": tweet["text"],
            "retweets": tweet["public_metrics"]["retweet_count"],
            "likes": tweet["public_metrics"]["like_count"],
            "language": tweet.get("lang", "en")
        }
        for tweet in tweets
    ])

# PostgreSQL 저장 함수
def save_to_postgres():
    df = fetch_tweets("trump", max_results=1)
    if df.empty:
        print("No tweets fetched.")
        return
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO social_media_posts (platform, post_id, username, content, post_date, likes, retweets, language)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (post_id) DO NOTHING;
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                "Twitter",  # platform
                row["post_id"],
                None,  # Twitter API v2에서는 username 제공 안 함
                row["content"],
                row["created_at"],
                row["likes"],
                row["retweets"],
                row["language"]
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print("Tweets saved to PostgreSQL successfully.")
    except Exception as e:
        print("Error saving tweets to PostgreSQL:", e)

# Airflow DAG 정의
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 8),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "twitter_data_pipeline",
    default_args=default_args,
    description="Fetch Twitter data and store in PostgreSQL",
    schedule_interval=timedelta(minutes=10),
    catchup=False,
)

fetch_and_store_task = PythonOperator(
    task_id="fetch_and_store_tweets",
    python_callable=save_to_postgres,
    dag=dag,
)

fetch_and_store_task
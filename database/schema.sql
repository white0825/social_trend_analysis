-- 소셜 미디어 크롤링 데이터 테이블
CREATE TABLE IF NOT EXISTS social_media_posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255),
    content TEXT NOT NULL,
    hashtags TEXT[],
    post_date TIMESTAMP NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    comments INT DEFAULT 0,
    language VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 감성 분석 결과 테이블
CREATE TABLE IF NOT EXISTS sentiment_analysis_results (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255) REFERENCES social_media_posts(post_id) ON DELETE CASCADE,
    sentiment_label VARCHAR(10) CHECK (sentiment_label IN ('positive', 'neutral', 'negative')),
    sentiment_score FLOAT CHECK (sentiment_score >= -1 AND sentiment_score <= 1),
    keyword TEXT NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tweets (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) DEFAULT 'Twitter',
    tweet_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255),
    text TEXT NOT NULL,
    hashtags TEXT[],
    created_at TIMESTAMP NOT NULL,
    likes INT DEFAULT 0,
    retweets INT DEFAULT 0,
    comments INT DEFAULT 0,
    language VARCHAR(10),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

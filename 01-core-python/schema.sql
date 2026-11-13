CREATE DATABASE agent_db;

-- Connect to agent_db before running these tables.

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mcqs (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_answer CHAR(1) NOT NULL,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO posts(title, content)
VALUES ('Python List Comprehension',
        'List comprehension provides a concise way to create lists in Python. It can contain an expression followed by a for loop and optional condition.');

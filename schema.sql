CREATE TABLE users (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(200) NOT NULL,
  last_name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,

  UNIQUE(email)
) CHARACTER SET 'utf8mb4' ENGINE=InnoDB ROW_FORMAT=DYNAMIC;

CREATE TABLE sources (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  uri TEXT NOT NULL,
  title TEXT NOT NULL,
  rss_uri TEXT NOT NULL,
  icon_path TEXT NOT NULL,
  latestlink_fetched TEXT NULL,
  created_at TIMESTAMP NOT NULL

) CHARACTER SET 'utf8mb4' ENGINE=InnoDB ROW_FORMAT=DYNAMIC;

CREATE TABLE articles (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  uri TEXT NOT NULL,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  source_id INT NOT NULL REFERENCES sources(id),
  published_at TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
) CHARACTER SET 'utf8mb4' ENGINE=InnoDB ROW_FORMAT=DYNAMIC;

CREATE TABLE subscriptions (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  source_id INTEGER REFERENCES sources(id),
  created_at TIMESTAMP NOT NULL,

  UNIQUE(user_id, source_id)
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC;

CREATE TABLE user_favouritearticles (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  article_id INTEGER REFERENCES articles(id),
  created_at TIMESTAMP NOT NULL,

  UNIQUE(user_id, article_id)
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC;
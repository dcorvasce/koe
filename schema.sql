CREATE TABLE users (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(200) NOT NULL,
  last_name VARCHAR(200) NOT NULL,
  email VARCHAR(200) NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,

  UNIQUE(email)
);

CREATE TABLE sources (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  uri VARCHAR(1024) NOT NULL,
  title TEXT NOT NULL,
  rss_uri TEXT NOT NULL,
  icon_path TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,

  UNIQUE(uri)
);

CREATE TABLE articles (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  uri VARCHAR(2048) NOT NULL,
  title TEXT NOT NULL,
  preview TEXT NOT NULL,
  category VARCHAR(200) NOT NULL DEFAULT 'General',
  source_id INTEGER NOT NULL REFERENCES sources(id),
  published_at DATETIME NOT NULL,
  created_at TIMESTAMP NOT NULL,

  UNIQUE(uri)
);

CREATE TABLE subscriptions (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  source_id INTEGER REFERENCES sources(id),
  created_at TIMESTAMP NOT NULL,

  UNIQUE(user_id, source_id)
);

CREATE TABLE user_favouritearticles (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  article_id INTEGER REFERENCES articles(id),
  created_at TIMESTAMP NOT NULL,

  UNIQUE(user_id, article_id)
);
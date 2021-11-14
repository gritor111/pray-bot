CREATE TABLE IF NOT EXISTS users (
  username VARCHAR NOT NULL,
  pray_count INT DEFAULT 0,
  user_id BIGINT
  current_xp INT
  level INT 
)

CREATE TABLE IF NOT EXISTS pray_logs (
  username VARCHAR NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE,
  user_id BIGINT
)
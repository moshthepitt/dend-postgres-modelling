"""SQL queries module."""
# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays (
  songplay_id SERIAL UNIQUE NOT NULL,
  start_time TIMESTAMP NOT NULL,
  user_id VARCHAR NOT NULL,
  level VARCHAR NOT NULL,
  song_id VARCHAR NOT NULL,
  artist_id VARCHAR NOT NULL,
  session_id BIGINT NOT NULL,
  location VARCHAR NOT NULL,
  user_agent VARCHAR NOT NULL,
  PRIMARY KEY (songplay_id)
);
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users (
  user_id  VARCHAR UNIQUE NOT NULL,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  gender VARCHAR NOT NULL,
  level VARCHAR NOT NULL,
  PRIMARY KEY (user_id)
);
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs (
  song_id VARCHAR UNIQUE NOT NULL,
  title VARCHAR NOT NULL,
  artist_id VARCHAR NOT NULL,
  year INT NULL,
  duration NUMERIC NOT NULL,
  PRIMARY KEY (song_id)
);
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists (
  artist_id VARCHAR UNIQUE NOT NULL,
  name VARCHAR NOT NULL,
  location VARCHAR NULL,
  latitude NUMERIC NULL,
  longitude NUMERIC NULL,
  PRIMARY KEY (artist_id)
);
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time (
  id SERIAL UNIQUE NOT NULL,
  start_time TIMESTAMP NOT NULL,
  hour VARCHAR NOT NULL,
  day VARCHAR NOT NULL,
  week VARCHAR NOT NULL,
  month VARCHAR NOT NULL,
  year INT NOT NULL,
  weekday VARCHAR NOT NULL,
  PRIMARY KEY (id)
);
"""

# INSERT RECORDS

songplay_table_insert = """
"""

user_table_insert = """
"""

song_table_insert = """
INSERT INTO songs (
  song_id,
  title,
  artist_id,
  year,
  duration
)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (song_id) DO UPDATE
SET
  title=EXCLUDED.title,
  artist_id=EXCLUDED.artist_id,
  year=EXCLUDED.year,
  duration=EXCLUDED.duration;
"""

artist_table_insert = """
INSERT INTO artists (
  artist_id,
  name,
  location,
  latitude,
  longitude
)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (artist_id) DO UPDATE
SET
  name=EXCLUDED.name,
  location=EXCLUDED.location,
  latitude=EXCLUDED.latitude,
  longitude=EXCLUDED.longitude;
"""


time_table_insert = """
"""

# FIND SONGS

song_select = """
"""

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]

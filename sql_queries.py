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
  start_time TIMESTAMP NOT NULL,
  user_id VARCHAR NOT NULL,
  level VARCHAR NOT NULL,
  song_id VARCHAR NULL,
  artist_id VARCHAR NULL,
  session_id BIGINT NOT NULL,
  location VARCHAR NOT NULL,
  user_agent VARCHAR NOT NULL,
  -- the assumption is that start_time and user_id are unique together
  PRIMARY KEY (start_time, user_id),
  CONSTRAINT fk_songplays_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_songplays_artists
    FOREIGN KEY (artist_id)
    REFERENCES artists (artist_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_songplays_songs
    FOREIGN KEY (song_id)
    REFERENCES songs (song_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_songplays_time
    FOREIGN KEY (start_time)
    REFERENCES time (start_time)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users (
  user_id VARCHAR,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  gender VARCHAR NOT NULL,
  level VARCHAR NOT NULL,
  PRIMARY KEY (user_id)
);
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs (
  song_id VARCHAR,
  title VARCHAR NOT NULL,
  artist_id VARCHAR NOT NULL,
  year INT NULL,
  duration NUMERIC NOT NULL,
  PRIMARY KEY (song_id)
);
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists (
  artist_id VARCHAR,
  name VARCHAR NOT NULL,
  location VARCHAR NULL,
  latitude NUMERIC NULL,
  longitude NUMERIC NULL,
  PRIMARY KEY (artist_id)
);
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time (
  start_time TIMESTAMP NOT NULL,
  hour VARCHAR NOT NULL,
  day VARCHAR NOT NULL,
  week VARCHAR NOT NULL,
  month VARCHAR NOT NULL,
  year INT NOT NULL,
  weekday VARCHAR NOT NULL,
  PRIMARY KEY (start_time)
);
"""

# INSERT RECORDS

songplay_table_insert = """
INSERT INTO songplays (
  start_time,
  user_id,
  level,
  song_id,
  artist_id,
  session_id,
  location,
  user_agent
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time, user_id) DO UPDATE
SET
  start_time=EXCLUDED.start_time,
  user_id=EXCLUDED.user_id,
  level=EXCLUDED.level,
  song_id=EXCLUDED.song_id,
  artist_id=EXCLUDED.artist_id,
  session_id=EXCLUDED.session_id,
  location=EXCLUDED.location,
  user_agent=EXCLUDED.user_agent;
"""

user_table_insert = """
INSERT INTO users (
  user_id,
  first_name,
  last_name,
  gender,
  level
)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (user_id) DO UPDATE
SET
  first_name=EXCLUDED.first_name,
  last_name=EXCLUDED.last_name,
  gender=EXCLUDED.gender,
  level=EXCLUDED.level;
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
INSERT INTO time (
  start_time,
  hour,
  day,
  week,
  month,
  year,
  weekday
)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time) DO UPDATE
SET
  hour=EXCLUDED.hour,
  day=EXCLUDED.day,
  week=EXCLUDED.week,
  month=EXCLUDED.month,
  year=EXCLUDED.year,
  weekday=EXCLUDED.weekday;
"""

# FIND SONGS

song_select = """
SELECT
  songs.song_id AS song_id,
  artists.artist_id AS artist_id
FROM songs
LEFT JOIN artists
  ON songs.artist_id = artists.artist_id
WHERE
  songs.title = %s
  AND artists.name = %s
  AND songs.duration = %s;
"""

# QUERY LISTS

create_table_queries = [
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
    songplay_table_create,
]
drop_table_queries = [
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
    songplay_table_drop,
]

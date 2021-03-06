"""etl module."""
import glob
import os

import pandas as pd
import psycopg2

from sql_queries import (
    artist_table_insert,
    song_select,
    song_table_insert,
    songplay_table_insert,
    time_table_insert,
    user_table_insert,
)


def process_song_file(cur, filepath):
    """Process song file and store in DB.

    This function takes a song's filepath and does:
        - cleans it by replacing any occurrences of `nan` with None
        - replacing instances where year=0 with year=None
        - inserts it into the artist table

    Arguments:
        cur - pycopg2 cursor object
        filepath - the filepath to the song file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    # replace nan with None
    df = df.where((pd.notnull(df)), None)
    # replace 0 year with None
    df.year = df.year.replace({0: None})
    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0]  # noqa
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ]
    ].values[0]
    cur.execute(artist_table_insert, artist_data)


def store_time_data(cur, time_dataframe):
    """Store time data.

    Arguments:
        cur - pycopg2 cursor object
        time_data - pandas dataframe containing time data
    """
    column_labels = ["start_time", "hour", "day", "week", "month", "year", "weekday"]  # noqa
    time_df = pd.DataFrame(data=time_dataframe.values, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


def store_user_data(cur, user_dataframe):
    """Store user data.

    Arguments:
        cur - pycopg2 cursor object
        user_dataframe - pandas dataframe containing user data
    """
    # insert user records
    for i, row in user_dataframe.iterrows():
        cur.execute(user_table_insert, row)


def store_songplay_data(cur, songplay_dataframe):
    """Store songplay data.

    This function simply takes in a pandas dataframe containing songplay data,
    it then extracts songplay data and inserts it into the songplay table using
    the provided psycopg2 cursor object.

    Arguments:
        cur - pycopg2 cursor object
        songplay_dataframe - pandas dataframe containing songplay data
    """
    # insert user records
    for index, row in songplay_dataframe.iterrows():

        # get song_id and artist_id from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        song_id, artist_id = results if results else None, None

        # insert songplay record
        songplay_data = (
            pd.to_datetime(row.ts, unit="ms"),
            row.userId,
            row.level,
            song_id,
            artist_id,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_log_file(cur, filepath):
    """Process and store log file data.

    This function takes a filepath to a songplay log file and does this:
        - cleans it by replacing any occurrences of `nan` with None
        - filters out any records where page != NextSong
        - converts the timestamp (field name is ts) to a datetime object
        - extracts hour, day, week, month, year and weekday from timestamp
        - stores the time information to the time table

    Arguments:
        cur - pycopg2 cursor object
        filepath - the filepath to the log file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)
    # replace nan with None
    df = df.where((pd.notnull(df)), None)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit="ms")

    # insert time data records
    time_data = pd.concat(
        [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday], axis=1  # noqa
    )
    store_time_data(cur, time_data)

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    store_user_data(cur, user_df)

    # insert songplay records
    store_songplay_data(cur, df)


def process_data(cur, conn, filepath, func):
    """
    Process all the data.

    This function goes through all the log and song files and processes them
    for storage into the data warehouse.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    """Run main.

    When this is run, the Python code in this module is executed
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

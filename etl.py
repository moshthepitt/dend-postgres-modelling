"""etl module."""
import glob
import json
import os

# import pandas as pd
import psycopg2

from sql_queries import artist_table_insert, song_table_insert


def process_song_file(cur, filepath):
    """Process song file and store in DB."""
    # open song file
    with open(filepath, "r") as file:
        data = json.load(file)

        # insert song record
        song_data = (
            data["song_id"],
            data["title"],
            data["artist_id"],
            data["year"],
            data["duration"],
        )
        cur.execute(song_table_insert, song_data)

        # insert artist record
        artist_data = (
            data["artist_id"],
            data["artist_name"],
            data["artist_location"],
            data["artist_latitude"],
            data["artist_longitude"],
        )
        cur.execute(artist_table_insert, artist_data)


# def process_log_file(cur, filepath):
#     # open log file
#     df =

#     # filter by NextSong action
#     df =

#     # convert timestamp column to datetime
#     t =

#     # insert time data records
#     time_data =
#     column_labels =
#     time_df =

#     for i, row in time_df.iterrows():
#         cur.execute(time_table_insert, list(row))

#     # load user table
#     user_df =

#     # insert user records
#     for i, row in user_df.iterrows():
#         cur.execute(user_table_insert, row)

#     # insert songplay records
#     for index, row in df.iterrows():

#         # get songid and artistid from song and artist tables
#         results = cur.execute(
#             song_select, (row.song, row.artist, row.length))
#         songid, artistid = results if results else None, None

#         # insert songplay record
#         songplay_data =
#         cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Process all the data."""
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Run main."""
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    # process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()

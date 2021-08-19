import string
import random
import psycopg2
from psycopg2 import extras
import pandas as pd
from datetime import datetime, timedelta
from config import config
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Database filling application')
parser.add_argument('--releases', '-r', default=0, type=int, help='number of releases to insert')
parser.add_argument('--artists', '-a', default=0, type=int, help='number of artists to insert')
parser.add_argument('--countries', '-c', default=0, type=int, help='number of countries to insert')
parser.add_argument('--labels', '-l', default=0, type=int, help='number of labels to insert')
parser.add_argument('--genres', '-g', default=0, type=int, help='number of genres to insert')
parser.add_argument('--charts', '-ch', default=0, type=int, help='number of charts to insert')
parser.add_argument('--artists_have_releases', '-ahr', default=0, type=int,
                    help='number of connections between artists and releases; not guaranteed')
parser.add_argument('--charts_have_releases', '-chr', default=0, type=int,
                    help='number of connections between charts and releases; not guaranteed')
parser.add_argument('--countries_have_artists', '-cha', default=0, type=int,
                    help='number of connections between countries and artists; not guaranteed')
parser.add_argument('--genres_have_releases', '-ghr', default=0, type=int,
                    help='number of connections between genres and releases; not guaranteed')
parser.add_argument('--labels_have_artists', '-lha', default=0, type=int,
                    help='number of connections between labels and artists; not guaranteed')
args = parser.parse_args()
releases_number = args.releases
artists_number = args.artists
countries_number = args.countries
labels_number = args.labels
genres_number = args.genres
charts_number = args.charts
artists_have_releases_number = args.artists_have_releases
charts_have_releases_number = args.charts_have_releases
countries_have_artists_number = args.countries_have_artists
genres_have_releases_number = args.genres_have_releases
labels_have_artists_number = args.labels_have_artists

origin = ['studio', 'live', 'compilation', None]
release_type = ['album', 'single', 'track']
issue = ['original', 'reissue', 'remaster', None]
status = ['released', 'upcoming']

dates = pd.date_range('1950-01-01', datetime.now(), freq='D')  # big array of dates
future_dates = pd.date_range(datetime.now() + timedelta(days=1), '2030-01-01', freq='D')  # big array of future dates


def generate_data(releases, artists, countries, labels, genres, charts, artists_have_releases, charts_have_releases,
                  countries_have_artists, genres_have_releases, labels_have_artists):
    # read connection parameters
    params = config()
    con = psycopg2.connect(**params)

    print("Database opened successfully")
    cur = con.cursor()

    # generate releases
    arguments = []
    statement = '''INSERT INTO music_database_release (id, name, date, origin, release_type, issue, status)
           VALUES (default, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'''
    for i in range(1, releases + 1):

        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        release_type_to_insert = random.choice(release_type)
        issue_to_insert = random.choice(issue)
        status_to_insert = random.choices(status, weights=[0.95, 0.05], k=1)[0]

        if release_type_to_insert == 'track':
            origin_to_insert = random.choice([origin[0], origin[1], None])
        else:
            origin_to_insert = random.choice(origin)

        if status_to_insert == 'released':
            date = random.choice(dates)
        else:
            date = random.choice(future_dates)

        arguments.append((name, date, origin_to_insert, release_type_to_insert, issue_to_insert, status_to_insert))
    if releases > 0:
        # page_size – maximum number of argslist items to include in every statement.
        # If there are more items the function will execute more than one statement.
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=releases)
        con.commit()  # commit inserts to database so data could be used in subsequent operations

    # update related field
    arguments = []
    statement = "UPDATE music_database_release SET related_id = (%s) WHERE id = (%s)"
    cur.execute("SELECT id FROM music_database_release WHERE release_type = 'album' or release_type = 'single';")
    albums_and_singles = cur.fetchall()
    cur.execute("SELECT id FROM music_database_release WHERE release_type = 'track';")
    tracks = cur.fetchall()
    if len(albums_and_singles) > 0 and len(tracks) > 0:
        # about 20% of existing tracks will be related to some albums and singles
        related_tracks = random.sample(tracks, k=int(len(tracks) * 0.2))  # sample for unique id's
        if len(related_tracks) > 0:
            for track in related_tracks:
                arguments.append((random.choice(albums_and_singles), track))
            psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=len(related_tracks))

    # generate countries
    arguments = []
    statement = "INSERT INTO music_database_country (id, name) VALUES (default , %s) ON CONFLICT DO NOTHING;"
    for i in range(1, countries + 1):
        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        arguments.append((name,))
    if countries > 0:
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=countries)

    # generate artists
    arguments = []
    statement = "INSERT INTO music_database_artist (id, name) VALUES (default, %s) ON CONFLICT DO NOTHING;"
    for i in range(1, artists + 1):
        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        arguments.append((name,))
    if artists > 0:
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=artists)

    # generate labels
    arguments = []
    statement = "INSERT INTO music_database_label (id, name) VALUES (default, %s) ON CONFLICT DO NOTHING;"
    for i in range(1, labels + 1):
        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        arguments.append((name,))
    if labels > 0:
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=labels)

    # generate genres
    arguments = []
    statement = "INSERT INTO music_database_genre (id, name) VALUES (default, %s) ON CONFLICT DO NOTHING;"
    for i in range(1, genres + 1):
        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        arguments.append((name,))
    if genres > 0:
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=genres)

    # generate charts
    arguments = []
    statement = "INSERT INTO music_database_chart (id, name) VALUES (default, %s) ON CONFLICT DO NOTHING;"
    for i in range(1, charts + 1):
        name = ''.join(random.choices(list(string.ascii_letters + string.digits), k=random.randint(1, 50)))
        arguments.append((name,))
    if charts > 0:
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=charts)

    con.commit()  # commit inserts to database so data could be used in subsequent operations

    # generate many-to-many connections between countries and artists
    arguments = []
    statement = "INSERT INTO music_database_artist_countries (country_id, artist_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    cur.execute("SELECT id FROM music_database_country;")
    countries_to_connect = cur.fetchall()
    cur.execute("SELECT id FROM music_database_artist;")
    artists_to_connect = cur.fetchall()
    if len(artists_to_connect) > 0 and len(countries_to_connect) > 0 and countries_have_artists > 0:
        for i in range(1, countries_have_artists + 1):
            arguments.append((random.choice(countries_to_connect), random.choice(artists_to_connect)))
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=countries_have_artists)

    # generate many-to-many connections between artists and releases
    arguments = []
    statement = "INSERT INTO music_database_release_artists (artist_id, release_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    cur.execute("SELECT id FROM music_database_release;")
    releases_to_connect = cur.fetchall()
    if len(releases_to_connect) > 0 and len(artists_to_connect) > 0 and artists_have_releases > 0:
        for i in range(1, artists_have_releases + 1):
            arguments.append((random.choice(artists_to_connect), random.choice(releases_to_connect)))
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=artists_have_releases)

    # generate many-to-many connections between genres and releases
    arguments = []
    statement = "INSERT INTO music_database_release_genres (genre_id, release_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    cur.execute("SELECT id FROM music_database_genre;")
    genres_to_connect = cur.fetchall()
    if len(genres_to_connect) > 0 and len(releases_to_connect) > 0 and genres_have_releases > 0:
        for i in range(1, genres_have_releases + 1):
            arguments.append((random.choice(genres_to_connect), random.choice(releases_to_connect)))
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=genres_have_releases)

    # generate many-to-many connections between labels and artists
    arguments = []
    statement = '''INSERT INTO music_database_labelshaveartists (label_id, artist_id, date_from, date_to) 
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;'''
    cur.execute("SELECT id FROM music_database_label;")
    labels_to_connect = cur.fetchall()
    if len(labels_to_connect) > 0 and len(artists_to_connect) > 0 and labels_have_artists > 0:
        for i in range(1, labels_have_artists + 1):
            date_from = random.choice(dates)
            possible_dates = np.concatenate((dates[dates >= date_from], future_dates), axis=None)
            # 9 to 1 distribution from suitable dates or None in case of life contract
            date_to = pd.to_datetime(random.choices([random.choice(possible_dates), None], weights=[0.9, 0.1], k=1)[0])
            arguments.append((random.choice(labels_to_connect), random.choice(artists_to_connect), date_from, date_to))
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=labels_have_artists)

    # generate many-to-many connections between charts and releases
    arguments = []
    statement = '''INSERT INTO music_database_chartshavereleases (chart_id, release_id, date, position) 
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;'''
    cur.execute("SELECT id FROM music_database_chart;")
    charts_to_connect = cur.fetchall()
    cur.execute("SELECT id, date FROM music_database_release WHERE music_database_release.status = 'released';")
    released_releases = cur.fetchall()
    if len(charts_to_connect) > 0 and len(released_releases) > 0 and charts_have_releases > 0:
        for i in range(1, charts_have_releases + 1):
            # determine the id of the release we want to connect with chart:
            release = random.choice(released_releases)
            release_date = pd.to_datetime(release[1])
            # choose date from dates which is no less that release date:
            date_to_chose_from = dates[dates >= release_date]
            date = random.choice(date_to_chose_from)
            arguments.append((random.choice(charts_to_connect), release[0], date, random.randint(1, 100)))
        psycopg2.extras.execute_batch(cur=cur, sql=statement, argslist=arguments, page_size=charts_have_releases)

    print("Data generated successfully")
    con.commit()
    print("Records inserted successfully")
    con.close()


generate_data(releases=releases_number, artists=artists_number, labels=labels_number, charts=charts_number,
              countries=countries_number, genres=genres_number,
              artists_have_releases=artists_have_releases_number, charts_have_releases=charts_have_releases_number,
              countries_have_artists=countries_have_artists_number,
              labels_have_artists=labels_have_artists_number, genres_have_releases=genres_have_releases_number)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
from datetime import datetime
import pandas as pd
import json
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler


def job_task():
    # reading spotify auth information from configure.json

    with open("configure.json") as conf:
        data = json.load(conf)

    cid = data['cid']
    secret = data['secret']
    redirect_uri = data['redirect_uri']
    csv_location = data['csv_location']

    # fetching the data from spotify api

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope='user-read-recently-played', client_id=cid, client_secret=secret,
                                  redirect_uri=redirect_uri))


    results = sp.current_user_recently_played(limit=50)['items']

    # parsing the info into a dataframe

    # - name of the artist
    name = np.array([results[i]['track']['artists'][0]['name'] for i in range(len(results))])
    # - name of the track
    track_name = np.array([results[i]['track']['name'] for i in range(len(results))])
    # - date
    dat = np.array([str(datetime.strptime(results[i]['played_at'], "%Y-%m-%dT%H:%M:%S.%fZ"))[:-3] for i in range(len(results))])
    # - genre
    genre = np.array(["none" if len(sp.artist(results[i]['track']['artists'][0]['id'])['genres']) ==0 else sp.artist(results[i]['track']['artists'][0]['id'])['genres'][0] for i in range(len(results))])
    # - image
    imag = np.array([results[i]['track']['album']['images'][0]['url'] for i in range(len(results))])
    df_new = pd.DataFrame({"nam": name, "track": track_name, "dat": dat, "genre": genre, 'imag' : imag})

    # deserializing the csv

    df = None

    try:
        f = open(csv_location)
        df = pd.read_csv(csv_location)
    except IOError:
        pass

    # adding infos
    # - if the dataframe doesn't exist
    if df is None:
        df = df_new
        print("Creation of the .csv !")
    # -if the dataframe exists
    else:
        for i in range(len(df_new["dat"])):
            if len(df[:][df["dat"] == df_new["dat"][i]]) == 0:
                print("Successfuly added "+df_new[:].loc[i].nam+" to the list")
                df = df.append(
                    {"nam": df_new[:].loc[i].nam, "dat": df_new[:].loc[i].dat, "track": df_new[:].loc[i].track, "genre":df_new[:].loc[i].genre, "imag":df_new[:].loc[i].imag},
                    ignore_index=True)
    # reserializing the csv
    df.to_csv(csv_location, index=False)


parser = argparse.ArgumentParser()
parser.add_argument("start", help="Start : start the bot, ctrl-c to end it.", type=str, choices=["start"])
args = parser.parse_args()
print("Spotihisbot launched !! Ctrl-C to kill me :)")
if args.start == "start":
    scheduler = BlockingScheduler()
    scheduler.add_job(job_task, 'interval', minutesc=1)
    scheduler.start()



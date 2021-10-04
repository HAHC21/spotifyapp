# Import libraries
from flask import Flask, jsonify, redirect, render_template, request, session
from flask.json.tag import TaggedJSONSerializer
import requests, json, pandas
from bs4 import BeautifulSoup as soup
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Define app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Global storage of data
QUERYDATA = None

albums_filter = []
artists_filter = []
songs_filtered = []
songs_artists_filtered = []
songs_albums_filtered = []

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        title = request.form.get('title')

        url = "https://unsa-unofficial-spotify-api.p.rapidapi.com/search"

        querystring = {"query":f"{title}","count":"2", "type":"tracks"}

        headers = {
            'x-rapidapi-host': "unsa-unofficial-spotify-api.p.rapidapi.com",
            'x-rapidapi-key': "4ce7fb66fbmsh75f27b6cb5e1416p13155djsn7869b3c397e0"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        songs_response = json.loads(response.text)

        songs_data = songs_response["Results"]

        songs_filtered.clear()
        albums_filter.clear()
        artists_filter.clear()

        for song in songs_data:
            song_name = song["name"]
            album_name = song["album"]["name"]
            album_cover = song["album"]["images"][0]["url"]
            artist_name = song["album"]["artists"][0]["name"]
            spotify_link = song["external_urls"]["spotify"]

            songs_filtered.append({"song_name":f"{song_name}", "album_name":f"{album_name}", "album_cover":f"{album_cover}", "artist_name":f"{artist_name}", "spotify_link":f"{spotify_link}"})
            
            if album_name in albums_filter:
                pass
            else:
                albums_filter.append(album_name)      
            
            if artist_name in artists_filter:
                pass
            else:
                artists_filter.append(artist_name)

        return render_template("results.html", title = title, songs=songs_filtered, albums_filter=albums_filter, artists_filter=artists_filter)

    else:
        return render_template("index.html")

@app.route("/filter_by_artist", methods=["POST"])
def artists():
    if request.method == "POST":
        artist = request.form.get('artist')
        title = request.form.get('title')

        songs_artists_filtered.clear()
        albums_filter.clear()
        artists_filter.clear()

        for song in songs_filtered:
            if artist == song["artist_name"]:
                songs_artists_filtered.append(song)
                albums_filter.append(song["album_name"])
        
        artists_filter.append(artist)


        return render_template("results.html", title = title, songs = songs_artists_filtered, albums_filter=albums_filter, artists_filter=artists_filter)


@app.route("/filter_by_album", methods=["POST"])
def albums():
    if request.method == "POST":
        album = request.form.get('album')
        title = request.form.get('title')

        songs_albums_filtered.clear()
        albums_filter.clear()
        artists_filter.clear()

        for song in songs_filtered:
            if album == song["album_name"]:
                songs_albums_filtered.append(song)
                artists_filter.append(song["artist_name"])
        
        albums_filter.append(album)

        return render_template("results.html", title = title, songs = songs_albums_filtered, albums_filter=albums_filter, artists_filter=artists_filter)
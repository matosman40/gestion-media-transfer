from flask import Flask, render_template, request, redirect
import os, shutil, requests
from config import *

app = Flask(__name__)


def get_radarr_movies():
    url = f"{RADARR_URL}/api/v3/movie?apikey={RADARR_APIKEY}"
    return requests.get(url).json()


def get_sonarr_series():
    url = f"{SONARR_URL}/api/v3/series?apikey={SONARR_APIKEY}"
    return requests.get(url).json()


@app.route("/")
def index():
    movies = get_radarr_movies()
    series = get_sonarr_series()
    return render_template("index.html", movies=movies, series=series)


@app.route("/transfer", methods=["POST"])
def transfer():
    item_path = request.form.get("path")

    src = os.path.join(MEDIA_PATH, item_path)
    dest = os.path.join(EXTERNAL_DISK, os.path.basename(item_path))

    if os.path.exists(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
        if DELETE_AFTER_COPY:
            shutil.rmtree(src)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

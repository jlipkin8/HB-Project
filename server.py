from flask import Flask, render_template, jsonify, request
from model import *

app = Flask(__name__)

@app.route("/")
def homepage(): 
    """Show homepage with map""" 

    return render_template("home_map.html")


@app.route("/coordinates")
def grab_coordinates():
    coordinates = []
    rows = db.session.query(Artpiece.dimensions).all()
    for row in rows: 
        lng = float(row[0][0])
        lat = float(row[0][1])
        coordinates.append((lat,lng))
    return jsonify(coordinates)

@app.route("/artistnames")
def return_artistnames(): 
    names = []
    rows = db.session.query(Artist.name).all()
    for row in rows: 
        names.append(row[0])

    return jsonify(names)

@app.route("/pieces-by-artist", methods=['POST'])
def return_artpieces_by_artist():
    artistname = request.form.get("artist")
    print artistname
    artist = Artist.query.filter(Artist.name == artistname).first()
    artist_id = artist.artist_id 
    artpieces = ArtistArtpiece.query.filter(ArtistArtpiece.artist_id == artist_id).all()
    art = []
    for ap in artpieces:
        info = {}
        info["title"] = ap.artpiece.title 
        lat = float(ap.artpiece.dimensions[0])
        lng = float(ap.artpiece.dimensions[1])
        info["coords"] = [lat,lng]
        art.append(info)

    return {"results": art}

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")
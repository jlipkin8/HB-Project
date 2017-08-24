from flask import Flask, render_template, jsonify, request
from model import *

app = Flask(__name__)

@app.route("/")
def homepage(): 
    """Show homepage with map""" 

    return render_template("home_map.html")


@app.route("/pieces.json")
def return_pieces():
    artpieces = Artpiece.query.all()
    art = []

    for ap in artpieces:
        info = {}
        names = []
        artists = ap.artists
        for artist in artists: 
            names.append(artist.name)

        info["artist"] = names
        info["title"] = ap.title 

        lat = float(ap.coords[0])
        lng = float(ap.coords[1])
        info["coords"] = [lat,lng]
        info["timeperiod"] =  ap.timeperiod
        medium = ap.medium
        if medium: 
            info["med_desc"] = ap.medium.medium_desc
        creditline = ap.creditline
        # import pdb; pdb.set_trace()
        if creditline:
            print creditline.creditline_name
            info["creditline"] = creditline.creditline_name
        info["loc_desc"] = ap.loc_desc
        art.append(info)

    return jsonify({"results": art})

@app.route("/artistnames")
def return_artistnames(): 
    names = []
    rows = db.session.query(Artist.name).all()
    for row in rows: 
        names.append(row[0])

    return jsonify(names)

@app.route("/pieces-by-artist.json")
def return_artpieces_by_artist():
    artistname = request.args.get("artist")
    print artistname
    artist = Artist.query.filter(Artist.name == artistname).first()
    artpieces = artist.artpieces
    art = []
    for ap in artpieces:
        info = {}
        print ap.title
        info["title"] = ap.title 

        lat = float(ap.coords[0])
        lng = float(ap.coords[1])
        info["coords"] = [lat,lng]
        info["timeperiod"] =  ap.timeperiod
        info["med_desc"] = ap.medium.medium_desc
        creditline = ap.creditline
        # import pdb; pdb.set_trace()
        if creditline: 
            info["creditline"] = creditline.creditline_name
        info["loc_desc"] = ap.loc_desc
        art.append(info)

    return jsonify({"results": art})

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")

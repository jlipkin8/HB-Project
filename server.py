from flask import Flask, render_template, jsonify
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
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def homepage(): 
    """Show homepage with map""" 

    return render_template("home_map.html")


@app.route("/art-pieces")
def artpiece_info():
    """JSON info about artpieces"""
    return jsonify({'markers':[{"name": "Mural", "lat": 37.7478586, "lng": -122.4556651}, 
                   {"name": "Sculpture", "lat": 37.7419071, "lng": -122.4650348}, 
                   {"name": "Drawing", "lat": 37.8085303, "lng": -122.4120591}]})
    

if __name__ == "__main__": 
    app.run(host="0.0.0.0")
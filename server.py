from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage(): 
    """Show homepage with map""" 

    return render_template("home_map.html")


if __name__ == "__main__": 
    app.run(host="0.0.0.0")
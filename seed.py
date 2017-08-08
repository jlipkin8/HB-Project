"""Utility file to seed arts database from sfdata website """

import requests 
from sqlalchemy import fun 

from model import * 

################################################################################
"""Get art data from SF data """

# got this code snippet from https://dev.socrata.com/foundry/data.sfgov.org/bm46-8iwk
url = "https://data.sfgov.org/resource/bm46-8iwk.json"

response = requests.get(url)

if response.status_code == 200: 
    #returns a list of objects 
    sf_data = response.json()

################################################################################
def load_artist(): 
    """Load artists from sf_data into database.""" 

    print "Artists"

    sf_data_len = len(sf_data)
    for i in range(sf_data_len): 
        artist = sf_data[i]['artist']
        lname, fname = artist.split(",")
        artist = Artist(lname=lname, fname=fname)
        db.session.add(artist)

    db.session.commit()
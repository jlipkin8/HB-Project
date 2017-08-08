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
DATA_LEN = len(sf_data)

def load_artists(): 
    """Load artists from sf_data into database.""" 

    print "Artists"

    for i in range(DATA_LEN): 
        artist = sf_data[i]['artist']
        lname, fname = artist.split(",")
        artist = Artist(lname=lname, fname=fname)
        db.session.add(artist)

    db.session.commit()


def create_load_decades(): 
    """Create decades from a for-loop""" 



def load_media(): 
    """Load media from sf_data into database. """ 

    print "Media"

    for i in range(DATA_LEN): 
        medium = sf_data[i]['medium']
        db.session.add(medium)

    db.session.commit()


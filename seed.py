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


def create_timeperiods(): 
    """Create timeperiods from a for-loop""" 

    print "Timeperiods"

    start_period = 0 
    end_period = 1700 

    while end_period < 2021: 
        timeperiod = (start_period, end_period)
        db.session.add(timeperiod)
        temperiod = end_period
        start_period = temperiod + 1 

        if start_period < 1901: 
            end_period = end_period + 100 
        else: 
            end_period = end_period + 10
             

    db.session.commit()




def load_media(): 
    """Load media from sf_data into database. """ 

    print "Media"

    for i in range(DATA_LEN): 
        medium = sf_data[i]['medium']
        db.session.add(medium)

    db.session.commit()


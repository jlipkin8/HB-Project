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

create_timeperiods()

for i in range(DATA_LEN):
    # load one row in Artist 
    load_artist(sf_data[i])
    #load one row in Artpiece 
    load_artpiece(sf_data[i]) 
    #load one row in Creditline 
    load_creditline(sf_data[i])
    #load one row in media
    load_medium(sf_data[i])
# end of for-loop 

################################################################################
# function definitions

def load_artist(sf_datum): 
    """Load artist from sf_data into database.""" 

    name = sf_datum['artist']
    if name: 
        artist = Artist(name=name)
        db.session.add(artist)

    db.session.commit()


def load_artpiece(sf_datum): 
    pass


def load_creditline(sf_datum):
    """Load creditline from sf_data into database"""
    
    creditline_name = sf_datum['credit_line']
    if creditline_name: 
        creditline = Creditline(creditline_name=creditline_name)
        db.session.add(creditline)

    db.session.commit()











def create_timeperiods(): 
    """Create timeperiods from a for-loop""" 

    print "Timeperiods"

    start_period = 0 
    end_period = 1700 

    while end_period < 2021: 
        timeperiod = Timeperiod(start_period=start_period, end_period=end_period)
        db.session.add(timeperiod)
        start_period = end_period + 1 

        if start_period < 1901: 
            end_period = end_period + 100 
        else: 
            end_period = end_period + 10

    db.session.commit()

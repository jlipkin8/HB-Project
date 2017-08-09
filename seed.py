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

    # might want to re-think splitting up the name
    # might be harder to account for Uniqueness
    # for i in range(DATA_LEN): 
    #     artist = sf_data[i]['artist']
    #     lname, fname = artist.split(",")
    #     artist = Artist(lname=lname, fname=fname)
    #     db.session.add(artist)

    for i in range(DATA_LEN): 
        artist = sf_data[i]['artist']
        artist = Artist(name=name)
        db.session.add(artist)

    db.session.commit()


def load_artpieces(): 
    """Load artpieces from sf_data into database""" 

    print "Artpieces"

    for i in range(DATA_LEN): 
        #get artist id 
        artist_name = sf_data[i]['artist']
        artist = Artist.query.filter(Artist.name == artist_name).first()
        artist_id = artist["artist_id"]

        #get timeperiod id
        timeperiod = sf_data[i].get('created_at', None)
        if timeperiod is not None: 
            timeperiod = timeperiod[:4]
            timeperiod = int(timeperiod)

        tperiod_query =  Timeperiod.query.filter((Timeperiod.start_period <= timeperiod) 
                                                  & (Timeperiod.end_period >= timeperiod))
        tperiod = tperiod_query.first()
        toeruid_id = tperiod['timeperiod_id']

        #get medium id 
        medium = sf_data[i].get('medium', None)
        #maybe there is an id associated with None
        if medium is not None: 
            medium_query = Medium.query.filter(Medium.medium_desc == medium)
            medium_object = medium_query.first() 
            medium_id = medium_object['medium_id']

        #get dimensions 

        #get location desc 

        #get title 

        #get creditline


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


def load_creditlines(): 
    """Load creditlines from sf_data into database.""" 

    print "Creditlines"

    for i in range(DATA_LEN): 
        creditline_name = sf_data[i]['credit_line']
        if creditline_name: 
            creditline = Creditline(creditline_name=creditline_name)
            db.session.add(creditline)

    db.session.commit()
    

def load_media(): 
    """Load media from sf_data into database. """ 

    print "Media"

    for i in range(DATA_LEN): 
        medium = sf_data[i]['medium']
        if medium: 
            medium = Medium(medium_desc=medium)
            db.session.add(medium)

    db.session.commit()


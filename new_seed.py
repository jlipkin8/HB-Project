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

    #load obe row in ArtistArtpiece
    load_artist_artpiece(sf_data[i])
    
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
    """Load artpiece from sf_data into database."""

    #get artist id 
    artist_name = sf_datum['artist']
    artist = Artist.query.filter(Artist.name == artist_name).first()
    artist_id = artist["artist_id"]
    
    #get timeperiod id
    timeperiod = sf_datum.get('created_at', None)
    if timeperiod is not None: 
        timeperiod = timeperiod[:4]
        timeperiod = int(timeperiod)

    tperiod_query =  Timeperiod.query.filter((Timeperiod.start_period <= timeperiod) 
                                              & (Timeperiod.end_period >= timeperiod))
    tperiod = tperiod_query.first()
    tperiod_id = tperiod['timeperiod_id']

    #get medium id 
    medium = sf_datum.get('medium', None)
    #maybe there is an id associated with None
    if medium: 
        medium_query = Medium.query.filter(Medium.medium_desc == medium)
        medium_object = medium_query.first() 
        medium_id = medium_object['medium_id']

    #get dimensions 

    #get location desc
    loc_desc = sf_datum.get('location_description', '')

    #get title 
    title = sf_datum.get('title', '')

    #get creditline
    creditline = sf_datum.get('credit_line', '')
    if creditline: 
        credit_line= Creditline.query.filter(Creditline.creditline_name == creditline).first()
        creditline_id = credit_line['creditline_id']


def load_creditline(sf_datum):
    """Load creditline from sf_data into database."""

    creditline_name = sf_datum['credit_line']
    if creditline_name: 
        creditline = Creditline(creditline_name=creditline_name)
        db.session.add(creditline)

    db.session.commit()


def load_artist_artpiece(sf_datum): 
    """Load artist and artpiece from sf_data into database"""

    #retrieve artist_id from Artist table
    artist_name = sf_datum['artist']
    artist = Artist.query.filter(Artist.artist_name == artist_name).first()
    artist_id = artist[artist_id]

    #retrieve artpiece_id from Artpiece table 
    art_title = sf_datum['title']
    art = Artpiece.query.filter(Artpiece.title == art_title).first()
    art_id = art['art_id']

    artistartpiece = ArtistArtPiece(artist_id=artist_id, art_id=art_id)
    db.session.add(artistartpiece)

    db.session.commit()


def load_medium(sf_datum): 
    """Load medium from sf_data into database."""

    medium = sf_datum['medium']
    if medium: 
            medium = Medium(medium_desc=medium)
            db.session.add(medium)

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

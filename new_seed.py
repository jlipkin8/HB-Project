"""Utility file to seed arts database from sfdata website """

import requests 
from sqlalchemy import func

from model import *
import ast


################################################################################
"""Get art data from SF data """

# got this code snippet from https://dev.socrata.com/foundry/data.sfgov.org/bm46-8iwk
url = "https://data.sfgov.org/resource/bm46-8iwk.json"

response = requests.get(url)

if response.status_code == 200: 
    #returns a list of objects 
    sf_data = response.json()

################################################################################
# DATA_LEN = len(sf_data)

# create_timeperiods()

# for i in range(DATA_LEN):
#     # load one row in Artist 
#     load_artist(sf_data[i])

#     #load one row in Artpiece 
#     load_artpiece(sf_data[i])

#     #load one row in Creditline 
#     load_creditline(sf_data[i])

#     #load obe row in ArtistArtpiece
#     load_artist_artpiece(sf_data[i])

#     #load one row in media
#     load_medium(sf_data[i])
# # end of for-loop 

################################################################################
# function definitions


artists = []
def load_artist(sf_datum): 
    """Load artist from sf_data into database.""" 
    print "made it into load_artists"

    name = sf_datum.get('artist', '')
    if (name not in artists) and (name): 
        artists.append(name)
        artist = Artist(name=name)
        db.session.add(artist)

    db.session.commit()


untitled_count = 1; 
def load_artpiece(sf_datum):
    """Load artpiece from sf_data into database."""

    #get artist id 
    artist_name = sf_datum.get('artist', '')
    if artist_name:  
        artist = Artist.query.filter(Artist.name == artist_name).first()
        artist_id = artist.artist_id

    #get timeperiod id
    created_at = sf_datum.get('created_at', '')
    if created_at: 
        time_period = int(created_at[:4])
        time_query =  Timeperiod.query.filter(((Timeperiod.start_period < time_period)
                                            | (Timeperiod.start_period == time_period))
                                            & ((Timeperiod.end_period >  time_period)
                                            | (Timeperiod.end_period == time_period)))
        returned_time_period= time_query.first()
        tperiod_id = returned_time_period.timeperiod_id
    else: 
        tperiod_id = None

    #get medium id 
    medium = sf_datum.get('medium', '')
    #maybe there is an id associated with None

    if medium: 
        medium_query = Medium.query.filter(Medium.medium_desc == medium)
        medium_object = medium_query.first() 
        print medium_object
        mediumid = medium_object.medium_id
    else: 
        mediumid = None

    #get dimensions
    # dimensions = sf_datum['geometry']['coordinates']
    # print "\n"
    dimensions = sf_datum['geometry']
    geo_dict = ast.literal_eval(dimensions)
    coordinates = geo_dict['coordinates']

    #get location desc
    loc_desc = sf_datum.get('location_description', '')

    #get title 
    title = sf_datum.get('title', '')

    #get creditline
    creditline = sf_datum.get('credit_line', '')
    if creditline: 
        credit_line= Creditline.query.filter(Creditline.creditline_name == creditline).first()
        creditline_id = credit_line.creditline_id

    else: 
        creditline_id = None

    # create artpiece instance 
    artpiece = Artpiece(artist_id=artist_id,
                        timeperiod_id=tperiod_id, 
                        medium_id=mediumid, 
                        dimensions=coordinates, 
                        loc_desc=loc_desc, 
                        title=title, 
                        creditline_id=creditline_id)
    db.session.add(artpiece)
    db.session.commit()


    # Get the Max user_id in the database
    result = db.session.query(func.max(Artpiece.art_id)).one()
    max_id = int(result[0])
    load_artist_artpiece(artist_id, max_id)



creditlines = []
def load_creditline(sf_datum):
    """Load creditline from sf_data into database."""

    creditline_name = sf_datum.get('credit_line', '')
    if creditline_name not in creditlines and creditline_name:
        creditlines.append(creditline_name)  
        creditline = Creditline(creditline_name=creditline_name)
        db.session.add(creditline)

    db.session.commit()


#thinking about putting this load function inside the load_artpiece on 
def load_artist_artpiece(artist_id, art_id): 
    """Load artist and artpiece from sf_data into database"""

    artistartpiece = ArtistArtPiece(artist_id=artist_id, art_id=art_id)
    db.session.add(artistartpiece)

    db.session.commit()


media = []
def load_medium(sf_datum): 
    """Load medium from sf_data into database."""

    medium = sf_datum.get('medium', '') 
    if medium and medium not in media:
            media.append(medium)
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


################################################################################

if __name__ == "__main__": 
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()

    # seeding tables with example data 
    example_data = sf_data[10:21]
    EX_LEN = len(example_data)

    create_timeperiods()

    for i in range(EX_LEN): 
        load_artist(example_data[i])
        load_creditline(example_data[i])
        load_medium(example_data[i])
        load_artpiece(example_data[i])


    #testing out create_timeperiods 
    



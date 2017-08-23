"""Utility file to seed arts database from sfdata website """

import requests 
from sqlalchemy import func

from model import *
import ast
import re
import json
import pprint
################################################################################
"""Get art data from SF data """

# got this code snippet from https://dev.socrata.com/foundry/data.sfgov.org/bm46-8iwk
url = "https://data.sfgov.org/resource/bm46-8iwk.json"

response = requests.get(url)

if response.status_code == 200: 
    #returns a list of objects 
    sf_data = response.json()


################################################################################
# function definitions

def create_artist(does_exist, name):
    """Create artist object and add to session""" 

    if not does_exist: 
        # print "I'm in create_artist"
        artist = Artist(name=name)
        db.session.add(artist)
        db.session.commit()


def chck_mult_nms_create_artists(names):
    """Check if name(or something like name) in names exists in database"""

    for name in names: 
        # already_exists = Artist.query.filter(Artist.name.like('%'+ name + '%')).first()
        already_exists = Artist.query.filter(Artist.name == name).first()
        print name
        create_artist(already_exists, name)


def chck_nm_create_artist(name): 
    """Check name if already in database, then create artist"""

    already_exists = Artist.query.filter(Artist.name == name).first()
    create_artist(already_exists, name)
    db.session.commit()


def load_artist(sf_datum): 
    """Load artist from sf_data into database."""

    pattern1 = re.compile("(-?\w)+, (\w)+ and (\w)+, (\w)+") 
    pattern2 = re.compile("(-?\w)+, (\w)+ and (\w)+") 
    pattern3 = re.compile("(\w)+, (\w)+, (\w)+")
    pattern4 = re.compile("(-?\w)+, (\w)+ (\(?\w.?\)?)*")
    pattern5 = re.compile("(-?\w)+,?.? (\w)*")
    pattern6 = re.compile("((\w)+(\/\w+)?), (\w)+((\/\w+))")

    name = sf_datum.get('artist', '')

    if re.match(pattern1, name): 
        # Chamberlain, Ann and Lubell, Bernie
        # print "pattern1"
        name1, name2 = re.split(" and ", name)
        chck_nm_create_artist(name1)
        chck_nm_create_artist(name2)
        return [name1, name2]
    elif re.match(pattern2, name):
        # Cervantes, Morales and Poethig
        # print "pattern2"
        names = name.replace(" and ", ", ")
        names = names.split(", ")
        print names 
        chck_mult_nms_create_artists(names)
        return names
    elif re.match(pattern3, name):
        # print "pattern3"
        # Collins, Goto, Reiko 
        names = name.split(", ")
        chck_mult_nms_create_artists(names)
        return names
    elif re.match(pattern4, name):
        # Chesse, Ralph A.
        # print "pattern4"
        m = re.match(pattern4, name)  
        name = m.group(0)
        chck_nm_create_artist(name)
        return [name]
    elif re.match(pattern5, name):
        # Cheng, Carl
        # print "pattern5"
        m = re.match(pattern5, name)
        name = m.group(0)
        chck_nm_create_artist(name)
        return [name]
    elif re.match(pattern6, name):
        # Cheng/Smith, Carl/Jon
        # print "pattern6"
        names = name.replace("/",",")
        names = names.replace(" ", "")
        print names
        name_match = re.match(r"(?P<f_name> ?\w+,?),(?P<l_name> ?\w+,?),(?P<fname_two> ?\w+,?),(?P<l_name_two> ?\w+)", names)
        print name_match
        names_dict = name_match.groupdict()
        name1 = names_dict["l_name"] + ", " + names_dict["f_name"]
        name2 = names_dict["l_name_two"] + ", " + names_dict["fname_two"]
        chck_nm_create_artist(name1)
        chck_nm_create_artist(name2)
        return [name1, name2]
    else:
        # print "else pattern"
        chck_nm_create_artist(name)
        return [name]

        
    db.session.commit()
    

def load_artpiece(sf_datum):
    """Load artpiece from sf_data into database."""

    #get timeperiod 
    timeperiod = sf_datum.get('created_at', '')

    #get medium id 
    medium = sf_datum.get('medium', '')

    #maybe there is an id associated with None
    if medium: 
        medium_query = Medium.query.filter(Medium.medium_desc == medium)
        medium_object = medium_query.first() 
        # print medium_object
        mediumid = medium_object.medium_id
    else: 
        mediumid = None

    #get coords
    coords = sf_datum.get('geometry')
    geo_dict = json.loads(coords)
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
    # check if there is and artpiece there 
    exists = Artpiece.query.filter(Artpiece.coords == coordinates, 
                                   Artpiece.title == title).first()

    if not exists: 
        artpiece = Artpiece(timeperiod=timeperiod, 
                            medium_id=mediumid, 
                            coords=coordinates, 
                            loc_desc=loc_desc, 
                            title=title, 
                            creditline_id=creditline_id)
        db.session.add(artpiece)
        db.session.commit()


    # Get the Max user_id in the database
    result = db.session.query(func.max(Artpiece.art_id)).one()
    max_id = int(result[0])
    return max_id


def load_creditline(sf_datum):
    """Load creditline from sf_data into database."""

    creditline_name = sf_datum.get('credit_line', '')
    already_exists = Creditline.query.filter(Creditline.creditline_name == creditline_name).first()
    if creditline_name and not already_exists: 
        creditline = Creditline(creditline_name=creditline_name)
        db.session.add(creditline)

    db.session.commit()


def load_artist_artpiece(artist_names, art_id): 
    """Load artist and artpiece from sf_data into database"""

    #get artist's name/names
    # print "---------> ", type(artist_names)
    for name in artist_names: 
        artist = Artist.query.filter(Artist.name == name).first()
        artist_id = artist.artist_id
        already_exists = ArtistArtpiece.query.filter(ArtistArtpiece.artist_id == artist_id,
                                                     ArtistArtpiece.art_id == art_id).first()
        if not already_exists:
             artistartpiece = ArtistArtpiece(artist_id=artist_id, art_id=art_id)
             db.session.add(artistartpiece)

    db.session.commit()


def load_medium(sf_datum): 
    """Load medium from sf_data into database."""

    medium = sf_datum.get('medium', '')
    already_exists = Medium.query.filter(Medium.medium_desc == medium).first() 
    if medium and not already_exists:
            medium = Medium(medium_desc=medium)
            db.session.add(medium)

    db.session.commit()


################################################################################

if __name__ == "__main__": 
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    count = 0; 
    # seeding tables with example data
    # pp = pprint.PrettyPrinter(indent=4)
    example_data = sf_data[405:410]
    EX_LEN = len(example_data)
    SF_LEN = len(sf_data)
    # for i in range(EX_LEN): 
    #     # pp.pprint(example_data[i])
    #     print "$$$$$$$$", count
    #     count = count + 1 
    #     if example_data[i].get(u'_id_') == u"_id" and example_data[i].get("geometry") == u"geometry":
    #         continue
    #     artist_names = load_artist(example_data[i])
    #     load_creditline(example_data[i])
    #     load_medium(example_data[i])
    #     artpiece_id = load_artpiece(example_data[i])
    #     load_artist_artpiece(artist_names, artpiece_id)

    for i in range(SF_LEN): 
        # pp.pprint(example_data[i])d
        # print "$$$$$$$$", count
        count = count + 1 
        if sf_data[i].get(u'_id_') == u"_id" and sf_data[i].get("geometry") == u"geometry":
            continue
        artist_names = load_artist(sf_data[i])
        load_creditline(sf_data[i])
        load_medium(sf_data[i])
        artpiece_id = load_artpiece(sf_data[i])
        load_artist_artpiece(artist_names, artpiece_id)


"""Models and database functions for SF_Art project""" 

from flask_sqlalchemy import SQLAlchmey 

db = SQLAlchmey()


################################################################################
#Model definitions 

class Artist(db.Model)
    """Artist who made an artpiece"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer,
                          autoincrement=True, 
                          primary_key=True)
    lname = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(64), nullable=True)
    
    def __repr__(self): 
        """Provide representation of Artist when printed. """

        return "<Artist artist_id=%s fname=%s lname=%s >" % (self.artist_id,
                                                             self.fname, 
                                                             self.lname)


class Artpiece(db.Model)
    """Artpiece made by an artist"""

    __tablename__ = "artpieces"

    art_id = db.Column(db.Integer,
                          autoincrement=True, 
                          primary_key=True)
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey('artists.artist_id'))

    #should the decade be an auto-incrementing integer or string like '00', '10'
    decade_id = db.Column(db.Integer, 
                          db.ForeignKey('decades.decade_id'))

    medium_id = db.Column(db.Integer, 
                          db.ForeignKey('media.medium_id'))
    dimensions #unsure what the datatype will be ??

    loc_desc = db.Column(db.String(300))
    #would 300 be too long? 

    title = db.Column(db.String(100))

    creditline_id = db.Column(db.String(100), 
                              db.ForeignKey('creditlines.creditline_id'))

    # Define relationship to artist 
    artist = db.relationship("Artist", 
                              backref=db.backref("artpieces"))

    # Define relationship to decade 
    # what goes in as an argument for db.backref
    decade = db.realtionship("Decade", 
                              backref=db.backref("artpiece"))

    def __repr__(self): 
        """Provide representation of an artpiece"""

        return "<Artpiece art_id=%s title=%s >" % (self.art_id, self.title)


class Decade(db.Model)
    
    pass


class Creditline(db.Model)
    """Credit line of an artpiece.""" 

    creditline_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    creditline_name = db.Column(db.String(200))

    def __repr__(self): 
        """Provide respresentation  of a creditline"""


class ArtistArtpiece(db.Model)
    pass


class Medium(db.Model)
    pass


class UserArtpiece(db.Model)
    pass


class User(db.Model)
    pass

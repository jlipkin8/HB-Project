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
    pass


class Decade(db.Model)
    pass


class Creditline(db.Model)
    pass


class ArtistArtpiece(db.Model)
    pass


class Medium(db.Model)
    pass


class UserArtpiece(db.Model)
    pass


class User(db.Model)
    pass

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
    decade = db.realtionship("Decade", 
                              backref=db.backref("artpieces"))

    # Define realtionship to medium 
    medium = db.realtionship("Medium", 
                              backref=db.backref("artpieces"))

    # Define relationship to Creditline
    creditline = db.realtionship("Creditline", 
                                  backref=db.backref("artpieces"))

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

        return "<Creditline creditline_id=%s creditline_name=%s >" % (self.creditline_id,
                                                                      self.creditline_name)


class ArtistArtpiece(db.Model)
    """Arist and an artpiece.""" 

    artist_art_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey('artists.artist_id'))
    art_id = db.Column(db.Integer, 
                       db.ForeignKey('artpieces.art_id'))

    def __repr__(self): 
        """Provide representation of one an artist's artipiece""" 

        return "<ArtistArtpiece artist_art_id=%s>" % (self.artist_art_id)


class Medium(db.Model)
    """Medium of an artpiece."""

    medium_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)

    medium_desc = db.Column(db.String(200))

    def __repr__(self): 
        """Provide respresentation of a medium."""

        return "<Medium medium_id=%s medium_desc=%s >" % (self.medium_id, 
                                                          self.medium_desc) 


class UserArtpiece(db.Model)
    pass


class User(db.Model)
    pass

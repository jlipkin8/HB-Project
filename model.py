"""Models and database functions for SF_Art project""" 
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


################################################################################
#Model definitions 

class Artist(db.Model):
    """Artist who made an artpiece"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer,
                          autoincrement=True, 
                          primary_key=True)
    lname = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(64), nullable=True)
    
    def __repr__(self): 
        """Provide representation of Artist when printed. """

        return "<Artist artist_id={} fname={} lname={} >".format(self.artist_id,
                                                             self.fname, 
                                                             self.lname)


class Artpiece(db.Model):
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
    dimensions = db.Column(db.String(100))

    loc_desc = db.Column(db.String(300))
    #would 300 be too long? 

    title = db.Column(db.String(100))

    creditline_id = db.Column(db.String(100), 
                              db.ForeignKey('creditlines.creditline_id'))


    # Define relationship to artist 
    artist = db.relationship("Artist", 
                              backref=db.backref("artpieces"))

    # Define relationship to decade 
    decade = db.relationship("Decade", 
                              backref=db.backref("artpieces"))

    # Define realtionship to medium 
    medium = db.relationship("Medium", 
                              backref=db.backref("artpieces"))

    # Define relationship to Creditline
    creditline = db.relationship("Creditline", 
                                  backref=db.backref("artpieces"))

    def __repr__(self): 
        """Provide representation of an artpiece"""

        return "<Artpiece art_id={} title={} >".format(self.art_id, self.title)


class Decade(db.Model):
    
    __tablename__ = "decades"

    decade_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self): 
        """Provide representation of a decade."""

        return "<Decade decade_id={} start_date={} end_date={} >".format(
                                                                self.decade_id,
                                                                self.start_date, 
                                                                self.end_date)


class Creditline(db.Model):
    """Credit line of an artpiece.""" 

    __tablename__ = "creditlines"

    creditline_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    creditline_name = db.Column(db.String(200))

    def __repr__(self): 
        """Provide respresentation  of a creditline"""

        return "<Creditline creditline_id={} creditline_name={} >".format(self.creditline_id,
                                                                      self.creditline_name)


class ArtistArtpiece(db.Model):
    """Arist and an artpiece.""" 

    __tablename__ = "artistartpieces"

    artist_art_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey('artists.artist_id'))
    art_id = db.Column(db.Integer, 
                       db.ForeignKey('artpieces.art_id'))

    # Define relationship to Artist 
    artist = db.relationship("Artist", 
                             backref=db.backref("artistartpieces"))
    # Define relationship to Artpiece 
    artipiece = db.realtionship("Artpiece", 
                                backref=db.backref("artistartpieces"))

    def __repr__(self): 
        """Provide representation of one an artist's artipiece""" 

        return "<ArtistArtpiece artist_art_id={}>".format(self.artist_art_id)


class Medium(db.Model):
    """Medium of an artpiece."""

    __tablename__ = "media"

    medium_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)

    medium_desc = db.Column(db.String(200))

    def __repr__(self): 
        """Provide respresentation of a medium."""

        return "<Medium medium_id={} medium_desc={} >".format(self.medium_id, 
                                                          self.medium_desc) 


class UserArtpiece(db.Model):
    """User and an artpiece.""" 

    __tablename__ = "userartpieces"

    user_art_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    art_id = db.Column(db.Integer, 
                       db.ForeignKey('artpieces.art_id'))
    like = db.Column(db.Boolean)

    # Define relationship to user
    user = db.relationship("User", 
                            backref=db.backref("userartpieces"))

    # Define relationship to artpiece 
    artipiece = db.realtionship("Artpiece", 
                                 backref=db.backref("userartpieces"))


    def __repr__(self): 
        """Provide representation of a user and an artpiece.""" 

        return "<UserArtpiece user_art_id={} like={} >".format(self.user_art_id, 
                                                           self.like)

class User(db.Model):
    """User of the art app. """ 

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    user_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(20))
    SF_resident = db.Column(db.Boolean)
    email = db.Column(db.String(75))
    password = db.Column(db.String(75))

    def __repr__(self): 
        """Provide respresentation of a user of the art app. """

        return "<User user_id={} user_name={} email={} >".format(self.user_id, 
                                                                 self.user_name, 
                                                                 self.email)


    

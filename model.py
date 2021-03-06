"""Models and database functions for SF_Art project""" 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


################################################################################
#Model definitions 

class Artist(db.Model):
    """Artist. An artist has many artpieces"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer,
                          autoincrement=True, 
                          primary_key=True)

    name = db.Column(db.String(100), nullable=True)

    artpieces = db.relationship("Artpiece", 
                                secondary="artistartpieces",
                                backref="artists")
    
    def __repr__(self): 
        """Provide representation of Artist when printed. """

        return "<Artist artist_id={} name={} >".format(self.artist_id,
                                                             self.name)


class Artpiece(db.Model):
    """Artpiece. An artpiece has a medium, a creditline, and (many) artists."""

    __tablename__ = "artpieces"

    art_id = db.Column(db.Integer,
                          autoincrement=True, 
                          primary_key=True)
    medium_id = db.Column(db.Integer, 
                          db.ForeignKey('media.medium_id'))
    coords = db.Column(db.ARRAY(db.Numeric, dimensions=1))

    loc_desc = db.Column(db.String(300))
  
    timeperiod = db.Column(db.String(100))

    title = db.Column(db.String(100))

    creditline_id = db.Column(db.Integer, 
                              db.ForeignKey('creditlines.creditline_id'))

    # Define realtionship to medium 
    medium = db.relationship("Medium", 
                              backref=db.backref("artpieces"))

    # Define relationship to Creditline
    creditline = db.relationship("Creditline", 
                                  backref=db.backref("artpieces"))

    def __repr__(self): 
        """Provide representation of an artpiece"""

        return "<Artpiece art_id={} title={} >".format(self.art_id, self.title)


class Creditline(db.Model):
    """Creditline. A creditline has many artpieces.""" 

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
    """AristArtpiece.""" 

    __tablename__ = "artistartpieces"

    artist_art_id = db.Column(db.Integer, 
                              autoincrement=True, 
                              primary_key=True)
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey('artists.artist_id'))
    art_id = db.Column(db.Integer, 
                       db.ForeignKey('artpieces.art_id'))

    def __repr__(self): 
        """Provide representation of one an artist's artipiece""" 

        return "<ArtistArtpiece artist_art_id={}>".format(self.artist_art_id)


class Medium(db.Model):
    """Medium of an artpiece."""

    __tablename__ = "media"

    medium_id = db.Column(db.Integer, 
                          autoincrement=True, 
                          primary_key=True)

    medium_desc = db.Column(db.String(200), 
                            unique=True)

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
    artipiece = db.relationship("Artpiece", 
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
    user_name = db.Column(db.String(50), 
                          nullable=False)
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(20))
    SF_resident = db.Column(db.Boolean)
    email = db.Column(db.String(75), 
                      nullable=False)
    password = db.Column(db.String(75), 
                         nullable=False)

    def __repr__(self): 
        """Provide respresentation of a user of the art app. """

        return "<User user_id={} user_name={} email={} >".format(self.user_id, 
                                                                 self.user_name, 
                                                                 self.email)


################################################################################
# Helper functions

def connect_to_db(app, database='postgresql:///arts'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    # from server import app
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

    

# TODO: Move this to a flile and reimport
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import lazyload, raiseload, relationship

app = Flask(__name__)
db_string = 'mysql://root:my-secret-pw@dragonfly.hopto.org:3306/lucerna'

app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # adds significant overhead when True

db = SQLAlchemy(app)
db.reflect() # get metadata to infer table structure
    
class Address(db.Model):
    __tablename__ = __qualname__
    
    def __repr__(self):
        if self.street2 is None:
            return '< Address: {} {}, {} >'.format(self.street1, self.city, self.state)
        return '< Address: {} {} {}, {} >'.format(self.street1, self.street2, self.city, self.state)

class Classroom(db.Model):
    __tablename__ = __qualname__
    
    school = relationship('School', foreign_keys='Classroom.schoolId')
    
class Contact(db.Model):
    __tablename__ = __qualname__
    
    login = relationship('Login', foreign_keys='Contact.email')
    school = relationship('School', foreign_keys='Contact.schoolId')
    address = relationship('Address', foreign_keys='Contact.addressId')
    
    def __repr__(self):    
        return '< Contact: {} {} >'.format(self.firstName, self.lastName)
    
class Game(db.Model):
    __tablename__ = __qualname__
    
    def __repr__(self):
        return '< Game: {} >'.format(self.name)

class Login(db.Model):
    __tablename__ = __qualname__
    
    def __repr__(self):
        return '< Login: {} {} >'.format(self.email, self.password)

class Player(db.Model):
    __tablename__ = __qualname__
    
    contact = relationship('Contact', foreign_keys='Player.contactId')
    guardian = relationship('Contact', foreign_keys='Player.guardianId')
    classroom = relationship('Classroom', foreign_keys='Player.classroomId')
    system = relationship('System', foreign_keys='Player.systemId')
    
    def __repr__(self):
        return '< Player: {}\'s grade is {} >'.format(self.name, self.grade)
    
class Round(db.Model):
    __tablename__ = __qualname__
    
    session = relationship('Session', foreign_keys='Round.sessionId')
    
    def __repr__(self):
        return '< Round: {} >'.format(self.id)

class School(db.Model):
    __tablename__ = __qualname__
    
    address = relationship('Address', foreign_keys='School.addressId')
    
    def __repr__(self):
        return '< School: {} >'.format(self.name)

class Session(db.Model):
    __tablename__ = __qualname__
    
    player = relationship('Player', foreign_keys='Session.playerId')
    game = relationship('Game', foreign_keys='Session.gameId')
    system = relationship('System', foreign_keys='Session.systemId')
    
    def __repr__(self):
        return '< Session: {} >'.format(self.id)
    
#class Stats(db.Model):
#    __tablename__ = 'Stats'

class System(db.Model):
    __tablename__ = __qualname__
    
    def __repr__(self):
        return '< System: {} OS {} >'.format(self.id, self.operatingSystem)
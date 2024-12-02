from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    __tablename__ = 'staff'
    ID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, nullable=False, unique=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    reviews = db.relationship('Review', back_populates='createdByStaff', lazy='joined')

    def __init__(self, staffID, username, firstname, lastname, email, password):
        self.staffID = staffID
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "staffID": self.staffID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "reviews": [review.to_json() for review in self.reviews],
        }

    def __repr__(self):
        return f'<Staff {self.ID}: {self.username}>'

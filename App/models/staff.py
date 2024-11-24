from App.database import db
from .user import User
from .student import Student


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  reviews = db.relationship('Review', backref='staffReviews', lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, username, firstname, lastname, email, password):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password)
    self.reviews = []




  def to_json(self):
    return {
        "staffID":
        self.ID,
        "username":
        self.username,
        "firstname":
        self.firstname,
        "lastname":
        self.lastname,
        "email":
        self.email,
        "reviews": [review.to_json() for review in self.reviews],
    }

  def __repr__(self):
    return f'<Admin {self.ID} :{self.email}>'

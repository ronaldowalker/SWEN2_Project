from App.database import db
from .user import User
from .student import Student


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.String(10) ,db.ForeignKey('user.ID') , primary_key=True)
  reviews = db.relationship('Review', backref='staff', lazy='joined')
  pendingPosts = db.relationship('Post', backref='staff', lazy='joined')

  def __init__(self,username,firstname, lastname, email, password, faculty):
     super().__init__(username,firstname, lastname, email, password, faculty) 
     self.reviews = []
     self.pendingPosts = []

#return staff details on json format

  def to_json(self):
    return {
        "staffID": self.ID,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "faculty": self.faculty,
        "reviews": [review.to_json() for review in self.reviews],
        "pendingPosts": [post.to_json() for post in self.pendingPosts]
    }

  def __repr__(self):
     return f'<Admin {self.ID} :{self.email}>'

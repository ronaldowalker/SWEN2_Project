from App.database import db
from .user import User


class Admin(User):
  __tablename__ = 'admin'
  ID = db.Column(db.String(10) ,db.ForeignKey('user.ID') , primary_key=True)

  def __init__(self,username,firstname, lastname, email, password, faculty):
     super().__init__(username,firstname, lastname, email, password, faculty) 

#return admin details on json format

  def to_json(self):
    return {
        "adminID": self.ID,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "faculty": self.faculty
    }
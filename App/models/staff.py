from App.database import db
from .user import User
from .student import Student


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.String(10), primary_key=True)

  def __init__(self, ID,firstname, lastname, email, password, faculty):
     super().__init__(firstname, lastname, email, password, faculty) 
     self.staff_id = ID

  def get_id(self):
    return self.staff_id

#return staff details on json format

  def to_json(self):
    return {
        "staffID": self.staff_id,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "faculty": self.faculty,
        "email": self.email,
        "faculty": self.faculty
    }

    def __repr__(self):
     return f'<Admin {self.staff_id} :{self.email}>'
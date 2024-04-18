from App.database import db
from .student import Student

class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  points = db.Column(db.Float, nullable=False, default=0.0)
  rank = db.Column(db.Integer, nullable=False, default=-99)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', use_alter=True))

  def __init__(self, points, rank, studentID):
    self.points = points
    self.rank = rank
    self.studentID = studentID

  def to_json(self):
    return {"karmaID": self.karmaID, "score": self.points, "rank": self.rank, "studentID": self.studentID}
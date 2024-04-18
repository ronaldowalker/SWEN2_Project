from App.database import db
from .student import Student


class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  points = db.Column(db.Float, nullable=False, default=0.0)
  academicPoints = db.Column(db.Float, nullable=False)
  accomplishmentPoints = db.Column(db.Float, nullable=False, default=0.0)
  reviewsPoints = db.Column(db.Float, nullable=False, default=0.0)
  rank = db.Column(db.Integer, nullable=False, default=-99)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID',
                                                  use_alter=True))

  def __init__(self, points, academicPoints, accomplishmentPoints,
               reviewsPoints, rank, studentID):
    self.points = points
    self.academicPoints = academicPoints
    self.accomplishmentPoints = accomplishmentPoints
    self.reviewsPoints = reviewsPoints
    self.rank = rank
    self.studentID = studentID

  def calculate_total_points(self):
    self.points = round(
        (self.academicPoints * 0.4) + (self.accomplishmentPoints * 0.3) +
        (self.reviewsPoints * 0.3), 2)

  def to_json(self):
    return {
        "karmaID": self.karmaID,
        "score": self.points,
        "academicPoints": self.academicPoints,
        "accomplishmentPoints": self.accomplishmentPoints,
        "reviewPoints": self.reviewsPoints,
        "rank": self.rank,
        "studentID": self.studentID
    }

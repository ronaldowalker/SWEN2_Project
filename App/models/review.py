from App.database import db
from .student import Student
from datetime import datetime

class Review(db.Model):
  __tablename__ = 'review'
  ID = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  reviewerID = db.Column(db.String(10),db.ForeignKey('staff.ID'))
  isPositive = db.Column(db.Boolean, nullable=False)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  points = db.Column(db.Integer, nullable=False)
  reviewer = db.relationship('Staff', backref=db.backref('reviews_created', lazy='joined'),foreign_keys=[reviewerID])

  def __init__(self,ID, reviewer, student, isPositive, points):
    self.reviewID = ID
    self.reviewerID = reviewer.ID
    self.reviewer = reviewer
    self.studentID = student.ID
    self.isPositive = isPositive
    self.dateCreatedreated = datetime.now()

  def get_id(self):
    return self.ID

  def to_json(self):
    return {
        "reviewID": self.ID,
        "reviewer": self.reviewer.firstname + " " + self.reviewer.lastname,
        "studentID": self.student.ID,
        "studentName": self.student.firstname + " " + self.student.lastname,
        "created":
        self.created.strftime("%d-%m-%Y %H:%M"),  #format the date/time
        "isPositive": self.isPositive,
        "points": self.points
    }
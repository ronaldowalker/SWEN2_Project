from App.database import db
from .student import Student
from .staff import Staff

class Accomplishment(db.Model):
  __tablename__ = "accomplishment"
  id = db.Column(db.Integer, primary_key=True)
  verified = db.Column(db.Boolean, nullable=False)
  taggedStaffId = db.Column(db.String(10), db.ForeignKey('staff.ID'))
  details = db.Column(db.String(400), nullable=False)

  def __init__(self,studentID ,verified, taggedStaffId, details):
    self.createdByStudentID = studentID
    self.verified = verified
    self.taggedStaffId = taggedStaffId
    self.details = details

  def to_json(self):
    return {"id": self.id,
        "studentID": self.createdByStudentID,
     "verified": self.verified,
      "taggedStaffId": self.taggedStaffId,
      "details": self.details}
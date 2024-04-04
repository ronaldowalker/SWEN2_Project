from App.database import db
from .student import Student
from .staff import Staff
from datetime import datetime


class Recommendation(db.Model):
  __tablename__ = 'recommendation'
  ID = db.Column(db.Integer, primary_key=True)
  createdByStudentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  taggedStaffID = db.Column(db.String(10), db.ForeignKey('staff.ID'))
  studentName = db.Column(db.String(100), nullable=False)
  approved = db.Column(db.Boolean, nullable=False)
  dateRequested = db.Column(db.DateTime, default=datetime.utcnow)
  reason = db.Column(db.String(400), nullable=False)
  details = db.Column(db.String(400), nullable=False)
  status= db.Column(db.String(100), nullable=False)

  def __init__(self, student, staffID, approved, reason, details,status):
    self.createdByStudentID = student.UniId
    self.studentName= f"{student.firstname} {student.lastname}"
    self.taggedStaffID = staffID
    self.approved = approved
    self.dateRequested = datetime.now()
    self.reason = reason
    self.details = details
    self.status=status

  def get_json(self):
    return {
        'studentID': self.createdByStudentID,
        "name":self.studentName,
        'staffID': self.taggedStaffID,
        'approved': self.approved,
        "date requested": self.dateRequested.strftime("%d-%m-%Y %H:%M"),
        'reason': self.reason,
        'details': self.details,
        "status": self.status
    }

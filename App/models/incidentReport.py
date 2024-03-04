from App.database import db
from .student import Student
from .staff import Staff
from datetime import datetime

class IncidentReport(db.Model):
  __tablename__ = "incidentreport"
  id = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  madeByStaffId = db.Column(db.String(10), db.ForeignKey('staff.ID'))
  report = db.Column(db.String(400), nullable=False)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  pointsDeducted = db.Column(db.Integer, nullable=False)

  def __init__(self,studentID , madeByStaffId, report, points):
    self.studentID = studentID
    self.madeByStaffId = madeByStaffId
    self.report = report
    self.dateCreated = datetime.now()
    self.pointsDeducted = points

  def to_json(self):
    return {"id": self.id,
        "studentID": self.createdByStudentID,
      "madeByStaffId": self.madeByStaffId,
      "pointsDeducted": self.pointsDeducted,
      "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),
      "report": self.report}
from App.database import db
from .student import Student
from .staff import Staff
from datetime import datetime

class IncidentReport(db.Model):
  __tablename__ = "incidentreport"
  id = db.Column(db.Integer, primary_key=True)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID'))
  madeByStaffId = db.Column(db.Integer, db.ForeignKey('staff.ID'))
  topic = db.Column(db.String(40), nullable=False)
  report = db.Column(db.String(400), nullable=False)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  pointsDeducted = db.Column(db.Integer, nullable=False)
  studentSeen = db.Column(db.Boolean, nullable=False, default=False)

  def __init__(self,studentID , madeByStaffId,topic, report, points, studentSeen):
    self.studentID = studentID
    self.madeByStaffId = madeByStaffId
    self.report = report
    self.topic= topic
    self.dateCreated = datetime.now()
    self.pointsDeducted = points
    self.studentSeen = studentSeen

  def to_json(self):
    return {"id": self.id,
        "studentID": self.studentID,
      "madeByStaffId": self.madeByStaffId,
      "pointsDeducted": self.pointsDeducted,
      "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),
      "report": self.report,
      "topic": self.topic,
      "studentSeen": self.studentSeen}
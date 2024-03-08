from App.database import db
from .student import Student
from .staff import Staff
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    ID = db.Column(db.Integer, primary_key=True)
    createdByStudentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
    taggedStaffID = db.Column(db.String(10), db.ForeignKey('staff.ID'))
    approved = db.Column(db.Boolean, nullable=False)
    dateRequested = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, studentID, staffID, approved):
        self.createdByStudentID = studentID
        self.taggedStaffID = staffID
        self.approved = approved
        self.dateRequested = datetime.now()

    def get_json(self):
        return {
            'studentID': self.createdByStudentID,
            'staffID': self.taggedStaffID,
            'approved': self.approved,
            "date requested": self.dateRequested.strftime("%d-%m-%Y %H:%M")
        }

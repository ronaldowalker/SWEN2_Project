from App.database import db
from .student import Student
from .staff import Staff

class Post(db.Model):
  __tablename__ = 'post'
  ID = db.Column(db.Integer, primary_key=True)
  createdByStudentID = db.Column(db.String(10), db.ForeignKey('student.ID'))
  verifiedByStaffID = db.Column(db.String(10),db.ForeignKey('staff.ID'))
  verified = db.Column(db.Boolean, nullable=False)
  details = db.Column(db.String(400), nullable=False)

  def __init__(self, studentID, staffID, verified, details):
        self.createdByStudentID= studentID
        self.verifiedByStaffID = staffID
        self.verified = verified
        self.details = details

    def get_json(self):
        return{
            'studentID': self.createdByStudentID,
            'staffID': self.verifiedByStaffID,
            'verified': self.verified,
            'details': self.details
        }
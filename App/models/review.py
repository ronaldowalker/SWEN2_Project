from App.database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True)
    taggedStudentID = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)
    createdByStaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)
    isPositive = db.Column(db.Boolean, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(400), nullable=False)

    taggedStudent = db.relationship('Student', backref='reviews', lazy='joined')
    createdByStaff = db.relationship('Staff', backref='reviews', lazy='joined')

    def __init__(self, staffID, studentID, isPositive, details):
        self.createdByStaffID = staffID
        self.taggedStudentID = studentID
        self.isPositive = isPositive
        self.details = details

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "reviewer": f"{self.createdByStaff.firstname} {self.createdByStaff.lastname}",
            "studentID": self.taggedStudentID,
            "studentName": f"{self.taggedStudent.firstname} {self.taggedStudent.lastname}",
            "created": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Formatted date/time
            "isPositive": self.isPositive,
            "details": self.details,
        }

    def __repr__(self):
        return f"<Review {self.ID}: {'Positive' if self.isPositive else 'Negative'}>"

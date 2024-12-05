from App.database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)
    StaffID = db.Column(db.Integer, db.ForeignKey('staff.ID'), nullable=False)
    isPositive = db.Column(db.Boolean, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(400), nullable=False)

    taggedStudent = db.relationship('Student', back_populates='reviews', lazy='joined')
    createdByStaff = db.relationship('Staff', back_populates='reviews', lazy='joined')

    def __init__(self, StudentID, StaffID, isPositive, details):
        self.StudentID = StudentID
        self.StaffID = StaffID
        self.isPositive = isPositive
        self.details = details

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "reviewer": f"{self.createdByStaff.firstname} {self.createdByStaff.lastname}",
            "studentID": self.taggedStudent.studentID,
            "studentName": f"{self.taggedStudent.firstname} {self.taggedStudent.lastname}",
            "created": self.dateCreated.strftime("%d-%m-%Y %H:%M"),  # Formatted date/time
            "isPositive": self.isPositive,
            "details": self.details,
        }

    def __repr__(self):
        return f"<Review {self.ID}: {'Positive' if self.isPositive else 'Negative'}>"
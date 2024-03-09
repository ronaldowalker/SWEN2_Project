from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'student'
    ID = db.Column(db.String(10), db.ForeignKey('user.ID'), primary_key=True)
    degree = db.Column(db.String(120), nullable=False)
    admittedTerm = db.Column(db.String(120), nullable=False)
    yearOfStudy = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.String(120), nullable=True)
    reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
    accomplishments = db.relationship('Accomplishment', backref='studentAccomplishments', lazy='joined')
    incidents = db.relationship('IncidentReport', backref='studentincidents', lazy='joined')
    grades = db.relationship('Grades', backref='studentGrades', lazy='joined')
    karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

    def __init__(self, username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree, gpa):
        super().__init__(username, firstname, lastname, email, password, faculty)
        self.admittedTerm = admittedTerm
        self.yearOfStudy = yearofStudy
        self.degree = degree
        self.gap = gpa
        self.reviews = []
        self.accomplishments = []
        self.incidents = []
        self.grades = []
    
    def get_id(self):
        return self.ID

    # Gets the student details and returns in JSON format
    def to_json(self):
        karma = self.getKarma()
        return {
            "studentID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "gpa": self.gpa,
            "email": self.email,
            "faculty": self.faculty,
            "degree": self.degree,
            "admittedTerm": self.admittedTerm,
            "yearOfStudy": self.yearOfStudy,
            "reviews": [review.to_json() for review in self.reviews],
            "accomplishments": [accomplishment.to_json() for accomplishment in self.accomplishments],
            "incidents": [incident.to_json() for incident in self.incidents],
            "grades": [grade.to_json() for grade in self.grades],
            "karmaScore": karma.score if karma else None,
            "karmaRank": karma.rank if karma else None
        }

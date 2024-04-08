from App.database import db
from .user import User
from .student import Student


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  reviews = db.relationship('Review', backref='staffReviews', lazy='joined')
  reports = db.relationship('IncidentReport',
                            backref='staffReports',
                            lazy='joined')
  pendingAccomplishments = db.relationship('Accomplishment',
                                           backref='studentaccomplishments',
                                           lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, username, firstname, lastname, email, password, faculty):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password,
                     faculty=faculty)
    self.reviews = []
    self.reports = []
    self.pendingAccomplishments = []


#return staff details on json format

  def to_json(self):
    return {
        "staffID":
        self.ID,
        "username":
        self.username,
        "firstname":
        self.firstname,
        "lastname":
        self.lastname,
        "email":
        self.email,
        "faculty":
        self.faculty,
        "reviews": [review.to_json() for review in self.reviews],
        "reports": [report.to_json() for report in self.reports],
        "pendingAccomplishments": [
            pendingAccomplishment.to_json()
            for pendingAccomplishment in self.pendingAccomplishments
        ]
    }

  def __repr__(self):
    return f'<Admin {self.ID} :{self.email}>'

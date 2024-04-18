from App.database import db
from .recommendation import Recommendation


class SchoolRecommendation(Recommendation):
  __tablename__ = 'schoolRecommendation'
  ID = db.Column(db.Integer,
                 db.ForeignKey('recommendation.ID'),
                 primary_key=True)
  school = db.Column(db.String(100), nullable=False)
  program = db.Column(db.String(100), nullable=False)
  schoolEmail = db.Column(db.String(100), nullable=False)

  __mapper_args__ = {"polymorphic_identity": "schoolRecommendation"}

  def __init__(self, currentYearOfStudy, details, student, staffID, approved,
               status, school, program, schoolEmail):
    super().__init__(student=student,
                     staffID=staffID,
                     approved=approved,
                     status=status,
                     currentYearOfStudy=currentYearOfStudy,
                     details=details,
                     studentSeen=False)
    self.school = school
    self.program = program
    self.schoolEmail = schoolEmail

  def __repr__(self):
    return f'<SchoolRecommendation {self.ID} >'

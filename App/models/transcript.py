from App.database import db

class Transcript(db.Model):
    __tablename__ = 'transcript'
    ID = db.Column(db.Integer, primary_key=True)
    UniId = db.Column(db.String(10), db.ForeignKey('student.UniId'), nullable=False)
    # gpa = db.Column(db.String(10), nullable=False)
    # fullname = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.String(120), nullable=False)
    isInProgress = db.Column(db.Boolean, default=False, nullable=False)


    def __init__(self, UniId, semester, course, grade, isInProgress=False):
        self.UniId = UniId
        # self.gpa = gpa
        # self.fullname = fullname
        self.semester = semester
        self.course = course
        self.grade = grade
        self.isInProgress = isInProgress

    def to_json(self):
        return {
            "ID": self.ID,
            "UniId": self.UniId,
            # "gpa": self.gpa,
            # "fullname": self.fullname,
            "semester": self.semester,
            "course": self.course,
            "grade": self.grade,
            "isInProgress": self.isInProgress
        }

from App.database import db

class Student(db.Model):
    __tablename__ = 'student'
    ID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    karma = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    reviews = db.relationship('Review', backref='student', lazy='joined')

    def __init__(self, firstName, lastName, karma=0):
        self.firstName = firstName
        self.lastName = lastName
        self.karma = karma

    def get_id(self):
        return self.ID

    def full_name(self):
        return f"{self.firstName} {self.lastName}"

    # JSON Representation
    def to_json(self):
        return {
            "studentID": self.ID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "karma": self.karma,
            "reviews": [review.to_json() for review in self.reviews],
        }

    def __repr__(self):
        return f"<Student {self.ID}: {self.full_name()}>"

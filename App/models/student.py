from App.database import db
from .user import User

class Student(User):
	__tablename__ = 'student'
	ID = db.Column(db.String(10),db.ForeignKey('user.ID'), primary_key=True)
	degree = db.Column(db.String(120), nullable=False) 
    admittedTerm = db.Column(db.String(120), nullable=False)
	yearOfStudy = db.Column(db.Integer, nullable=False)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	posts= db.relationship('Post', backref='student', lazy='joined')
	karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

	def __init__(self, username,firstname, lastname, email, password, faculty, admittedTerm, yearofStudy,degree):
		super().__init__(username, firstname, lastname, email, password, faculty)
		self.admittedTerm = admittedTerm
		self.yearOfStudy = yearofStudy
        self.degree= degree
		self.reviews = [] 
		self.posts = []
	
	def get_id(self):
		return self.ID

#Gets the student details and returns in JSON format
	def to_json(self):
		karma = self.getKarma()
		return {
        "studentID": self.ID,
        "username": self.username,
        "firstname": self.firstname,
        "lastname": self.lastname,
		"email": self.email,
		"faculty": self.faculty,
        "degree": self.degree,
        "admittedTerm": self.admittedTerm,
        "yearOfStudy": self.yearOfStudy,
        "reviews": [review.to_json() for review in self.reviews],
		"posts": [post.to_json() for post in self.posts],
		"karmaScore": karma.score if karma else None,
        "karmaRank": karma.rank if karma else None
    }



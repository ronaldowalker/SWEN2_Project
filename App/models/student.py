from App.database import db
KarmaManager = None  # Prevent circular import

def init_karma_manager():
    global KarmaManager
    if KarmaManager is None:
        from App.karmaManager import KarmaManager


class Student(db.Model):
    __tablename__ = 'student'
    ID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, unique = True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    karma = db.Column(db.Integer, nullable=False, default=0)

    reviews = db.relationship('Review', back_populates='taggedStudent', lazy='joined')
    karma_history = db.relationship('Karma', back_populates='student', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, studentID, firstName, lastName, karma=0):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.karma = karma

    def get_id(self):
        return self.studentID

    def full_name(self):
        return f"{self.firstName} {self.lastName}"

    def to_json(self):
        return {
            "studentID": self.studentID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "karma": self.karma,
            "reviews": [review.to_json() for review in self.reviews],
        }

    # Interact with the KarmaManager
    def increase_karma(self, amount):
        init_karma_manager()
        return KarmaManager().increase_karma(self, amount)

    def decrease_karma(self, amount):
        init_karma_manager()
        return KarmaManager().decrease_karma(self, amount)

    def undo_last_action(self):
        init_karma_manager()
        return KarmaManager().undo_last_action(self)

    def view_karma_history(self):
        init_karma_manager()
        return KarmaManager().view_history(self)


    def __repr__(self):
        return f"<Student {self.ID}: {self.studentID} {self.full_name()}>"
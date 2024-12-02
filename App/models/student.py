from App.database import db
from App.karmaManager import KarmaManager

karma_manager = KarmaManager()  # Singleton instance of the manager

class Student(db.Model):
    __tablename__ = 'student'
    ID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, unique = True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    karma = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    reviews = db.relationship('Review', back_populates='taggedStudent', lazy='joined')

    def __init__(self, ID, firstName, lastName, karma=0):
        self.studentID = ID
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
        return karma_manager.increase_karma(self, amount)

    def decrease_karma(self, amount):
        return karma_manager.decrease_karma(self, amount)

    def undo_last_action(self):
        return karma_manager.undo_last_action(self)

    def view_karma_history(self):
        return karma_manager.view_history(self)

    def __repr__(self):
        return f"<Student {self.ID}: {self.full_name()}>"
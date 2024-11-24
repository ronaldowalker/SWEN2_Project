from App.database import db
from App.models import karmaCommand

class DecreaseKarmaCommand(KarmaCommand):
    def __init__(self, student, amount):
        self.student = student
        self.amount = amount

    def execute(self):
        self.previous_karma = self.student.karma
        self.student.karma -= self.amount
        return f"Karma decreased by {self.amount} to {self.student.karma}"

    def undo(self):
        self.student.karma = self.previous_karma
        return f"Karma reverted to {self.student.karma}"


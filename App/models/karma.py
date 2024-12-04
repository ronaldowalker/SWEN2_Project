from App.database import db
from .student import Student
from datetime import datetime


class Karma(db.Model):
      
      __tablename__ = "karma"
      ID = db.Column(db.Integer, primary_key=True)
      studentID = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)  # Link to Student model
      action = db.Column(db.String(10), nullable=False)  # 'increase' or 'decrease'
      amount = db.Column(db.Integer, nullable=False)  # Change in karma (e.g., +1 or -1)
      previous_karma = db.Column(db.Integer, nullable=False)  # Karma before the change
      updated_karma = db.Column(db.Integer, nullable=False)  # Karma after the change
      timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Time of change

      student = db.relationship('Student', back_populates='karma_history')

      def __init__(self, studentID, action, amount, previous_karma, updated_karma):
            self.studentID = studentID
            self.action = action
            self.amount = amount
            self.previous_karma = previous_karma
            self.updated_karma = updated_karma

      
      def to_json(self):
        return {
            "id": self.ID,
            "student_id": self.studentID,
            "action": self.action,
            "amount": self.amount,
            "previous_karma": self.previous_karma,
            "updated_karma": self.updated_karma,
            "timestamp": self.timestamp.isoformat(),
        }
      
       return f"<Karma History {self.ID}: StudentID {self.studentID}, Action-{self.action} by {self.amount}. The previous karma was {self.previous_karma}. Updated to {self.updated_karma}>"

  
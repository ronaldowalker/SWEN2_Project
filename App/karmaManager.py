from App.database import db
from App.models.karma import Karma

class KarmaManager:
    
    def increase_karma(self, student, amount):
        """Increase the karma for a student."""
        previous_karma = student.karma
        student.karma += amount
        updated_karma = student.karma

        #self, studentID, action, amount, previous_karma, updated_karma
        history = Karma(studentID = student.ID,
                        action = "increase",
                        amount = amount,
                        previous_karma = previous_karma,
                        updated_karma = updated_karma
                        )

        db.session.add(history)
        db.session.commit()

        return f"Karma increased by {amount} to {student.karma} for student {student.firstName} {student.lastName}"

    def decrease_karma(self, student, amount):
        """Decrease the karma for a student."""
        previous_karma = student.karma
        student.karma -= amount
        updated_karma = student.karma

        history = Karma(studentID = student.ID,
                        action = "decrease",
                        amount = amount,
                        previous_karma = previous_karma,
                        updated_karma = updated_karma
                        )

        db.session.add(history)
        db.session.commit()


        return f"Karma decreased by {amount} to {student.karma} for student {student.firstName} {student.lastName}"

    def undo_last_action(self, student):
        """Undo the last karma change for a student."""
        # Fetch the last karma change for this student from the database
        last_action = Karma.query.filter_by(studentID=student.ID).order_by(Karma.timestamp.desc()).first()
        if not last_action:
            return "No actions to undo"

        # Revert the student's karma
        student.karma = last_action.previous_karma

        # Delete the last action from the history
        db.session.delete(last_action)
        db.session.commit()

        action = "reverted" if last_action.action == "increase" else "restored"
        return f"Karma {action} to {last_action.previous_karma}"

    def view_history(self, student):
        """View the karma history for a student."""
        history = Karma.query.filter_by(studentID=student.ID).order_by(Karma.timestamp.desc()).all()
        return [entry.to_json() for entry in history] if history else ["No karma changes recorded"]

    
from App.database import db

class KarmaManager:
    def __init__(self):
        self.history = []

    def increase_karma(self, student, amount):
        """Increase the karma for a student."""
        previous_karma = student.karma
        student.karma += amount
        self.history.append((student.ID, "increase", amount, previous_karma, student.karma))
        return f"Karma increased by {amount} to {student.karma}"

    def decrease_karma(self, student, amount):
        """Decrease the karma for a student."""
        previous_karma = student.karma
        student.karma -= amount
        self.history.append((student.ID, "decrease", amount, previous_karma, student.karma))
        return f"Karma decreased by {amount} to {student.karma}"

    def undo_last_action(self, student):
        """Undo the last karma change for a student."""
        if not self.history:
            return "No actions to undo"
        last_action = self.history.pop()
        if last_action[0] != student.ID:
            self.history.append(last_action)
            return "No actions to undo for this student"
        action_type, _, amount, previous_karma, _ = last_action[1:]
        student.karma = previous_karma
        action = "reverted" if action_type == "increase" else "restored"
        return f"Karma {action} to {previous_karma}"

    def view_history(self, student):
        """View the karma history for a student."""
        student_history = [
            f"{action.capitalize()} karma by {amount}: {prev} -> {curr}"
            for sid, action, amount, prev, curr in self.history
            if sid == student.ID
        ]
        return student_history if student_history else ["No karma changes recorded"]

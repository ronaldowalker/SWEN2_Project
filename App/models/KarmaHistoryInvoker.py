from App.database import db
from App.models import IncreaseKarmaCommand

class KarmaHistoryInvoker:
    def __init__(self):
        self.history = []

    def execute_command(self, command):
        result = command.execute()
        self.history.append(command)
        return result

    def undo_last_command(self):
        if not self.history:
            return "No commands to undo"
        command = self.history.pop()
        return command.undo()
    
    def view_history(self):
        if not self.history:
            return "No karma changes recorded"
        changes = []
        for command in self.history:
            action = "Increased" if isinstance(command, IncreaseKarmaCommand) else "Decreased"
            changes.append(f"{action} karma by {command.amount} to {command.student.karma}")
        return changes

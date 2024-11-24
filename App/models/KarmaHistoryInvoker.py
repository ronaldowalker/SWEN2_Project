from App.database import db

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
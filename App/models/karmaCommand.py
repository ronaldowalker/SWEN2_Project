from abc import ABC, abstractmethod

class KarmaCommand:
    def execute(self):
        raise NotImplementedError("Subclasses must implement execute")

    def undo(self):
        raise NotImplementedError("Subclasses must implement undo")

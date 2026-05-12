class CoverageTracker:
    def __init__(self):
        self.states = set()

    def seen(self, state):
        if state in self.states:
            return True

        self.states.add(state)

        return False
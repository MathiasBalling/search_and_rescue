class BlackBoard:
    def __init__(self):
        self.blackboard = {}

    def set(self, key, value):
        self.blackboard[key] = value

    def get(self, key):
        return self.blackboard[key]

class BlackBoard:
    def __init__(self):
        self.blackboard = {}

    def __setitem__(self, key, value):
        self.blackboard[key] = value

    def __getitem__(self, key):
        return self.blackboard[key]

    def set(self, key, value):
        self.blackboard[key] = value

    def get(self, key):
        return self.blackboard[key]

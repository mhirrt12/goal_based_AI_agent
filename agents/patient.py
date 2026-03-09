class Patient:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

        priority_map = {
            "critical": 1,
            "serious": 2,
            "normal": 3
        }

        self.priority = priority_map[condition]

    def __lt__(self, other):
        return self.priority < other.priority
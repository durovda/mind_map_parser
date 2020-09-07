

class Step:
    def __init__(self, name):
        self.name = name


class Case:
    def __init__(self, name):
        self.name = name
        self.method_name = None
        self.steps = []

    def add_step(self, step_name):
        self.steps.append(Step(step_name))

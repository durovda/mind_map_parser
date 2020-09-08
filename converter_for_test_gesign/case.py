

class Step:
    def __init__(self, name):
        self.name = name
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)


class Case:
    def __init__(self, name, feature=None, story=None, method="???"):
        self.name = name
        self.method = method
        self.feature = feature
        self.story = story
        self.steps = []
        self.comments = []

    def add_step(self, step_name):
        self.steps.append(Step(step_name))

    def add_comment(self, comment):
        self.comments.append(comment)

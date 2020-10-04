class ArtifactExp:
    def __init__(self, experience):
        self._experience = float(experience)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, experience):
        self._experience = experience
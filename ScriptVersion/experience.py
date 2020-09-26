class ArtifactExp:
    def __init__(self, experience):
        self._experience = experience

    @property
    def Experience(self):
        return self._experience

    @Experience.setter
    def Experience(self, experience):
        self._experience = experience
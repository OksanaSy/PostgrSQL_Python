class Character:

    def __init__(self, nm, snm, rc, cls):
        self.name = nm
        self.surname = snm
        self.race = rc
        self.clas = cls

    def to_string(self):
        return '{0} {1}, race: {2}, class: {3}'.format(self.name,self.surname,self.race,self.clas)

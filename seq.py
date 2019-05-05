class Seq:
    """A class for representing sequences"""
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def perc(self, base):
        tl = len(self.strbases)
        counter = self.strbases.count(base)
        perc = 100.0 * counter/tl
        return perc
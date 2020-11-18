class Engineer:

    def __init__(self, un):
        self.username = un
        self.comments = 1
        self.negatives = []
        self.positives = []

    def inc_comments(self):
        self.comments += 1

    def comments_cnt(self):
        return self.comments

    def pos_cnt(self):
        return len(self.positives)

    def neg_cnt(self):
        return len(self.negatives)

    def pos_rate(self):
        if self.comments > 0:
            return len(self.positives) / self.comments
        else:
            return 0

    def neg_rate(self):
        if self.comments > 0:
            return len(self.negatives) / self.comments
        else:
            return 0

    def pos_found(self, txt):
        self.positives.insert(len(self.positives), txt)

    def neg_found(self, txt):
        self.negatives.insert(len(self.negatives), txt)

    def dump(self, f):
        pref = "{u}: {c} comments, {pp:.2f}% positive ({pw}), {np:.2f}% negative ({nw})".format(u=self.username,
                                                                                                c=self.comments,
                                                                                                pp=100*self.pos_rate(),
                                                                                                pw=len(self.positives),
                                                                                                np=100*self.neg_rate(),
                                                                                                nw=len(self.negatives))
        print(pref)
        f.write(pref + '\n')


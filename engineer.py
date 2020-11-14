class Engineer:
    comments = 0
    positives = 0
    negatives = 0
    username = ""

    def pos_rate(self):
        if self.comments > 0:
            return round(self.positives/self.comments)
        else:
            return 0

    def neg_rate(self):
        if self.comments > 0:
            return round(self.negatives/self.comments)
        else:
            return 0

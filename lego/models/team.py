# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from sqlalchemy.ext.hybrid import hybrid_property

from lego import app, db


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    is_practice = db.Column(db.Boolean, default=False, nullable=False)
    round_1 = db.Column(db.Integer, nullable=True)
    round_2 = db.Column(db.Integer, nullable=True)
    round_3 = db.Column(db.Integer, nullable=True)
    quarter = db.Column(db.Integer, nullable=True)
    semi = db.Column(db.Integer, nullable=True)
    final_1 = db.Column(db.Integer, nullable=True)
    final_2 = db.Column(db.Integer, nullable=True)


    @hybrid_property
    def attempts(self):
        return [self.round_1, self.round_2, self.round_3]

    @hybrid_property
    def finals(self):
        return [self.final_1, self.final_2]


    def set_score(self, score):
        stage = app.load_stage()
        app.logger.debug('Stage: %s', stage)
        app.logger.debug('Team: %s', str(self.__dict__))

        # first round
        if stage == 0:
            if self.round_1 is None:
                self.round_1 = score
            elif self.round_2 is None:
                self.round_2 = score
            elif self.round_3 is None:
                self.round_3 = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # quarter finals
        elif stage == 1:
            if self.quarter is None:
                self.quarter = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # semi finals
        elif stage == 2:
            if self.semi is None:
                self.semi = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # finals
        elif stage == 3:
            if self.final_1 is None:
                self.final_1 = score
            elif self.final_2 is None:
                self.final_2 = score
            else:
                raise Exception('All attempts have been made for this stage.')

        else:
            raise Exception('Invalid value for stage.')

    @hybrid_property
    def highest_score(self):
        stage = app.load_stage()
        if stage == 0:
            return max(self.round_1 or 0, self.round_2 or 0, self.round_3 or 0)

        if stage == 1:
            return self.quarter or 0

        if stage == 2:
            return self.semi or 0

        return max(self.final_1 or 0, self.final_2 or 0)


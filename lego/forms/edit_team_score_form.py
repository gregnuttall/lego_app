# -----------------------------------------------------------------------------
# A form for editing teams scores.
#
# To be used by Admin accounts.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange


class EditTeamScoreForm(FlaskForm):
    id = HiddenField('Id', validators=[DataRequired()])
    stage = SelectField('Stage',
                        choices=[('attempt_1', 'Round 1 - Attempt 1'),
                                 ('attempt_2', 'Round 1 - Attempt 2'),
                                 ('attempt_3', 'Round 1 - Attempt 3'),
                                 ('round_2', 'Round 2'),
                                 ('quarter', 'Quarter Final'),
                                 ('semi', 'Semi Final'),
                                 ('final', 'Final')],
                        default='attempt_1',
                        validators=[DataRequired()])
    score = IntegerField('Score', validators=[NumberRange(min=0)])

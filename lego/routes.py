# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import render_template, flash, redirect, request, url_for, g, abort
from flask_login import login_user, logout_user, current_user, login_required

from lego import app, db, lm
from lego.forms import LoginForm, ScoreRoundForm
from lego.models import User, Team


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(403)
def page_not_found(error):
    return render_template('errors/403.html', title='Permission denied'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page not found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Internal error'), 500


@app.route('/')
@app.route('/home')
def home():
    teams = Team.query.all()
    return render_template('home.html', title='Home', teams=teams)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        res = User.authenticate(username, password)

        if isinstance(res, User):
            login_user(res)
            return redirect(url_for('home'))

        flash(res)

    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html', title='Scoreboard',
                           qualifying=[], not_qualifying=[])


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', title='Completed Tasks')


@app.route('/judges')
@app.route('/judges/')
@app.route('/judges/home')
@login_required
def judges_home():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    return render_template('judges/home.html', title='Judges Home')


@app.route('/judges/score_round', methods=['GET', 'POST'])
@login_required
def judges_score_round():
    if not (current_user.is_judge or current_user.is_admin):
        return abort(403)

    form = ScoreRoundForm()

    form.team.choices = [('', '--Select team--')]
    form.team.choices += [(str(t.id), t.name) for t in Team.query.order_by('name')]

    if form.validate_on_submit():
        team_id = form.team.data
        team = Team.query.get(team_id)
        score = form.points_scored()

        flash('Submitted successfully')

        if len(team.scored_attempts) == 3:
            flash('Team has no more attempts remaining')
        else:
            if form.confirm.data == '1':
                if score == int(form.score.data):
                    setattr(team, 'attempt_{!s}'.format(attempt), score)
                    db.session.commit()

                    return redirect(url_for('judges_score_round'))

            attempt = len(team.scored_attempts) + 1

            if team.is_practice:
                flash('Practice attempt')
            else:
                form.confirm.data = '1'

            flash('Score: {!s}'.format(score))

            form.score.data = score
            form.attempt.data = attempt

            return render_template('judges/score_round.html', title='Score round',
                                   form=form, confirm=True)

    return render_template('judges/score_round.html', title='Score round', form=form)


@app.route('/admin/')
@app.route('/admin/home')
@login_required
def admin_home():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Home'


@app.route('/admin/teams/')
@login_required
def admin_teams():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams'


@app.route('/admin/teams/new')
@login_required
def admin_teams_new():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/New'


@app.route('/admin/teams/<name>/edit')
@login_required
def admin_teams_edit():
    if not current_user.is_admin:
        return abort(403)

    return 'Admin/Teams/Edit'

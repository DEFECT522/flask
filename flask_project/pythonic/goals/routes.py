from flask import Blueprint, render_template, url_for, redirect, flash
from pythonic.models import Goal
from pythonic.goals.forms import GoalForm
from pythonic import db
from flask_login import current_user, login_required


goals = Blueprint('goals', __name__)


@goals.route('/goals')
@login_required
def goals_dashboard():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    total_points = sum(goal.points for goal in goals)
    total_goals = len(goals)
    percentage = 0
    if total_goals > 0:
        percentage = int(sum(goal.points for goal in goals) / (total_goals * 365) * 100)
    return render_template('goals_dashboard.html', total_points=total_points, total_goals=total_goals, percentage=percentage)



@goals.route('/goals/add', methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(name=form.name.data, description=form.description.data, owner=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('goals.all_goals'))
    return render_template('add_goal.html', form=form)



@goals.route('/goals/all')
@login_required
def all_goals():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('all_goals.html', goals=goals)



@goals.route('/goal/<int:goal_id>/increase')
@login_required
def increase_points(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.owner != current_user:
        flash('Access denied.', 'danger')
        return redirect(url_for('goals.goals_dashboard'))
    goal.points += 1
    db.session.commit()
    return redirect(url_for('goals.all_goals'))



@goals.route('/goal/<int:goal_id>/decrease')
@login_required
def decrease_points(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.owner != current_user:
        flash('Access denied.', 'danger')
        return redirect(url_for('goals.goals_dashboard'))
    if goal.points > 0:
        goal.points -= 1
    db.session.commit()
    return redirect(url_for('goals.all_goals'))
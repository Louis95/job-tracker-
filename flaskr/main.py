from flask import Blueprint, flash
from flaskr.models import *
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/newjob')
def new_job():
    jobstatus = []
    for status in JobStatus:
        jobstatus.append(status)
    return render_template('create_job.html', jobstatus=jobstatus)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/newjob', methods=['POST'])
@login_required
def post_job():
    company = request.form.get('company')
    position = request.form.get('position')
    website = request.form.get('website')
    status = request.form.get('status')
    description = request.form.get('description')

    if not company or not position or not status:
        flash('Please input required fields')
        return redirect(url_for('main.new_job'))

    job = Job(company=company, description=description, url=website, position=position, user_id=current_user.id,
              job_status=status)
    flash('You have successfully created a new job  ', job.position)

    job.insert()
    return redirect(url_for('main.index'))


@main.route('/all_jobs', methods=['GET'])
@login_required
def get_jobs():
    user_id = current_user.id
    jobs_for_user = Job.query.filter_by(user_id=user_id)

    return render_template("all_jobs.html", jobs_for_user=jobs_for_user)



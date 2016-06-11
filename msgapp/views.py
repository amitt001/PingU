"""msgapp app views"""

from datetime import datetime
from flask import render_template, request, url_for, redirect

import utils
import cron
import messenger
from models import User, Reminder, db


@utils.catch_exc
def index():
    """Home Page. Takes phonenumber through POST, serves home through GET."""
    if request.method == 'GET':
        return render_template('msgapp/index.html')

    elif request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        country_code = request.form['country_code']
        timezone = request.form['timezone']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        if not utils.valid_info(name, phone):
            raise Exception(("Invalid phone or name. Phone should "
                            "have at least 10 characters."), 404)

        #check user already exists
        if utils.number_exists(phone):
            return redirect(url_for('info', phone=phone))
        else:
            u = User(name=name, phone=phone,
                    country_code=country_code, 
                    timezone=timezone, 
                    night_start=start_time,
                    night_end=end_time)
            db.session.add(u)
            db.session.commit()
            cron_job = cron.create(phone)

        return redirect(url_for('info', phone=phone))


@utils.catch_exc
def reminder():
    """Get reminder details of the user"""
    if request.method == 'GET':
        return render_template('msgapp/reminder_info.html')

    if request.method == 'POST':
        phone = request.form['phone']
        if not phone:
            raise Exception("Invalid or empty phone field", 404)
        return redirect(url_for('info', phone=phone))


@utils.catch_exc
def info():
    phone = request.args.get('phone')
    user = User.query.filter_by(phone=phone).first()
    if user:
        reminder = Reminder.query.filter_by(phone=phone).all()
        norecord_msg = ''

        if reminder:
            columns = utils.process_reminder_info(reminder[0])
            #number of hours the application has been running
            timedelta = (datetime.utcnow() - user.created_on)
            num_hrs = "%.0f" % (timedelta.total_seconds()//3600)

        else: #when user just created profile and no reminder is sent
            num_hrs = 0
            columns, reminder = [], []
            norecord_msg = 'Welcome! Check back after 1 hour to see status.'
            # if night mode on
            if not messenger.right_time(user):
                norecord_msg = ('Night Mode On.'
                                'Check beck after %s AM') % user.night_end

        return render_template(
            "msgapp/info.html",
            norecord_msg = norecord_msg,
            name = user.name, phone = user.phone,
            hours = num_hrs, columns = columns,
            reminders = [r.__dict__ for r in reminder])
    else:
        return render_template(
            "msgapp/404.html",
            status_code='404',
            error='No Record Found')

def error():
    error = "----"
    return render_template("msgapp/404.html", error=error)
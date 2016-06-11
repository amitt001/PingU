"""Small utility functions"""

import traceback
from datetime import datetime
from pytz import timezone
from functools import wraps

from flask import render_template, redirect, url_for

from models import User, Reminder


def number_exists(number):
    """check if user with thsi phone number already exists"""
    return User.query.filter_by(phone=number).first() != None


def valid_info(name, phone):
    """check name and phone are valid"""
    _valid = True
    if not name or not phone:
        _valid = False
    if not phone.isdigit():
        _valid = False
    if len(phone) < 10:
        _valid = False
    return _valid


def process_reminder_info(reminder):
    """Get columns from reminder obj"""
    columns = reminder.__table__.columns.keys()
    for col in ['phone', 'id', 'updated_on']:
        columns.remove(col)
    return columns


def local_from_timezone(tymzone):
    """get users loca time from his timezone

        US/Eastern
        Asia/Kathmandu
        Africa/Johannesburg
    """

    tz = timezone(tymzone)
    tz_time = datetime.now(tz)
    #return tz_time.strftime('%H:%M:%S')
    return float(str(tz_time.time().hour) + "." + str(tz_time.time().minute))


def catch_exc(f):
    """exception catcher decorator"""
    @wraps(f)
    def _catch_exc(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            return ret
        except Exception as e:
            #traceback.print_exc(e)
            error = e.args[0] if len(e.args) > 1 else 'Error...Retry'
            return render_template("msgapp/404.html", error=error)
    return _catch_exc



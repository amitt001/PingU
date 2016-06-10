"""Small utility functions"""

import traceback
from functools import wraps

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
    return _valid


def process_reminder_info(reminder):
    """Get columns from reminder obj"""
    columns = reminder.__table__.columns.keys()
    for col in ['phone', 'id', 'updated_on']:
        columns.remove(col)
    return columns


def catch_exc(f):
    """exception catcher generator"""
    @wraps(f)
    def _catch_exc(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            return ret
        except Exception as e:
            traceback.print_exc(e)
            return "Error"
    return _catch_exc



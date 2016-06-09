"""Small utility functions"""

#from app import db
import traceback
from functools import wraps

from models import User, Reminder


def number_exists(number):
    return User.query.filter_by(phone=number).first() != None

def valid_info(name, phone):
    _valid = True
    if not name or not phone:
        _valid = False
    if not phone.isdigit():
        _valid = False
    return _valid


def process_reminder_info(reminder):
    columns = reminder.__table__.columns.keys()
    for col in ['phone', 'id', 'updated_on']:
        columns.remove(col)
    return columns


# def process_reminder(reminder):
#     data = {'columns': [], 'info': []}
#     columns = reminder[0].__table__.columns.keys()
#     for col in columns:
#         if col == 'id':
#             continue
#         data['columns'].append(' '.join(col.capitalize().split('_')))
#         data['info'].append()
#     columns.rem



def catch_exc(f):
    @wraps(f)
    def _catch_exc(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            return ret
        except Exception as e:
            traceback.print_exc(e)
            return "Error"
    return _catch_exc



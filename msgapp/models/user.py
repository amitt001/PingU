from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
#import msgapp.utils as utils

#db = utils.db
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56))
    phone = db.Column(db.String(24), unique=True, index=True)
    country_code = db.Column(db.String(5))
    timezone = db.Column(db.String(128))
    night_start = db.Column(db.String(10))
    night_end = db.Column(db.String(10))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    reminders = db.relationship("Reminder")

    def __repr__(self):
        return "<User(name='%s', phone='%s'>" % (self.name, self.phone)

    def __init__(self, name, phone, country_code, timezone, night_start, night_end):
        self.name = name
        self.phone = phone
        self.country_code = country_code
        self.timezone = timezone
        self.night_start = night_start
        self.night_end = night_end
        self.updated_on = datetime.utcnow()


class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(24), db.ForeignKey('users.phone'))
    reminder_status = db.Column(db.Boolean)
    error = db.Column(db.String(512), default="")
    reminder_message = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Reminder(user_id='%s', cron='%s'>" % (self.phone, self.reminder_status)

    def __init__(self, phone, reminder_status, error, reminder_message):
        self.phone = phone
        self.reminder_status = reminder_status
        self.error = error
        self.reminder_message = reminder_message
        self.updated_on = datetime.utcnow()


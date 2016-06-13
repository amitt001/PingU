
import sys
from os import path

import twilio
from twilio.rest import TwilioRestClient

import utils
from models import User, Reminder, db


def send_reminder(to, body, RETRY, FROM, ASID, TOKEN):
    """Send message using twilio"""
    client = TwilioRestClient(ASID, TOKEN)
    counter = 1
    success = False

    #Try resending an SMS if it fails, but retry no more than 5 times.
    error_code, error_message = None, None
    while counter <= RETRY and success is False:
        counter += 1
        try:
            message = client.messages.create(to=to, from_=FROM,
                                             body=body)
            if message.error_code == None:
                success = True
            error_code = message.error_code
            error_message = message.error_message
        except twilio.rest.exceptions.TwilioRestException as e:
            error_code = e.code
            error_message = e.msg
        except Exception as e: #for all other exception
            error_code = -1
            error_message = e

    print error_code, error_message
    return (error_code is None, error_message or "")


def right_time(user):
    """
    Checks whether its right to send reminder. First
    users local time is retrived from user's timezone
            
        user: User model.
    """
    timezone = user.timezone
    start_time = float(user.night_start.replace(':', '.'))
    end_time = float(user.night_end.replace(':', '.'))

    #Get user's timezon's local time
    local_time = utils.local_from_timezone(timezone)
    return not (local_time >= start_time or local_time < end_time)


if __name__ == '__main__' and __package__ is None:
    
    #add parent directory in path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
    #set flaslkapp context for sqlalchemy
    import settings
    from app import app
    db.app = app

    phone = sys.argv[1]
    user = User.query.filter_by(phone=phone).first()
    if right_time(user): 
        message = "Hello there! Your name is " + user.name
        phone_num = user.country_code + phone
        success, error = send_reminder(
                            phone_num, message,
                            settings.RETRY,
                            settings.FROM,
                            settings.ASID,
                            settings.TOKEN)

        rem = Reminder(phone, success, error, message)
        db.session.add(rem)
        db.session.commit()
    else:
        print("Not a right time. Good Night")
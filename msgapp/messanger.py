
import sys
from os import path
from datetime import datetime
from pytz import timezone

from twilio.rest import TwilioRestClient

import cron
from models import User, Reminder, db


_FROM = "+15005550006"
_ASID = "ACde3d9f8915e7be40163284f38b02849b"
_TOKEN = "9468671c1999c05c0e4af55bec5bdf6e"
_RETRY = 1

#not at night, retry 5 times, log error and tell how many hours it has been running

def send_reminder(to, body):
    #send message
    client = TwilioRestClient(_ASID, _TOKEN)
    counter = 0
    success = False

    #Retry 5 times
    error_code, error_message = None, None
    while counter <= _RETRY  and success is False:
        counter += 1
        try:
            message = client.messages.create(to=to, from_=_FROM,
                                             body=body)
            if message.error_code == None:
                success = True
            error_code = message.error_code
            error_message = message.error_message
        except Exception as e:
            pass
    return (error_code == None, error_message or "")


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


def right_time(user):
    """check for the right time to remind"""
    timezone = user.timezone
    start_time = user.night_start
    end_time = user.night_end
    hr_min = local_from_timezone(timezone)
    return not (hr_min >= start_time and hr_min <= end_time)
    


if __name__ == '__main__' and __package__ is None:
    
    #add parent directory in path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    print path.dirname(path.dirname(path.abspath(__file__)))
    #set flaslkapp context for sqlalchemy
    from app import app
    db.app = app
    with open("/home/amit/Codes/cops/scapp/msgapp/test.txt", "w") as f:
        f.write("test")
    phone = sys.argv[1]
    user = User.query.filter_by(phone=phone).first()
    if right_time(user): 
        message = "Hello there! Your name is " + user.name
        success, error = send_reminder(phone, message)
        rem = Reminder(phone, success, error, message)
        db.session.add(rem)
        db.session.commit()
    else:
        print("Not right time. Good Night")
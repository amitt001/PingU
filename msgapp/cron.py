"""Module to manage crons"""

from crontab import CronTab

_CRON = CronTab(user=True)
_PYTHON_PATH = '/home/amit/venv/bin/python'
_MESSENGER_PATH = '/home/amit/Codes/cops/pvtassist/msgapp/messenger.py'


def create(phone):
    base = _PYTHON_PATH + " " + _MESSENGER_PATH + " "
    command =  base + phone
    job = _CRON.new(command=command)
    job.set_comment(phone)
    job.minute.every(2)
    job.enable()
    _CRON.write()
    print job.is_valid()
    print _CRON.render()
    return job.is_valid()

def remove(phone):
    #if 0 i.e. wrong phone number or user doesnt exists
    return cron.remove_all(commant=phone)
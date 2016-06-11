"""Module to manage crons"""

import subprocess
import os, os.path as path

from crontab import CronTab


_CRON = CronTab(user=True)
_MESSENGER_PATH = path.join(path.abspath('.'), 'msgapp', 'messenger.py')
#Get python path
_PYTHON_PATH = subprocess.check_output('which python', shell=True).strip()
_HOUR = 1

def create(phone):
    print _PYTHON_PATH, _MESSENGER_PATH
    base = _PYTHON_PATH + " " + _MESSENGER_PATH + " "
    command =  base + phone
    job = _CRON.new(command=command)
    job.set_comment(phone)
    job.every(_HOUR).hour()
    #job.minute.every(2)
    job.enable()
    _CRON.write()
    print job.is_valid()
    print _CRON.render()
    return job.is_valid()

#!/usr/bin/env python

import datetime
import sys
from crontab import CronTab
import os
import subprocess

def setearHora(programa, limite):
    my_cron = CronTab(user='usuario')	
    job = my_cron.new(command=f'python3 ~/Escritorio/proyecto/main.py {programa} {limite}')
    job.minute.every(1)
    my_cron.write()

def setearReseteoSemanal():
    my_cron = CronTab(user='usuario')
    job = my_cron.new(command="bash scriptReseteoSemanal.sh")
    job.minute.every(59)
    job.hour.every(23)
    job.day.every(6)
    my_cron.write()

setearReseteoSemanal()
setearHora(sys.argv[1], sys.argv[2])

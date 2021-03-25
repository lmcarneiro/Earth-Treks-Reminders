#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crontab import CronTab
import os

def delete_cron():
    
    cron = CronTab(user='User')
    job = next(cron.find_comment('Earth Treks'))
    cron.remove(job)
    cron.write()
    os.remove('/path/start.txt')
    os.remove('/path/date.txt')
    print('Cron job was deleted.')
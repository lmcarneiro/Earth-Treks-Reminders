#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Must be called in terminal as 'earth_treks_v1.py receiver(s) date_choice time'
"""

import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
import re
from reminder import reminder
from crontab import CronTab
import sys

cron = CronTab(user='lucas')
job = next(cron.find_comment('Earth Treks'))
job.enable()
cron.write()

args = sys.argv
args = iter(args[1:])
receiver = []
while True:
    i = next(args)
    if i.isdigit() is False:
        receiver.append(i)
    if i.isdigit() is True:
        date_choice = int(i)
        break
time = int(next(args))


ET_URL = 'https://app.rockgympro.com/b/widget/?'

headers_g = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

headers_p = {'User-Agent': 'Mozilla/5.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest' }

params_g = {'a':'offering',
          'offering_guid':'2923df3b2bfd4c3bb16b14795c569270',
          'random':'60536721b6263',
          'iframeid':'',
          'mode':'p'}

params_p = {'a':'equery'}

session = requests.Session()

show_date = date.today() + timedelta(days = date_choice)

data = {
	"PreventChromeAutocomplete": "",
	"random": "60537a225b5d3",
	"iframeid": "",
	"mode": "p",
	"fctrl_1": "offering_guid",
	"offering_guid": "2923df3b2bfd4c3bb16b14795c569270",
	"fctrl_2": "course_guid",
	"course_guid": "",
	"fctrl_3": "limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270",
	"limited_to_course_guid_for_offering_guid_2923df3b2bfd4c3bb16b14795c569270": "",
	"fctrl_4": "show_date",
	"show_date": show_date,
	"ftagname_0_pcount-pid-1-316074": "pcount",
	"ftagval_0_pcount-pid-1-316074": "1",
	"ftagname_1_pcount-pid-1-316074": "pid",
	"ftagval_1_pcount-pid-1-316074": "316074",
	"fctrl_5": "pcount-pid-1-316074",
	"pcount-pid-1-316074": "0",
	"ftagname_0_pcount-pid-1-6420306": "pcount",
	"ftagval_0_pcount-pid-1-6420306": "1",
	"ftagname_1_pcount-pid-1-6420306": "pid",
	"ftagval_1_pcount-pid-1-6420306": "6420306",
	"fctrl_6": "pcount-pid-1-6420306",
	"pcount-pid-1-6420306": "0",
	"ftagname_0_pcount-pid-1-6304903": "pcount",
	"ftagval_0_pcount-pid-1-6304903": "1",
	"ftagname_1_pcount-pid-1-6304903": "pid",
	"ftagval_1_pcount-pid-1-6304903": "6304903",
	"fctrl_7": "pcount-pid-1-6304903",
	"pcount-pid-1-6304903": "0",
	"ftagname_0_pcount-pid-1-6304904": "pcount",
	"ftagval_0_pcount-pid-1-6304904": "1",
	"ftagname_1_pcount-pid-1-6304904": "pid",
	"ftagval_1_pcount-pid-1-6304904": "6304904",
	"fctrl_8": "pcount-pid-1-6304904",
	"pcount-pid-1-6304904": "0",
	"ftagname_0_pcount-pid-1-6570973": "pcount",
	"ftagval_0_pcount-pid-1-6570973": "1",
	"ftagname_1_pcount-pid-1-6570973": "pid",
	"ftagval_1_pcount-pid-1-6570973": "6570973",
	"fctrl_9": "pcount-pid-1-6570973",
	"pcount-pid-1-6570973": "0",
	"ftagname_0_pcount-pid-1-6570974": "pcount",
	"ftagval_0_pcount-pid-1-6570974": "1",
	"ftagname_1_pcount-pid-1-6570974": "pid",
	"ftagval_1_pcount-pid-1-6570974": "6570974",
	"fctrl_10": "pcount-pid-1-6570974",
	"pcount-pid-1-6570974": "0"
}

res_get = session.get(ET_URL, headers=headers_g, params=params_g)
cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
res_pos = session.post(ET_URL, headers=headers_p, params=params_p, data=data,
                       cookies=cookies)

content_g = res_get.content

available_json = res_pos.json()

available_soup = BeautifulSoup(available_json['event_list_html'], features='lxml')
times = available_soup.find_all('td', attrs={'class':'offering-page-schedule-list-time-column'})
times = [time.text.strip('\n') for time in times]
slots = available_soup.find_all(string=re.compile('space'))
no_slot = available_soup.find_all(string=re.compile('full'))
slots = [slot.strip('\n') for slot in slots]
time_slots = dict(zip(times, slots))

print(time_slots)
print()

slot_v = []
if len(time_slots.keys()) > 0:
    slot_t = list(time_slots.keys())[time]
if len(time_slots.values()) > 0:
    slot_v = list(time_slots.values())[time]

if 'space' in slot_v:
    num_slots = int(slot_v.split(' spaces')[0])
    if num_slots == 1:
        message = ('Subject: Your Sign-Up Reminder\n\nThere is 1 spot available'
                   ' on {}.\n\nThis message was sent from Python.').format(slot_t)
    elif num_slots > 1:
        message = ('Subject: Your Sign-Up Reminder\n\nThere are {0} spots'
                  ' available on {1}.\n\nThis message was sent'
                  ' from Python.').format(num_slots, slot_t)
    print(message)
    reminder(receiver, message)
    cron = CronTab(user='lucas')
    job = next(cron.find_comment('Earth Treks'))
    job.enable(False)
    cron.write()
else:
    print('Crontab is running this script every minute until a spot opens up')

# Earth-Treks-Reminders
Get notified when a reservation opens up at Earth Treks!

*Please note that the POST request is currently only for the Crystal City location in VA.*

You will have to set up an email account that can send the reminder emails for you. You can follow the tutorial at https://realpython.com/python-send-email/.

You have to provide arguments when you run the script in the command line,

`$ python earth_treks_v1.py arg1 arg2 arg3 arg4.`

* The last argument will always be the index of the time slot you want to check in ascending order (first slot of the day is 0, etc.).
* The previous argument will be the number of days ahead you want to check (today is 0, tomorrow is 1, etc.).
* Any arguments before that must be receiver email addresses.

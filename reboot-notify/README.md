reboot-notify
=============

Small python script that gets run as a weekly cron job. The script checks if
its the first week of the month and if so, sends an email message to a
configured list of recipients.

Usage
-----
Add the following line to your crontab:

    00 09 * * 3     cd <path-to-reboot-notify> && ./reboot_notifier.py

and configure the addresses in `reboot-notify.cfg` and the message content in
`notification_msg.txt`.

I help run my labs computing servers and often times lab mates have long
running processes that we don't want to kill prematurely, but we don't want to
skip applying security updates that might require a reboot. Instead of tracking
down all the long running processes and asking the owner if they still need it,
this sends out a gentle reminder each month. If a user needs to keep their
processes running, they can let us know.

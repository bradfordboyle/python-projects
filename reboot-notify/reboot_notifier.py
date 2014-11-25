#!/usr/bin/env python
# -*- coding: utf-8 -#-

import datetime
import smtplib
from email.mime.text import MIMEText
import ConfigParser

def _load_config(conf_file):
    config = ConfigParser.RawConfigParser()
    config.read(conf_file)
    return config


def user_list(users):
    users_as_list = users.split(',')
    email = lambda u: u + '@drexel.edu'
    return map(email, users_as_list)


def send_msg(config):
    msg_file = config.get('general', 'msg_file')
    with open(msg_file, 'rb') as f:
        msg = MIMEText(f.read())
    users = user_list(config.get('general', 'users'))
    to = config.get('general', 'to_addr')
    msg['Subject'] = config.get('general', 'subject')
    msg['From'] = config.get('general', 'from_addr')
    msg['To'] = to
    msg['Bcc'] = ', '.join(users)
    
    to_addrs = [to] + users        
    s = smtplib.SMTP('smtp.mail.drexel.edu')
    s.sendmail(me, to_addrs, msg.as_string())
    s.quit()


def first_day():
    day_of_month = datetime.datetime.today().day
    return (day_of_month <= 7)


def main():
    if first_day():
        config = _load_config('reboot-notify.cfg')
        send_msg(config)
    else:
        print('It is not the first day of the month!')


if __name__ == '__main__':
    main()

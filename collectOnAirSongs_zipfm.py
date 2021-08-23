#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Collect On Air Songs
# import
## default
import datetime
import sys

## scraping
import requests
from bs4 import BeautifulSoup

## mail
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


args = sys.argv
if 4 != len(args):
    print('invalid argument.')
    sys.exit(0)

# CONST
TODAY = datetime.datetime.today()
TODAY = TODAY.strftime('%Y/%m/%d')

# Radio Station
ZIP_FM = 'http://noa.media-click.net/FM/zip-fm/include/oalist.html?vd=' + TODAY

# mail settings
SMTP_SERVER = ''
SMTP_PORT = ''
ACCOUNT = ''
PASSWD = ''
TO = ''

# argument check
def arg_check():
    global SMTP_SERVER
    global SMTP_PORT
    global ACCOUNT
    global PASSWD
    global TO

    args = sys.argv

    if 4 != len(args):
        print('invalid argument.')
        sys.exit(0)

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    ACCOUNT = args[1]
    PASSWD = args[2]
    TO = args[3]

def create_mail():
    global SMTP_SERVER
    global SMTP_PORT
    global ACCOUNT
    global PASSWD
    global TO

    # message settings
    msg = MIMEMultipart('alternative')

    # subject
    msg['Subject'] = '[ZIP-FM]' + TODAY

    # from
    msg['From'] = ACCOUNT

    # to
    msg['To'] = TO

    # Access
    response = requests.get(ZIP_FM)
    soup = BeautifulSoup(response.content, 'html.parser')

    # message
    message = '<table border="1" bordercolor="black" bgcolor="white">'
    time_list = soup.find_all('td', class_='f9', width='12%')
    artist_list = soup.find_all('td', class_='f9', width='48%')
    song_list = soup.find_all('td', class_='f9', width='40%')
    for time, artist, song in zip(time_list,artist_list,song_list):
        message = message + '<tr align="left">'
        message = message + '<th>' + time.text + '</th>' + '<th>' + artist.text + '</th>' + '<th>' + song.text + '</th>'
        message = message + '</tr>'
    message = message + '</table>'

    html_msg = MIMEText(message, 'html')
    msg.attach(html_msg)

    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context())
    smtp.login(ACCOUNT, PASSWD)
    smtp.send_message(msg)
    smtp.quit()
    print('Done')

# main
def main():
    arg_check()
    create_mail()

if __name__ == '__main__':
    main()
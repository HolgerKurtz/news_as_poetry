from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice

import email
import imaplib
import re

from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_APP_PW = os.getenv("GMAIL_APP_PW")
INSTAGRAM_PW = os.getenv("INSTAGRAM_PW")
CHALLENGE_EMAIL = "kulturdata@googlemail.com"


def get_code_from_email(username):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(CHALLENGE_EMAIL, GMAIL_APP_PW)
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    assert result == "OK", "Error1 during get_code_from_email: %s" % result
    ids = data.pop().split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # mark as read
        result, data = mail.fetch(num, "(RFC822)")
        assert result == "OK", "Error2 during get_code_from_email: %s" % result
        msg = email.message_from_string(data[0][1].decode())
        payloads = msg.get_payload()
        if not isinstance(payloads, list):
            payloads = [msg]
        code = None
        for payload in payloads:
            body = payload.get_payload(decode=True).decode()
            if "<div" not in body:
                continue
            match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
            if not match:
                continue
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if not match:
                print('Skip this email, "code" not found')
                continue
            code = match.group(1)
            if code:
                return code
    return False

def get_code_from_sms(username):
    while True:
        code = input(f"Enter code (6 digits) for {username}: ").strip()
        if code and code.isdigit():
            return code
    return None

def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        return get_code_from_sms(username)
    elif choice == ChallengeChoice.EMAIL:
        pw = get_code_from_email(username)
        print(f"PW BY MAIL: {pw}", flush=True)
        return pw
    return False

def post_insta_pic(pic, caption):
    cl = Client()
    cl.challenge_code_handler = challenge_code_handler
    try:
        cl.load_settings('insta_login_settings.json')
    except:
        pass
    cl.login("news_as_poetry", INSTAGRAM_PW)
    cl.dump_settings('insta_login_settings.json')
    cl.photo_upload(pic,caption)

if __name__ == "__main__":
    get_code_from_email("news_as_poetry")
    # post_insta_pic("/Users/holgerkurtz/Documents/news_as_poems/static/images/a-bestseller-book,-digital-art.jpg", "test")

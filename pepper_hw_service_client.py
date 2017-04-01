import os
import qi
import sys
import time
from time import gmtime, strftime


def response_cb(data):
    clear()
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print data


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

app = qi.Application(sys.argv)
app.start()
sess = app.session
phws = sess.service("pepper_hardware_service")
phws.send.connect(response_cb)

while True:
    phws.request()
    time.sleep(10)

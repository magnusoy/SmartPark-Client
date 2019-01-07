#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartPark - Client Application
Short description...

Code by: Magnus Øye, Dated: 14.12-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/
"""

# Importing packages
from lib.client import Client
from datetime import datetime, timedelta
import configparser
import time


# Communicates with server
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("../instance/config.ini")
    client = Client()
    response = client.addParkinglot(config['Settings']['name'], config['Settings']['location'], config['Settings']['size'])
    print(response)
    print("New token accuired: {}".format(client.token))
    tokenTime = datetime.now()
    while client.isConnected():
        lastTokenUpdate = datetime.now() - tokenTime
        if lastTokenUpdate > timedelta(days=29):
            client.getToken()
            print("New token accuired: {}".format(client.token))
            tokenTime = datetime.now()
        response = client.updateParkinglot()
        print(response)
        time.sleep(60)

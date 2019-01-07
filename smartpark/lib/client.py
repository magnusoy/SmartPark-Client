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
import requests
import json
import configparser


class Client(object):
    """Handels the parkinglots for the given client."""

    def __init__(self):
        """Reads configure files and requests for a secure token."""
        self.config = configparser.ConfigParser()
        self.token = self.getToken()

    def getToken(self):
        """Fetches a new secure token from the server."""
        self.config.read("../instance/config.ini")
        try:
            r = requests.get('http://localhost:5000/login', auth=(
                "magnusoy", "password"))
            data = json.loads(r.text)
            self.token = data['token']
            return self.token
        except requests.exceptions.ConnectionError:
            print(
                "\nCan't establish secure connection to server, please check your connection.\n")

    def addParkinglot(self, name, location, size):
        """Adds a new parkinglot to the database."""
        payload = {
            "name": name,
            "location": location,
            "size": size,
            "empty": size
        }
        if len(self.config['Settings']['ID']) > 0:
            return "Parkinglot ID: {}".format(self.config['Settings']['ID'])
        else:
            r = requests.post(
                'http://localhost:5000/parkinglots?token={}'.format(self.token), json=payload)
            print(r)
            data = json.loads(r.text)
            self.config.set('Settings', 'ID', str(data['id']))
            with open('../instance/config.ini', 'w+') as configfile:
                self.config.write(configfile)
            return data

    def updateParkinglot(self):
        """Updates the parkinglot."""
        self.config.read("../instance/config.ini")
        payload = {
            "name": self.config['Settings']['Name'],
            "location": self.config['Settings']['Location'],
            "size": self.config['Settings']['Size'],
            "empty": self.config['Settings']['Empty']
        }
        parkinglotID = self.config['Settings']['ID']
        r = requests.put(
            'http://localhost:5000/parkinglots/{}?token={}'.format(parkinglotID, self.token), json=payload)
        data = json.loads(r.text)
        return data

    def deleteParkinglot(self, parkinglotID):
        """docstring"""
        r = requests.delete(
            'http://localhost:5000/parkinglots/{}?token={}'.format(parkinglotID, self.token))
        data = json.loads(r.text)
        return data

    def isConnected(self):
        """docstring"""
        if len(self.token) > 0:
            return True
        else:
            return False


if __name__ == "__main__":
    client = Client()
    client.getToken()
    num = input("speak: ")
    client.deleteParkinglot(int(num))
        
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
from lib.utility import configure, settings
from lib.parkdetection import run


def startUpMsg():
    """Displays the startup message to the user."""
    print("\nWelcome to SmartPark!\n*********************\nCode by: Magnus Kvendseth Øye\nVersion: 0.2\nDated: 14.12-2018\nContact: magnus.oye@gmail.com\nWebsite: https://github.com/magnusoy/\n*********************\n")


def menu():
    """Displays the main menu to the user."""
    print("\nMain Menu\n1.Run\n2.Configure parkinglot\n3.Overlay settings\n4.Quit")


def close():
    """Closes the application."""
    confirm = input("\nAre you sure you want to quit? [Y/N]")
    if confirm.lower() == "y":
        print("\nThank you for using SmartPark.")
        quit()
    else:
        pass


# Main script
if __name__ == "__main__":
    startUpMsg()
    while True:
        menu()
        menuChoice = input("\nPlease choose one of the options: ")
        if menuChoice == "1":
            run()
        elif menuChoice == "2":
            configure()
        elif menuChoice == "3":
            settings()
        elif menuChoice == "4":
            close()
        else:
            print("\nNot a valid input, please try again.")

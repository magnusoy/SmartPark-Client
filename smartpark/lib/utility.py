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
import os
import configparser
import json
import cv2

points = []


def confMenu():
    """Displays the parkinglot configuration menu to the user."""
    print("\nConfigure Menu\n1.Add parkinglot\n2.Update parkinglot\n3.Delete parkinglot\n4.Close menu")


def settingMenu():
    """Displays the overlay settings menu to the user."""
    print("\nSettings Menu\n1.Create overlay\n2.Load overlay\n3.Delete overlay\n4.Close menu")


def addConfigureFile(config):
    """Add a new parkinglot by assigning attributes."""
    filename = "../instance/config.ini"
    exists = os.path.isfile(filename)
    if exists:
        delete = input(
            "\n Configurefile already exists.\nWould you like to delete current configurations? [Y/N]")
        if delete.lower() == "y":
            deleteConfigureFile()
        else:
            pass
    else:
        print("\nCreating new configurations.\nPlease fill in the required values: ")
        username = input("\nUsername: ")
        password = input("Password: ")
        print("\nParkinglot attributes")
        name = input("Name: ")
        location = input("Location: ")
        size = input("Size: ")
        with open(filename, "w") as f:
            f.write(
                "[Settings]\nusername = \npassword = \nID = \nname = \nlocation = \nsize = \nempty = ")
        config.read(filename)
        config.set('Settings', 'username', username)
        config.set('Settings', 'password', password)
        config.set('Settings', 'name', name)
        config.set('Settings', 'location', location)
        config.set('Settings', 'size', size)
        with open(filename, 'w+') as configfile:
            config.write(configfile)
        print("Configurations saved.")


def deleteConfigureFile():
    """Delete parkinglot configurations."""
    filename = "../instance/config.ini"
    if os.path.exists(filename):
        deleting = input("\nConfirm [Y/N]: ")
        if deleting.lower() == "y":
            os.remove(filename)
            print("\Configurations deleted.")
        else:
            pass
    else:
        print("Configurations does not exist yet.")


def addPoints(event, x, y, flag, param):
    """Records left button mouse clicks on the image,
     and collects 4 coordinates."""
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print("\nAdding point: ({},{})".format(x, y))


def draw_border(img, points):
    """Draws 4 circles on the image from the given points."""
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    cv2.circle(img, (x1, y1), 3, (255, 0, 255), -1)  # -- top_left
    cv2.circle(img, (x2, y2), 3, (255, 0, 255), -1)  # -- bottom-left
    cv2.circle(img, (x3, y3), 3, (255, 0, 255), -1)  # -- top-right
    cv2.circle(img, (x4, y4), 3, (255, 0, 255), -1)  # -- bottom-right
    return img


def savePoints(filename, parkID):
    """Saves the points in a.yml format."""
    with open(filename, 'a') as f:
        f.write(
            "-\n    id: {}\n    points: [[{},{}],[{},{}],[{},{}],[{},{}]]\n".format(parkID, points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1]))
        f.close()


def createOverlay():
    """Create a new overlay for the parkinglot."""
    print("\nPlace 4 points to draw a rectangle.\nPress 's' to save the points, or 'r' to discard them.\nPress 'q' when you are finished.\n")
    parkID = 0
    overlayEditing = True
    try:
        img = input("\nPlease provide the full path to image: ")
        overlayName = input(
            "\nPlease provide a new name for the overlay: ")
        f = open(os.path.join("../instance/overlays", overlayName+".yml"), "w")
        f.close()
        img = cv2.imread(img)
        copy = img.copy()
    except AttributeError as e:
        overlayEditing = False
        print("Closing edit, please provide a valid filename.")

    cv2.namedWindow('Parkinglot', 1)
    cv2.setMouseCallback('Parkinglot', addPoints, None)
    while overlayEditing:
        if len(points) == 4:
            copy = draw_border(copy, points)
            if k == ord('s'):
                savePoints(os.path.join("../instance/overlays",
                                        overlayName+".yml"), parkID)
                img = copy.copy()
                parkID += 1
                points.clear()
                print("\nPoints saved, you can now proceed to add more.")

            if k == ord('r'):
                print("\nPoints removed,you can now proceed to add more.")
                copy = img.copy()
                points.clear()

        cv2.waitKey(1)
        cv2.imshow('Parkinglot', copy)

        k = cv2.waitKey(10)
        if k == ord('q'):
            print("\nClosing edit, all parkingspots are saved.")
            overlayEditing = False
    cv2.destroyAllWindows()


def loadOverlay():
    """Select and load a new overlay from the saved list."""
    base = "../instance/overlays/"
    overlays = []
    index = 1
    print("\nOverlays that are accessible: ")
    for file in os.listdir(base):
        if file.endswith(".yml"):
            overlays.append(file)
            print("{}. {}".format(index, file))
            index += 1
    print("{}. Cancel".format(index))
    newOverlay = int(input("\nPlease select one form the list: "))
    if newOverlay >= (index):
        print("Canceled!")
    else:
        with open('../instance/settings.json') as f:
            settings = json.load(f)
        settings["detection"]["overlay"] = os.path.join(
            base, overlays[newOverlay-1])
        with open('../instance/settings.json', 'w') as f:
            f.write(json.dumps(settings, indent=4))
        print("{} is now loaded.\n".format(overlays[newOverlay-1]))

def deleteOverlay():
    """Delete one overlay from the saved list."""
    base = "../instance/overlays/"
    overlays = []
    index = 1
    print("\nOverlays that are accessible: ")
    for file in os.listdir(base):
        if file.endswith(".yml"):
            overlays.append(file)
            print("{}. {}".format(index, file))
            index += 1
    print("{}. Cancel".format(index))
    newOverlay = int(input("\nPlease select one form the list: "))
    if newOverlay >= (index):
        print("Canceled!")
    else:
        confirm = input("Confirm: [Y/N]")
        if confirm.lower() == "y":
            os.remove(os.path.join(base, overlays[newOverlay-1]))
            print("\n{} is now deleted.".format(newOverlay-1))
        else:
            print("Canceled!")


def configure():
    """Menu selector for parkinglot configurations."""
    config = configparser.ConfigParser()
    inConfigure = True
    while inConfigure:
        confMenu()
        menuChoice = input("\nPlease choose one of the options: ")
        if menuChoice == "1":
            addConfigureFile(config)
        elif menuChoice == "2":
            updateConfigurations()
        elif menuChoice == "3":
            deleteConfigureFile()
        elif menuChoice == "4":
            inConfigure = False
            print("\nClosing configure menu.")
        else:
            print("\nNot a valid input, please try again.")


def settings():
    """Menu selector for overlay settings."""
    inSettings = True
    while inSettings:
        settingMenu()
        menuChoice = input("\nPlease choose one of the options: ")
        if menuChoice == "1":
            createOverlay()
        elif menuChoice == "2":
            loadOverlay()
        elif menuChoice == "3":
            deleteOverlay()
        elif menuChoice == "4":
            inSettings = False
            print("\nClosing settings menu.")
        else:
            print("\nNot a valid input, please try again.")

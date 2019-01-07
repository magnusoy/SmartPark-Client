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
import cv2
import numpy as np
import yaml
import json
import configparser
from lib.prediction import loadModel, getParkingStatus


def updateStatus(numOfEmptySlots):
    """Updates the number of empty parkingslots."""
    filename = "../instance/config.ini"
    config = configparser.ConfigParser()
    config.read(filename)
    config.set('Settings', 'empty', str(numOfEmptySlots))
    with open(filename, 'w+') as configfile:
            config.write(configfile)
    print("\nUpdating parkinglot: {}/{}".format(numOfEmptySlots, config['Settings']['size']))


def run():
    """Finds the number of empty parkingspots."""
    model = loadModel()
    points = []
    parkingStatus = []
    with open('../instance/settings.json') as f:
        settings = json.load(f)
    overlay = settings["detection"]["overlay"]
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    # Read YAML data (parking space polygons)
    with open(overlay, 'r') as stream:
        parking_data = yaml.load(stream)

    parking_contours = []
    parking_bounding_rects = []
    parking_mask = []

    for park in parking_data:
        points = np.array(park['points'])
        rect = cv2.boundingRect(points)
        points_shifted = points.copy()
        points_shifted[:, 0] = points[:, 0] - \
            rect[0]  # shift contour to roi
        points_shifted[:, 1] = points[:, 1] - rect[1]
        parking_contours.append(points)
        parking_bounding_rects.append(rect)
        mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                color=255, thickness=-1, lineType=cv2.LINE_8)
        mask = mask == 255
        parking_mask.append(mask)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            print("Capture Error")
            break

        parkingStatus.append(getParkingStatus(model))
        frame_out = frame.copy()
        for spotID, park in enumerate(parking_data):
            points = np.array(park['points'])
            r = cv2.boundingRect(points)
            cv2.imwrite('../instance/images/{}.png'.format(park['id']), cv2.resize(
                frame[r[0]:r[0]+r[2], r[1]:r[1]+r[3]], dsize=(64, 64), interpolation=cv2.INTER_LINEAR))
            status = parkingStatus[0][spotID]
            if status:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            cv2.drawContours(frame_out, [points], contourIdx=-1,
                             color=color, thickness=2, lineType=cv2.LINE_8)
            moments = cv2.moments(points)
            try:
                centroid = (int(moments['m10']/moments['m00'])-3,
                            int(moments['m01']/moments['m00'])+3)
                cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]+1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]-1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), (centroid[0]+1, centroid[1]-1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), (centroid[0]-1, centroid[1]+1),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(
                    park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            except ZeroDivisionError:
                print(
                    "\nNo valid points.\nPlease use another overlay.\nPress 'q' to quit")
        numOfEmptySlots = sum(parkingStatus[0])
        updateStatus(numOfEmptySlots)
        parkingStatus.clear()

        # Display video
        cv2.imshow('frame', frame_out)
        k = cv2.waitKey(10)
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

# SmartPark-Client

SmartPark-Client contains the user interface for the SmartPark application.
This solution is supposed to run on a Raspberry Pi, but will work with linux, windows computers aswell.
It is possible to run the application alone as seen in the Examples, but you will have to download the server application for full functionality.
With doing so you will be able to add, update your parkingspots on the server.


Go to [SmartPark-Server](https://github.com/magnusoy/SmartPark-Server) for more imformation setting it up.


### Prerequisites

You will need [Python 3](https://www.python.org/) for using the provided files.
Furthermore you will need to install all the dependencies listed below.

Install all of the following:
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y xterm
sudo apt-get install python3-dev libffi-dev libssl-dev -y
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install python3-pyqt5
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev

```

### Installing

Clone or download repository to your home directory.

```bash
cd ~
git clone https://github.com/magnusoy/SmartPark-Client.git
```

Install dependencies
```bash
pip3 install -r /path/to/requirements.txt

or

pip3 install requests
pip3 install opencv-python
pip3 install pyyaml
pip3 install keras
pip3 install Theano
pip3 install tensorflow
pip3 install cython
```

### Example

This example will show you how to add a parkinglot and create a overlay for your parkingspots.


To run the application :
```bash
cd ~/SmartPark-Client/smartpark
sh run.sh
```
Press Ctrl+C in the terminals to close the applications.

Leave the communication window alone.
You will now have the application running in the second window,
and be presented with the main menu.

Press the menuchoices marked with *

```
Main Menu
1.Run
2.Configure parkinglot *
3.Overlay settings
4.Quit

----------------------------------

Configure Menu
1.Add parkinglot *
2.Update parkinglot
3.Delete parkinglot
4.Close menu

Creating new configurations.
Please fill in the required values: 

Username: magnusoy 
Password: password

Parkinglot attributes
Name: Parkinglot X
Location: 62.733471,7.1434657
Size: 76  
Configurations saved.

You have now added a parkinglot. We will now proceed to create the overlay.

----------------------------------

Main Menu
1.Run
2.Configure parkinglot
3.Overlay settings *
4.Quit

----------------------------------

Settings Menu
1.Create overlay *
2.Load overlay
3.Delete overlay
4.Close menu

Place 4 points to draw a rectangle.
Press 's' to save the points, or 'r' to discard them.
Press 'q' when you are finished.


Please provide the full path to image: ../instance/parkinglots/parkinglot.png

Please provide a new name for the overlay: myoverlay

Adding point: (156,338)

Adding point: (220,336)

Adding point: (233,365)

Adding point: (160,371)

Points saved, you can now proceed to add more.

Closing edit, all parkingspots are saved.

----------------------------------

At default a another overlay is selected, so wi will have to select our new one.

Settings Menu
1.Create overlay
2.Load overlay *
3.Delete overlay
4.Close menu 

Overlays that are accessible: 
1. default.yml
2. myoverlay.yml *
3. Cancel

Please select one form the list: 2
myoverlay.yml is now loaded.

----------------------------------

You are now done and you will be able to run the application.

Main Menu
1.Run *
2.Configure parkinglot
3.Overlay settings
4.Quit

Remember to click 'q' to stop the process and get back to Main Menu again.

----------------------------------

```


### Usage with SmartPark-Server

Follow the example for adding a dummy parkinglot.

Be sure to checkout [SmartPark-Server](https://github.com/magnusoy/SmartPark-Server) to get the server running.
When the server is running you can run the client application.

```bash
cd ~/SmartPark-Client/smartpark
sh run.sh
```
Choose Run in the Main Menu and navigate to http://localhost:5000/overview in your browser.
Your parkinglot should now be on the map and you can get information about it by clicking on the marker.


## Built With

* [Python](https://www.python.org/) - Python

## Contributing

If you want to contribute or find anything wrong, please create a Pull request, or issue addressing the change, or issue.


## Author

* **Magnus Øye** - [magnusoy](https://github.com/magnusoy)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/magnusoy/SmartPark-client/blob/master/LICENSE) file for details


## Libraries

[Requests](http://docs.python-requests.org/en/master/)

[OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)

[Numpy](http://www.numpy.org/)

[Keras](https://keras.io/)

[Tensorflow](https://www.tensorflow.org/)

[PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

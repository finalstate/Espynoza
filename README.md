# Remark:
Please be patient, documentation will be worked on. For the moment, refer to the [Tutorial](https://github.com/finalstate/Espynoza/blob/master/doc/Tutorial.md)

# Introduction
Espynoza is a Python framework for writing, configuring and managing applications on ESP8266 microcontroller boards.

Espynoza supports remote uploading of files/sources via USB cable, or via Wifi/??MQTT?? once the basic software is installed on the target board. Multiple MQTT servers as well as distinct Wifi Access Points may be configured.

All user actions are made through a command-line interface, *Espynoza.py* (use --help for details). Configuration is made via Python files (basically variable assignments). Configuration files exist on the global level, as well as for the individual target devices.

The framework, running on the target device, handles the initial setup of the Wifi network connection and then establishes a connection with the specified MQTT broker. The host server may then send commands to the target device, using standard Python syntax, and will receive data produced on the target. The frameworks main loop calls (user-definable) handlers to perform actions such as setting outputs and reading sensor data. A watchdog will reboot the target if the board hangs.

Right now, some simple sample handlers are provided with Espynoza, more will follow soon. The aim is to create a library that will allow the user to build a system by writing a configuration file for simple cases, but that may be extended by writing small code fragments in Python for more special cases.

Special care has been been taken to use as little memory as possible on the target devices. Python files may be compiled on the host system before being uploaded to avoid out of memory conditions during system startup. Only the files needed for the targets configuration are loaded into RAM.

(BTW, in case you wonder why some things are designed the way they are: I plan to write a web/database-based application to make using Espynoza easier. But first things first...)

## Version
Current version is *0.2*,.
This version should be considered alpha quality, even though the code should work if Espynoza and all needed libraries and tools are installed correctly.
Right now, the number of available handlers is limited to simple digital and analog IO, as well as some I2C or similar serial communication protocol devices. More will follow as soon as the basic code is stable.

# Download and Install
## Requirements
* Hardware
  * Host computer
    * PC running Linux (maybe other OS)
    * or a Raspberry Pi running Linux (Ubuntu Jessie works)
    * Python >= 3.6 (3.6 minimum, as format strings are used)
  * Target
    * ESP6288
    * (more to come)

* Software packages
  * git
  * MicroPython
  * Mosquitto (and paho-mqtt)
  * ampy (from Adafruit)
  * esptool.py
  * (esp-open-sdk -- optional, needed to build custom runtimes, no support yet)

## Install

*Remark*: the following instructions worked for me, your mileage may vary. Please drop me a note if you have problems, I will try to help, and amend these instructions.

## Install using pip

This is the easy way to install Espynoza. It will not only install Espynoza, but also the other necessary packages (except one, see below).
```
sudo pip3 install Espynoza
```
_You absolutely need python3.6 or later, as format-strings are used_

Additionnally, we need to install the Micropython package:

**MicroPython**: the MicroPython language files, and its compiler. Install this using Github, and build the compiler yourself (the pre-build one provided for download is notoriously out of date, and your code might not work with it):
```
git clone https://github.com/micropython/micropython.git
cd micropython/mpy-cross
make
```
This will create the mpy-cross compiler executable. Open the file *EspyConfig.py* in the Espynoza root directory. There you will find the following line:
```
C_MpyCross = './bin/mpy-cross'
```
You may either change this to point to your brand-new compiler, or create the bin sub-directory and create a symbolic link to the compiler in this directory (or use your own strategy, Espynoza is designed to be flexible).

To start working, go to a directory of your choice, and execute
```
espynoza --setup myinstallation
```
This will create a directory _myinstallation_, and copy/create some files into in. Of course, you may name this directory whatever you like, and you may create more than one such directory, for instance if you want to maintain several distinct IoT setups.

**Mosquitto**: the MQTT broker used as a communication hub for Espynoza (and potentially many more sub-systems of your IoT installation.)

If you use Debian or Ubuntu, the following should work:

```
sudo su
apt-get update
apt-get upgrade
apt-get install mosquitto mosquitto-clients
```

Please refer to the mosquitto documentation for configuration and usage. The out-of-the-box config should be OK if you are happy without security settings...


## Installing Espynoza from Github

**Espinoza**: clone Espynoza from GitHub using this command:
```
git clone https://github.com/finalstate/Espynoza.git
```
This will create a directory called Espynoza containig the Espynoza.py cli tool, a basic configuration file and a number of sub-directories.

Moreover you will need to install the following packages to use Espynoza. Install them in some convenient place on your disk, not into the Espinoza directory.

**MicroPython**: see above

**Mosquitto**: see above

The next tools are normally installed automatically if using pip, here we need to do it manually if they are not yet installed
**esptool**: This tool is used to flash the target flash memory, and to upload the MicroPython firmware
```
sudo pip3 install esptool
```

**ampy**: This library is used to initially upload Python files to the target board. Install like this:
```
sudo pip3 install adafruit-ampy
```

**paho-mqtt**: a Python library for using MQTT. Again, we install using pip:

```
sudo pip3 install paho-mqtt
```

# Tutorial
[Here](https://github.com/finalstate/Espynoza/blob/master/doc/Tutorial.md) is a simple tutorial to get you started with Espynoza. First, we will set up some basic hardware, and then install the software on it to get a feeling for how Espinoza works and what it can do for us.

## Troubleshooting
To be completed 


# Architecture overview
_(to be written once things settle down somewhat)_

## File organization

# Reference

# Contributing, bug reports, comments, ideas e.t.c.

Contact me at finalstate@cassy.lu

# Known issues
- out of order file chunk transfers
- dir name ESP is sub-optimal

# Upcoming
(help welcome :-) )

* DHCP address for target


* custom firmware building support
* https support for mqtt connections
* cli commands: rename board, move target to another broker
* tested/enhanced espylisten command (currently VERY alpha)


* ESP32 support (if and when MicroPython supports the stuff needed)

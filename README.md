# Remark:
**Info will be completed a.s.a.p., but if you happen to stumble on this project, feel free to use.**


Please be patient, doc. will be worked on before first public announcement

# Introduction
Espynoza is a framework for writing, configuring and managing applications on ESP8266 microcontroler boards.

Espynoza supports remote uploading of files/sources via USB cable, or via Wifi/MQTT once the basic software is installed. Multiple MQTT servers may be configured as well as distinct Wifi Hotspots. 

All user actions are made through a command-line interface, *Espynoza.py* (use --help for details). Configuration is made via Python files (basically variable assignments). Configuration files exist on the global level, as well as for the individual target devices.

The framework, running on the target device, handles initial connection to the Wifi network, and then establishes a connection with the specified MQTT broker. The host server may then send commands to the target device, using standard Python syntax, and will receive data produced on the target. The frameworks main loop calls (user-definable) handlers to perform actions such as setting outputs and reading sensor data. 

Some simple sample handlers are provided with Espynoza, more will follow soon. The aim is to create a library that will allow the user to build a system by writing a configuration file for simple cases, but that may be extended simply by writing small code fragments in Python for more special cases.

Special care has been been taken to use as little memory as possible on the target devices. Python files may be compiled on the host system before being uploaded to avoid out of memory conditions during system startup. Only the files needed for the targets configuration are loaded into RAM.

(BTW, in case you wonder why some things are designed the way they are, I plan to write a web/database-based application to make using Espynoza easier. But first things first...) 

## Version
Current version is 0.1, the initial commit.
This version should be considered alpha quality, even though the code should work if Espynoza and all needed libraries and tools are installed correctly.
Right now, the number of available hardware drivers is limited to simple digital and analog IO, as well as some I2C or similar serial communication protocol devices. More will follow as soon as the basic code is stable.


# Download and Install
## Requirements
* Hardware
  * Host computer
    * PC running Linux (maybe others)
    * or Raspberry running Linux (Ubuntu Jessie works)
    * Python >= 3.6 (format strings are used)
  * Target
    * ESP6288 
    * more to come

* Software packages
  * Micropython 
  * Mosquitto (and paho-mqtt)
  * ampy (from Adafruit)
  * esptool.py
  * (esp-open-sdk -- optional, needed to build custom runtimes, no support yet)

## Clone from GitHub

*Remark*: this worked for me, your mileage may vary. Please drop me a note if you have problems, I will try to help, and amend these instructions.

clone Espynoza from GitHub using this command:
```
git clone https://github.com/finalstate/Espynoza.git
```
This will create a directory called Espynoza containig the Espynoza.py cli tool, a basic configuration file and a number of sub-directories.

Moreover you will need to install the following packages to use Espynoza. Install them in some convenient place on your disk, not into the Espinoza directory.

MicroPython: the MicroPython language files, and its compiler. Install this using Github, and build the compiler yourself (the prebuild one provided for download is notoriously out of date, and your code will not work with it):
```
git clone https://github.com/micropython/micropython.git
cd micropython/bin
make
```
This will create the mpy-cross compiler executable. Open the file EspyConfig.py in the Espynoza root directory. There you will find the following line:
```
C_MpyCross = './bin/mpy-cross'
```
You may either change this to point to your brand-new compiler, or create the bin sub-directory and create a symbolic link to the compiler in this directory.


esptool: This tool is used to flash the target flash memory, and to upload the MicroPython firmware
```
sudo pip3 install esptool
```

ampy: This library is used to initially upload Python files to the target board. Install like this:
```
sudo pip3 install adafruit-ampy
```

Mosquitto: the MQTT broker used as a communication hub for Espynoza (and potentially many more sub-systems for your IoT installation)
If you use Debian or Ubuntu, the following should work:

```
sudo su
apt-get update
apt-get upgrade
apt-get install mosquitto mosquitto-clients
```

Please refer to the mosquitto documentation for configuration. the out-of-the-box config should be OK if you are happy without security settings...

paho-mqtt: a Python library for using MQTT. Again, we install using pip:

```
sudo pip3 install paho-mqtt
```

## Install with PIP

ToBeDone

# Tutorial
Here is a simple tutorial to get you started with Espynoza. First, we will set up some basic hardware, and then install the software on it to get a feeling for how Espinoza works and what it can do for us.

## Hardware setup
You need to get hold of an ESP6288 development board. Any board that has a USB port for uploading should work. We will, for the purpose of this tutorial, connect an LED to Port xxx to play with output lines, and a simple wire to Port yyy to try out input lines. Please note that we will use the Dnn numbering scheme as printed on (most?) boards when dealing with hardware, but will use the pin numbers as used in the official ESP documentation when writing software.

## Software configuration
## Running it
## Troubleshooting

# Architecture overview
## File organisation

# Reference

# Contributing

# Known issues
- out of order file chunk transfers
- dir name ESP is sub-optimal

# Upcoming

* pip3 installer
* custom firmware building support
* cli commands: rename board, move target to another broker 

# Remark:
**Info will be completed a.s.a.p., but if you happen to stumble on this project, feel free to use.**


Please be patient, doc. will be worked on before first public announcement

# Introduction
Espynoza is a framework for writing, configuring and managing applications on ESP8266 microcontroler boards.

Espynoza supports remote uploading of files/sources via USB cable, or via Wifi/MQTT once the basic software is installed. Multiple MQTT servers may be configured as well as distinct Wifi Hotspots. 

All user actions are made through a command-line interface, *Espynoza.py* (use --help for details). Configuration is made via Python files (basically variable assignments). Configuration files exist on the global level, as well as for the individual target devices.

The framework, running on the target device, handles initial connection to the Wifi network, and then establishes a connection with the specified MQTT broker. The host server may then send commands to the target device, using standard Python syntax, and will receive data produced on the target. The frameworks main loop calls (user-definable) handlers to perform actions such as setting outputs and reading sensor data. A wachdog will reboot the target if the board hangs.

Right now, some simple sample handlers are provided with Espynoza, more will follow soon. The aim is to create a library that will allow the user to build a system by writing a configuration file for simple cases, but that may be extended by writing small code fragments in Python for more special cases.

Special care has been been taken to use as little memory as possible on the target devices. Python files may be compiled on the host system before being uploaded to avoid out of memory conditions during system startup. Only the files needed for the targets configuration are loaded into RAM.

(BTW, in case you wonder why some things are designed the way they are, I plan to write a web/database-based application to make using Espynoza easier. But first things first...) 

## Version
Current version is *0.1*, the initial commit.
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
  * MicroPython 
  * Mosquitto (and paho-mqtt)
  * ampy (from Adafruit)
  * esptool.py
  * (esp-open-sdk -- optional, needed to build custom runtimes, no support yet)

## Clone from GitHub

*Remark*: the following instructions worked for me, your mileage may vary. Please drop me a note if you have problems, I will try to help, and amend these instructions.

**Espinoza**: clone Espynoza from GitHub using this command:
```
git clone https://github.com/finalstate/Espynoza.git
```
This will create a directory called Espynoza containig the Espynoza.py cli tool, a basic configuration file and a number of sub-directories.

Moreover you will need to install the following packages to use Espynoza. Install them in some convenient place on your disk, not into the Espinoza directory.

**MicroPython**: the MicroPython language files, and its compiler. Install this using Github, and build the compiler yourself (the prebuild one provided for download is notoriously out of date, and your code will not work with it):
```
git clone https://github.com/micropython/micropython.git
cd micropython/mpy-cross
make
```
This will create the mpy-cross compiler executable. Open the file EspyConfig.py in the Espynoza root directory. There you will find the following line:
```
C_MpyCross = './bin/mpy-cross'
```
You may either change this to point to your brand-new compiler, or create the bin sub-directory and create a symbolic link to the compiler in this directory (or use your own strategy, Espynoza is designed to be flexible).


**esptool**: This tool is used to flash the target flash memory, and to upload the MicroPython firmware
```
sudo pip3 install esptool
```

**ampy**: This library is used to initially upload Python files to the target board. Install like this:
```
sudo pip3 install adafruit-ampy
```

**Mosquitto**: the MQTT broker used as a communication hub for Espynoza (and potentially many more sub-systems of your IoT installation.)

If you use Debian or Ubuntu, the following should work:

```
sudo su
apt-get update
apt-get upgrade
apt-get install mosquitto mosquitto-clients
```

Please refer to the mosquitto documentation for configuration and usage. The out-of-the-box config should be OK if you are happy without security settings...

**paho-mqtt**: a Python library for using MQTT. Again, we install using pip:

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
Lets try to keep this simple for now. EspyConfig.py should be OK for this tutorial if you don have done anything special during installation. Let go into the *etc/* sub-directory. There, we find a file called *DemoDeviceList.py*. (We may use it as is, or we may make a copy of it that we call *DeviceList.py*, The later will be used if it exists. Do this if you do not want to run into problems when pulling the newest Espinoza library).

Open this file in your prefered text editor. It contains the configuration of your IoT installation as a whole. Later on, we will see how an individual target device is configured. We will need to make some changes in this file, specifically the Wifi and MQTT settings, and the basic settings of our target devices.

So, lets start with WiFi setup. In this tutorial, we will suppose that you have a single Wifi router. Uncomment the following line (leave the first one as is, it doesn't bother us right now), and change the name of the Hotspot and the Password to your settings:
```python
C_WifiPasswords    =    { 
                          ''         : '**PWD**',
                         
#                         'HotSpot1' : '**PWD**',
                        }
```

If your MQTT broker is configured to use a login and password, comment he first line, and uncomment the second one. Change the IP address you see to the one used by your MQTT broker. Change login and password if appropriate.
```python
C_MQTTCredentials  =    { 
                          '192.168.1.99' : (None,   None     ),
#                         '192.168.1.98' : ('esp', '*******' ),
                        }
```

And finally, we need to add our target to the device descriptor. Copy one of the linesn and modify it like this:
```python
C_DeviceDescriptor =    { 
                         # Target     : (Config,      AP, IP Address,      Broker,          Description                ),
                           'Tutorial' : ('Tutorial',  '', '192.168.1.42',   '192.168.1.99', 'Tutorial board'           ),
                                                       
                           'SimpleIO' : ('SimpleIO',  '', '192.168.1.100', '192.168.1.215', 'Blink and rotary encoder' ),
                        ...
```
Change the dictionaries key to the name you want to give to your board. The associated parameter list begins with the name of the target configuration that we will define below. Here, we give it the same name as the target, but if you have several targets that use the same configuration (such as temperature sensors in different rooms), you may use different target board names, and reuse the same configuration file. Next comes the SSID name of the Access Point you want the device to connect to. Then, find and enter an address in your LAN that is not used, here, I used 192.168.1.42. The second quad.dot.address is the address of the broker this particular board uses, change it to the one you used above. Finally, there is a string describing the board, change it to whatever you like, it is currently only used for documentation purposes.

Btw, if you leave the AP empty, the target will scan the Ether for access points and try to use those found, one by one, starting with the strongest, until a connection works. Of course, you will then need to set the password for the '' Hotspot in the *<Demo>DeviceList.py* file, and booting the board will take longer. Also, more RAM will be used. But hey, it will work, and having multiple access points for redundancy, or better coverage, has also its advantages. (Btw, right now, all access points must have the same password. Stay tuned...)

Save the file, it should be OK for now. But we are not done yet with the configuration...

Make a copy of file Newbie.py, name it Tutorial.py. That's to say, use the config name you defined in the <Demo>DeviceList.py file. Open this file in your editor, and change the following items:
**C_DNS, C_Gateway, C_Netmask**: change if necessary so it fits your network

**C_Hotspot**: enter the name of your Hotspot. 

**C_Handlers**: we will configure our IO here. Insert the following lines:
```python
C_Handlers       = {
                     'DigitalOut': { 'Period' : 250,   'Params' : (('Led',    True ), ) }
                     'DigitalIn' : { 'Period' :    1,  'Params' : (('Wire',    500 ), ) },
                   }
```
Now, what does this mean. Lets see item by item. 

*DigitalOut* and *DigitalIn* are handler names. Think of them as drivers for your input and output devices. If you are curious, see the files *DigitalOut.py* and *DigitalIn.py* in the *usr/* directory.

The 'Period' parameter indicates how often the output handler should be called. It is the number of milliseconds that the target should wait between two calls to the handlers 'periodic' method. The *DigitalOut* handler will blink the Led we connected every 500 ms (250 ms between individual togglings), and the *DigitalIn* pin will be read evers millisecond.

Next, we have the Parameters. These are different for all handlers, see the source file of the given Handler for a description. For *DigitalOut*, they are: The pin name to use, and if the Led should blink. We will see later what else than blinking we can do with this handler. *DigitalIn*s first parameter is also the pin name. The second parameter is used for debouncing, any changes happening at intervals (in milliseconds) shorter than this will be ignored.

**C_Pins**:
Finally, we need to define our pins:
```
# (Pin, direction: 0=IN | 1=OUT, Pull: 1=PULL_UP | None=None)
C_Pins          = {
                    'Led'  : (0,  1),  
                    'Wire' : (1,  0, None),
                  }
```

This dictionaries keys are the names of the Pins, as we used them above. The first parameter is the pin number. Here, we use the Espressif numbering, not the Dx stuff from the Arduino world. The second parameter defines if the pin is used as an Input or as an Output. Finally, the 'Wire' input pin has a third value which indicates whether it is configured as a PULL_UP input or not.

And this concludes the configuration of our target. Next, we need to get it on our target, and then we may finally play with it.

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
(help welcome :-) )

* pip3 installer
* custom firmware building support
* https support for mqtt connections
* cli commands: rename board, move target to another broker

* ESP32 support (if and when MicroPython supports the stuff needed)

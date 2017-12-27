# Remark:
** Info will be completed a.s.a.p., if you happen to stumble on this project, feel free to use. **

Please be patient, doc. will be worked on before first public announcement

# Introduction

Espynoza

iot framework -> handler based, mqtt-based

Watchdog
build (multiple) runtime
easy configuration
highly configurable
low footprint
rapid development cycle


## Version
Current version is 0.1, the initial commit.
This version should be considered alpha quality, even though the code should work if Espynoza and all needed libraries and tools are installed correctly.
Right now, the number of available hardware drivers is limited to simple digital and analog IO, as well as some I2C or similar serial communication protocol devices. More will follow as soon as the basic code is stable.


# Download and Install
## Requirements
- Hardware
-- Host computer
--- PC running : Linux (maybe others)
--- Raspberry running Linux (Ubuntu Jessie works)
-- target
--- ESP6288 
--- more to come

- Software packages
-- Micropython 
-- Mosquitto
-- ampy
-- esptools
-- (esp-open-sdk -- optional, needed to build custom runtimes)

## Clone from GitHub

## Install with PIP

# Tutorial
Here is a simple tutorial to get you started with Espynoza. First, we will set up some basic hardware, and then install the software on it to get a feeling for how Espinoza works and what it can do for us.

## Hardware setup
You need to get hold of an ESP6288 development board. Any board that has a USB port for uploading will work. We will, for the purpose of this tutorial, connect an LED to Port xxx to play with output lines, and a simple wire to Port yyy to try out input lines. Please note that we will use the Dnn numbering scheme as printed on (most?) boards when dealing with hardware, but will use the pin numbers as used in the official ESP documentation when writing software.

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

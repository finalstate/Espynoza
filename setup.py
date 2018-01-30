import codecs
import os    
import setuptools

try:
    import pypandoc
    l_LongDescription = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    l_LongDescription = open('README.md').read()


setuptools.setup(
    name             = 'Espynoza',
    version          = '0.2.3', 
                     
    description      = 'Runtime and upload utilities for MicroPython/ESP8266 boards', 
    long_description = l_LongDescription,
    url              = 'https://github.com/finalstate/Espynoza',
    author           = 'René Schmit',
    author_email     = 'rene.schmit@plaakert.lu', 

    license          = 'MIT',
    classifiers      = [ 
                        'Development Status :: 3 - Alpha',

                        'Intended Audience :: Developers',
                        'Topic :: Software Development :: Build Tools',

                        'License :: OSI Approved :: MIT License',

                        'Programming Language :: Python :: 3',
                        'Programming Language :: Python :: 3.6',
                       ],

    keywords         = 'IoT esp8266 MicroPython runtime uploader MQTT OverTheAir',

    packages         = setuptools.find_packages(exclude=['bin',]),
    package_data     = {
                        'ESP'      : [ 'DeviceList.py.sample',],
                        'ESP.conf' : [ 'Config.py.sample',    ],
                        'Espynoza' : [ 'EspyConfig.py.sample',],
                       },

    install_requires = ['esptool>=2.2','adafruit-ampy>=1.0.3', 'paho-mqtt>=1.3.1'],

    python_requires  = '>=3.6', # because f-strings are used...

    entry_points     = { 'console_scripts': ['espynoza   = Espynoza.Espynoza:main',
                                             'espylisten = Espynoza.EspyListen:main',
                                            ],},
)

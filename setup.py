"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import setuptools
import codecs
import os    

l_Here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with codecs.open(os.path.join(l_Here, 'README.md'), encoding='utf-8') as l_File:
    l_LongDescription = l_File.read()

setuptools.setup(
    name             = 'Espynoza',
    version          = '0.1', 
                     
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

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages         = ['Espynoza',], # setuptools.find_packages(exclude=['bin']),

    install_requires = ['esptool>=2.2','adafruit-ampy>=1.0.3', 'paho-mqtt>=1.3.1'],
    
    # f-strings are used...
    python_requires  = '>=3.6',

    # If there are data files included in your packages that need to be
    # installed, specify them here.
#    package_data     = {  
#                         'ESP': [
#                                       'ESP/*.py',
#                                       'etc/*.py', 
#                                       'usr/*.py', 
#                                       'var/*.py',
#                                     ],
#                       },
#    data_files       = [
#                        ('',   [
#                                'ESP/*.py',
#                                'etc/*.py', 
#                                'usr/*.py', 
#                                'var/*.py',
#                               ],
#                        ),
#                       ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points     = { 'console_scripts': ['Espynoza=Espynoza:main',],},
)

C_WifiPasswords    =    { 
                          ''           : ('**PWD**' ),
                         
#                          'HotSpot1'  : ('**PWD**' ),
#                          'HotSpot2'  : ('**PWD**' ),
                        }

C_MQTTCredentials  =    { 
                          '192.168.1.99'  : (None,   None     ),
#                          '192.168.1.98' : ('esp', '*******' ),
                        }

C_DeviceDescriptor =    { 
                           'SimpleIO'  : ('192.168.1.100',  '192.168.1.99', 'Digital I/O and single-wire temp'      ), #
                           'SimpleIO2' : ('192.168.1.101',  '192.168.1.99', 'Blink, temperature and rotary encoder' ), #

                           'Dimmer'    : ('192.168.1.102',  '192.168.1.99', 'Dimmer with PWM'                       ), #
                           'Neo'       : ('192.168.1.103',  '192.168.1.99', 'NeoPixel'                              ), #
                           'Baro'      : ('192.168.1.104',  '192.168.1.99', 'Barometer, radar and temp'             ), #
                        }

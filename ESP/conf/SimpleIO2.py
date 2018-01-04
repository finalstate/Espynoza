C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.001
C_ChunkSize      = 256*8

# MQTT server     
C_BrokerQoS      = 1
C_BrokerSubPat   = 'esp/{ClientId}/cmd'
C_BrokerPubPat   = 'sensors/esp/{ClientId}/{Name}'

# Log file (disable in prod. so not to overflow memory)
C_LogFile        = ''
#C_LogFile        = '/Log.txt'
             
C_Handlers       = {
                     'AnalogIn'   : { 'Period' :   50,  'Params' : (('Analog',       20,      ), ) },
                     'DigitalIn'  : { 'Period' :    1,  'Params' : (('Touch',       500,      ), ) },
                     'Interrupt'  : { 'Period' :    1,  'Params' : (('Button1',               ),
                                                                    ('Button2',               ),
                                                                   ) 
                                    },
                     'DS18B20'    : { 'Period' : 1000,  'Params' : (('Temperature', 0.067,    ), ) },
                                  
                     'DigitalOut' : { 'Period' : 250,   'Params' : (('Red',  False),
                                                                    ('Blue',  True)
                                                                   )
                                    },
                     'PwmOut'     : { 'Period' : None,  'Params' : (('Green',                 ), ) },
                    }

# Pin  : ESP pin id, 
# Mode : 0=IN | 1=OUT | 2=OPEN_DRAIN, 
# Value: if  IN: 1=PULL_UP | None=None)
#        if OUT: 0=OFF | 1=ON | None=leave (default state)

C_Pins            = {
                      'OneWire'   : (0,  1, None),  
                                  
                      'Button1'   : (1,  0, None),
                      'Button2'   : (3,  0, None),
                                         
                      'SDA'       : (4,  1, None),  
                      'SCL'       : (5,  1, None),  
                                         
                      'Dimmer'    : (12, 1, None),  
                                  
                      'Red'       : (14, 1, None),  
                      'Green'     : (12, 1, None),  
                      'Blue'      : (13, 1, None),  
                                    
                      'Touch'     : (15, 0, None),  
                    }
        

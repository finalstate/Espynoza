C_IP             = ''
C_DNS            = '192.168.1.1' 
C_Gateway        = '192.168.1.1'
C_NetMask        = '255.255.255.0'
                 
C_Hotspot        = 'NSA'
C_ClientId       = 'SimpleIO'
C_ChunkSize      = 256*8

C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.001

# MQTT server     
C_BrokerIP       = ''
C_BrokerPort     = 0
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

# (Pin, direction: 0=In, 1=Out)
C_Pins            = {
                      'OneWire'   : (0,  1),  
                                  
                      'Button1'   : (1,  0, None),
                      'Button2'   : (3,  0, None),
                                         
                      'SDA'       : (4,  1),  
                      'SCL'       : (5,  1),  
                                         
                      'Dimmer'    : (12, 1),  
                                  
                      'Red'       : (14, 1),  
                      'Green'     : (12, 1),  
                      'Blue'      : (13, 1),  
                                    
                      'Touch'     : (15, 0, None),  
                    }
        

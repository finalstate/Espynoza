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
                     'DS18B20'   : { 'Period' : 1000,  'Params' : (('Temperature', 0.067, ), ) },
                     'DigitalIn' : { 'Period' :  100,  'Params' : (('RadarIn',      100   ), ) },
                     'Pressure'  : { 'Period' : 1000,  'Params' : (('Temperature', 0.25), 
                                                                   ('Pressure',    0.25), 
                                                                  )
                                   },
                   }

# (Pin, direction: 0=IN | 1=OUT, Pull: 1=PULL_UP | None=None)
C_Pins          = {
                    'OneWire' : ( 0,  1), 
                    
                    'SDA'     : ( 4,  1),  
                    'SCL'     : ( 5,  1),  

                    'RadarIn' : (14,  0, None),  
                  }
        

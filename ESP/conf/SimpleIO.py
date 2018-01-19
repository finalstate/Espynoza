C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.001
C_ChunkSize      = 256*8

# MQTT server     
C_BrokerQoS      = 0
C_BrokerSubPat   = 'esp/{ClientId}/cmd'
C_BrokerPubPat   = 'sensors/esp/{ClientId}/{Name}'

# Log file (disable in prod. so not to overflow memory)
C_LogFile        = ''
#C_LogFile        = '/Log.txt'
             
C_Handlers       = {
                     'DigitalIn' : { 'Period' :  2,   'Params'  : (('Switch',  1),
                                                                  ),
                                   },
                     'DigitalOut': { 'Period' : 100,   'Params' : (('Led',  True),
                                                                  ),
                                   },
                   }

# Pin  : ESP pin id, 
# Mode : 0=IN | 1=OUT | 2=OPEN_DRAIN, 
# Value: if  IN: 1=PULL_UP | None=None)
#        if OUT: 0=OFF | 1=ON | None=leave (default state)

C_Pins           = {
                      'Switch'   : ( 4, 0, 1),   
                      
                      'Led'      : (14, 1, 1),  
                   }
        

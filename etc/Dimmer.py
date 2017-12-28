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
                     'PwmOut'    : { 'Period' : None,  'Params' : (('Led',                 ), ) },
                   }

# (Pin, direction: 0=IN | 1=OUT, Pull: 1=PULL_UP | None=None)
C_Pins           = {
                     'Led'   : (4, 1),  
                  }
        

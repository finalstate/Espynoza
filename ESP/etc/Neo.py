C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.0001
C_ChunkSize      = 256*16

# MQTT server     
C_BrokerQoS      = 1
C_BrokerSubPat   = 'esp/{ClientId}/cmd'
C_BrokerPubPat   = 'sensors/esp/{ClientId}/{Name}'

# Log file (disable in prod. so not to overflow memory)
C_LogFile        = ''
#C_LogFile        = '/Log.txt'
             
C_Handlers       = {
#                     'NeoGen'    : { 'Period' : 1,  'Params' : (('Neo', 300, 'NeoFile', 'Run.data',      ), ) },
                     'NeoGen'    : { 'Period' : 1,  'Params' : (('Neo', 300, 'NeoRun', 3      ), ) },
                   }

# Pin  : ESP pin id, 
# Mode : 0=IN | 1=OUT | 2=OPEN_DRAIN, 
# Value: if  IN: 1=PULL_UP | None=None)
#        if OUT: 0=OFF | 1=ON | None=leave (default state)

C_Pins           = {
                     'Neo'   : (0, 1, None),  
                   }
        

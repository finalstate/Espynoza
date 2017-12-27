C_IP             = ''
C_DNS            = '192.168.1.1' 
C_Gateway        = '192.168.1.1'
C_NetMask        = '255.255.255.0'
                 
C_Hotspot        = 'NSA'
                 
C_ClientId       = 'Newbie'
C_ChunkSize      = 256*16

C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.0001

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
#                     'NeoGen'    : { 'Period' : 1,  'Params' : (('Neo', 300, 'NeoFile', 'Run.data',      ), ) },
                     'NeoGen'    : { 'Period' : 1,  'Params' : (('Neo', 300, 'NeoRun', 3      ), ) },
                   }

# (Pin, direction: 0=In, 1=Out)
C_Pins           = {
                     'Neo'   : (0, 1),  
                   }
        

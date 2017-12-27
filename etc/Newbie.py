C_IP             = ''
C_DNS            = '192.168.1.1' 
C_Gateway        = '192.168.1.1'
C_NetMask        = '255.255.255.0'
                 
C_Hotspot        = ''
                 
C_ClientId       = 'Newbie'
C_ChunkSize      = 256*8

C_ConnectTO      = 15
C_WatchdogTO     = 60
                 
C_LoopDelay      = 0.001

# MQTT server     
C_BrokerIP       = ''
C_BrokerPort     = 0
C_BrokerQoS      = 0
C_BrokerSubPat   = 'esp/{ClientId}/cmd'
C_BrokerPubPat   = 'sensors/esp/{ClientId}/{Name}'

# Log file (disable in prod. so not to overflow memory)
C_LogFile        = ''
#C_LogFile        = '/Log.txt'
             
C_Handlers       = {
                   }

# (Pin, direction: 0=In, 1=Out)
C_Pins           = {
                   }
        

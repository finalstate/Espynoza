#! /usr/local/bin/python3.6
# -*- coding: utf-8 -*-
####################################################################################################

import argparse
import datetime
import os
import shutil
import subprocess
import sys
import time

import paho.mqtt.client as mqtt

import ampy.pyboard
import ampy.files

####################################################################################################
####################################################################################################

C_ChunkSize     = 256*4

####################################################################################################
####################################################################################################

def getRuntimeFiles():
    return [
#               'ESP/main.py',
            
                os.path.join(EspyConfig.C_TmpDirectory,     'Config.py'     ),
                                                                                
                os.path.join(EspyConfig.C_RuntimeDirectory, 'Runtime.py'    ),
                os.path.join(EspyConfig.C_RuntimeDirectory, 'mqtt.py'       ),
                
                os.path.join(EspyConfig.C_RuntimeDirectory, 'LogToFile.py'  ),
                os.path.join(EspyConfig.C_RuntimeDirectory, 'LogNone.py'    ),
                
                os.path.join(EspyConfig.C_RuntimeDirectory, 'WifiHotspot.py'),
                os.path.join(EspyConfig.C_RuntimeDirectory, 'WifiScan.py'   ),
                
                os.path.join(EspyConfig.C_RuntimeDirectory, 'BaseHandler.py'),
                
#                os.path.join(EspyConfig.C_RuntimeDirectory, 'bme280.py'     ),
           ]

####################################################################################################

def setupLocalProjectDir():
    l_NewDirectoryName = g_Arguments.setup
    if os.path.exists(l_NewDirectoryName):
        sys.exit(f'Directory already exists.')
    
    l_EspinozaInstallDir = os.path.realpath(__file__).replace('Espynoza/Espynoza.py', '') # hack, change this
    
    if g_Arguments.verbose:
        print(f'Setting up local directory "{l_NewDirectoryName}", copying from install directory "{l_EspinozaInstallDir}"')
    
    os.mkdir(l_NewDirectoryName)
    os.chdir(l_NewDirectoryName)
    
    shutil.copytree(os.path.join(l_EspinozaInstallDir, 'ESP'), 'ESP')
    
    shutil.copyfile('ESP/DeviceList.py.sample',                                         'DeviceList.py')    
    shutil.copyfile(os.path.join(l_EspinozaInstallDir,'Espynoza/EspyConfig.py.sample'), 'EspyConfig.py')    
    
####################################################################################################
####################################################################################################

class USB:
    def __init__(self, p_Arguments):
        if p_Arguments.usb is None:
            self.f_PyBoard  = None
            self.f_EspFiles = None
            self.f_Port     = None
        else:
            if p_Arguments.usb == '':
                self.f_Port = self.findUSB()
            else:
                self.f_Port = p_Arguments.usb
                
            if p_Arguments.verbose:
                print (f'USB interface: {self.f_Port}')
                
            self.f_PyBoard  = ampy.pyboard.Pyboard(self.f_Port   )
            self.f_EspFiles = ampy.files.Files    (self.f_PyBoard)
       
    def close(self):
        if self.f_PyBoard:
            self.f_PyBoard.close()
    
    def ls(self):
        return self.f_EspFiles.ls()
    
    def put(self, l_Filename, l_Data):
        return self.f_EspFiles.put(l_Filename, l_Data)
    
    def rm(self, l_Filename):
        return self.f_EspFiles.rm(l_Filename)
    
    def reset(self):
        # do this with Esptool.ps, as ampy does not expose reset function
        return subprocess.run((EspyConfig.C_Esptool, '--port', self.f_Port, 'run'), stdout=subprocess.PIPE, universal_newlines=True)

    def findUSB(self):
        for l_File in os.listdir('/dev'):
            if 'USB' in l_File:
                return(f'/dev/{l_File}')
        
####################################################################################################

class MQTT:
    
    ''' *All* payload data is in bytes.
    '''
    def __init__(self, p_TargetName, p_Broker, p_UserName=None, p_Password=None):
        self.resetState()
        self.f_TargetName = p_TargetName
        
        self.f_Client     = mqtt.Client()
        
        if p_UserName is not None:
            self.f_Client.username_pw_set(p_UserName, p_Password)
        
        self.f_Client.connect(p_Broker, 1883,60) #
        
        self.f_Client.on_message = self.getResponse
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/#',  qos=0)
#        print('Subscribe result: ', l_Result)
        self.f_Client.loop_start()
        
    def resetState(self):
        self.f_Hello   = False
        self.f_Bye     = False
        self.f_Done    = False
        self.f_Payload = None
        self.f_Data    = bytearray()
        self.f_Status  = True
    
    def __str__(self):
        return  f'''
                     {self.f_Done}     
                     {self.f_Payload}
                     {self.f_Data}     
                     {self.f_Status}       
                 '''
                 
    def getData(self):
        return self.f_Data
    
    def getResponse(self, p_Client, p_UserData, p_Message):
        '''
            MQTT subscribe callback.
            Sets the global state:
                f_Data      : add the data returned by the target to a bytearray
                f_Payload   : the payload of this message
                f_Status    : True if no error resturned by target
               
            
            The global state should not be read by external functions, the return value of sendCommand should be used instead.
            Cumulated data during file rerievel is accessible through getData().
            Text printed on remote host is printed to console, and is not part of either data or payload.
        '''
        
        self.f_Status  = p_Message.payload[0] == ord('T')
        self.f_Payload = p_Message.payload[1:]

        if   p_Message.topic.endswith('print'):
            print(self.f_Payload.decode(), end='', flush=True)
                
        elif p_Message.topic.endswith('data'):
            if self.f_Payload != b'':
                self.f_Data += self.f_Payload
                print('.', end='', flush=True)
            else:
                print ('', flush=True)
                
        elif p_Message.topic.endswith('Hello'):
            self.f_Hello = True
            
        elif p_Message.topic.endswith('Bye'):
            self.f_Bye   = True
            
        elif p_Message.topic.endswith('res'):
            self.f_Done  = True
        else:
            pass
            # print (f'Unknown topic: {p_Message.topic}')
            
    def sendCommand(self, p_Command, p_Timeout=15):
        '''
            p_Command : convert to bytes
            p_Timeout : timeout, not waiting for response if 0
        ''' 
        l_Command = p_Command
        if isinstance(l_Command, str):
            l_Command = l_Command.encode()
        
        self.resetState()
        self.f_Client.publish(f'esp/{self.f_TargetName}/cmd', l_Command, qos=0)
        
#        print ('Timeout', p_Timeout)
        
        if p_Timeout <= 0:
            return (True, '')
        
        while (not self.f_Done):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Timeout')
            
#        print ('Payload', self.f_Payload)
        return (self.f_Status, self.f_Payload)
    
    def waitHello(self, p_Timeout=15):
        while (not self.f_Hello):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Hello timeout')
        return (self.f_Status, self.f_Payload)
    
    def waitBye(self, p_Timeout=15):
        while (not self.f_Bye):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Bye timeout')
        return (self.f_Status, self.f_Payload)
        
    def close(self):
        self.f_Client.disconnect()
        
####################################################################################################
####################################################################################################  

def getHandlerList(p_ConfigName):
    l_ConfigFilename = os.path.join(EspyConfig.C_ConfigDirectory, f'{p_ConfigName}.py')
    with open(l_ConfigFilename, 'r') as l_Config:
        l_ConfigFileContent = l_Config.read()
        exec(l_ConfigFileContent)
        
    return locals()['C_Handlers'].keys()
                      
####################################################################################################

def prepareConfig(p_DeviceName,):   
    l_Target = DeviceList.C_DeviceDescriptor[p_DeviceName]
    l_ConfigFilename = os.path.join(EspyConfig.C_ConfigDirectory, f'{p_DeviceName}.py')
    with open(l_ConfigFilename, 'r') as l_ConfigTemplate:
        l_ConfigFileContent = l_ConfigTemplate.read()

    l_Configs = [l_ConfigFileContent]
    l_Configs.append(f"""C_ClientId = '{p_DeviceName}'""")
    l_Configs.append(f"""C_Hotspot  = '{l_Target[1]}'""")
    l_Configs.append(f"""C_IP       = '{l_Target[2]}'""")
    l_Configs.append(f"""C_DNS      = '{DeviceList.C_Network["DNS"    ]}'""")
    l_Configs.append(f"""C_Gateway  = '{DeviceList.C_Network["Gateway"]}'""")
    l_Configs.append(f"""C_Netmask  = '{DeviceList.C_Network["Netmask"]}'""")
    
    l_Credentials = DeviceList.C_MQTTCredentials[l_Target[3]]
    l_Configs.append(f"""C_BrokerIP       = '{l_Target[3]}'""")
    l_Configs.append(f"""C_BrokerUser     = '{l_Credentials[0]}'""")
    l_Configs.append(f"""C_BrokerPassword = '{l_Credentials[1]}'""")
    
    # now, this is UGLY
    for l_Line in l_ConfigFileContent:
        if 'C_Hotspot' in l_Line:
            break
        
    l_HotSpot  = l_Line.replace('C_Hotspot','').replace('=','').strip().strip("'")
    l_Password = DeviceList.C_WifiPasswords[l_HotSpot]

    l_Configs.append(f"""C_Password = '{l_Password}'""")

    
    with open(os.path.join(EspyConfig.C_TmpDirectory, 'Config.py'), 'w') as l_TempConfig:
        l_TempConfig.write('\n'.join(l_Configs))
        
####################################################################################################

def resetTarget():
    if g_Arguments.verbose:
        print ('\nReboot  : please wait...\n', end='')
        
    if g_USB:
        g_USB.reset()
        
    else:
        g_MQTT.sendCommand('g_MQTT.stopESP()', p_Timeout=0)
        
        l_Answer = g_MQTT.waitBye  (p_Timeout=5)
        if g_Arguments.verbose:
            print (f'{l_Answer[0]} : Bye   -> {l_Answer[1].decode()}')
        
        l_Answer = g_MQTT.waitHello(p_Timeout=15)
        if g_Arguments.verbose:
            print (f'{l_Answer[0]} : Hello -> {l_Answer[1].decode()}')            
                                
####################################################################################################
        
def sendChunckedFile(p_LocalFilename, p_RemoteFilename):            
    l_RemoteTempFilename = p_RemoteFilename + '.tmp'
    
    with open(p_LocalFilename, 'rb') as l_LocalFile:
        while True:
            l_Chunk   = l_LocalFile.read(C_ChunkSize)
            l_Length  = len(l_Chunk)
            l_Command = f'''appendFile('{l_RemoteTempFilename}',{l_Chunk})'''
            l_Result  = g_MQTT.sendCommand(l_Command)
            
            if l_Result[1] == b'OK':
                print ('.', end='', flush=True)
            else:
                print('Send file error returned:', l_Result[1].decode('utf-8'))
                return l_Result
               
            if l_Length != C_ChunkSize:
                break
            
    g_MQTT.sendCommand(f'''os.rename('{l_RemoteTempFilename}', '{p_RemoteFilename}')''')
    return l_Result

####################################################################################################

def readDirectory(p_Directory):
    if g_USB:
        l_Files   = g_USB.ls()
    else:
        l_Command = f'''os.listdir('{p_Directory}')'''
        l_Result  = g_MQTT.sendCommand(l_Command)
        l_Files   = eval(l_Result[1])
        
    l_Files.sort()
    
    return l_Files

####################################################################################################
        
def writeFile(p_LocalFilename, p_RemoteFilename):
    if g_USB is None:
        return sendChunckedFile(p_LocalFilename, p_RemoteFilename)
    else:
        with open(p_LocalFilename, 'rb') as l_InFile:
            l_Data = l_InFile.read()
            g_USB.put(p_RemoteFilename, l_Data)
        return (0, b'OK')
    
####################################################################################################
        
def removeFile(p_Filename):
    l_RemoteFilelist = readDirectory('/')

    if p_Filename in l_RemoteFilelist:
        if g_USB is None:
            g_MQTT.sendCommand(f'''os.remove('{p_Filename}')''')
        else:
            g_USB.rm(p_Filename)
        
##################################################

def sendFile(p_LocalFilename, p_RemoteFilename, p_Compile=True):
    l_IsPythonfile = p_LocalFilename.endswith('.py')
    l_Answer       = None
    
    if l_IsPythonfile:
        
        if p_Compile:
        
            l_Completed      = subprocess.run((EspyConfig.C_MpyCross , p_LocalFilename), stdout=subprocess.PIPE, universal_newlines=True)
            if l_Completed.returncode != 0:
                print ('Error during compile: ',l_Completed)
                return False
            
            l_CompiledFilename = p_LocalFilename.replace ('.py', '.mpy')
            l_RemoteFilename   = p_RemoteFilename.replace('.py', '.mpy')
            l_Answer = writeFile(l_CompiledFilename, l_RemoteFilename)
            removeFile(p_RemoteFilename.replace('.mpy', '.py'))
                        
        else:
            l_Answer = writeFile(p_LocalFilename, p_RemoteFilename)
            if p_RemoteFilename.endswith('py'):
                removeFile(p_RemoteFilename.replace('.py', '.mpy'))
            
    else:
        l_Answer = writeFile(p_LocalFilename, p_RemoteFilename)        
        
    return l_Answer

####################################################################################################
        
def setRTC():
    l_Now     = datetime.datetime.utcnow()
    l_Command = f'machine.RTC().datetime((({l_Now.year},{l_Now.month},{l_Now.day},0,{l_Now.hour},{l_Now.minute},{l_Now.second},0)))'
    return g_MQTT.sendCommand(l_Command)

####################################################################################################

def flashESP8266():
    if not g_USB:
        sys.exit('Only possible in USB mode')
        
    l_Port      = g_USB.f_Port
    l_Chip      = 'esp8266'
    l_Baud      = '115200'
    l_FlashMode = 'dio'
    l_FlashSize = 'detect'
    l_Address   = '0x0000'
    l_Binary    = '/home/rene/esp8266/esp8266-20171101-v1.9.3.bin'
    
#    esptool.py --port /dev/ttyUSB0 erase_flash
    if g_Arguments.verbose:
        print('Erasing chip flash memory : ', end='', flush=True)

    l_Completed      = subprocess.run((EspyConfig.C_Esptool, '--port', l_Port, 'erase_flash'), stdout=subprocess.PIPE, universal_newlines=True)
    if l_Completed.returncode != 0:
        sys.exit('Could not erase flash')
    
    if g_Arguments.verbose:
        print('Done')
        
#    esptool.py --chip esp8266 --baud 115200 --port /dev/ttyUSB0 write_flash --flash_mode dio --flash_size=detect 0 /home/rene/esp8266/esp8266-20171101-v1.9.3.bin
    if g_Arguments.verbose:
        print('Uploading binary image    : ', end='', flush=True)
        
    l_Completed      = subprocess.run(( EspyConfig.C_Esptool, 
                                        '--chip', l_Chip, 
                                        '--port', l_Port, 
                                        '--baud', l_Baud,
                                        'write_flash', 
                                        '--flash_mode', l_FlashMode,
                                        '--flash_size', l_FlashSize,
                                        l_Address, l_Binary
                                      ),
                                      stdout=subprocess.PIPE, universal_newlines=True
                                     )
    if l_Completed.returncode != 0:
        sys.exit('Could not erase flash')
        
    if g_Arguments.verbose:
        print('Resetting board, please wait')
        resetTarget()
        
    if g_Arguments.verbose:
        print('Done')
   
####################################################################################################

def main():
    global g_Arguments
    global g_USB
    global g_MQTT
    
    global EspyConfig
    global DeviceList
    
    l_ArgumentParser = argparse.ArgumentParser(description='Communicate with an ESP6288 board via MQTT')
    
    l_ArgumentParser.add_argument('-v', '--verbose',    required=False,  action='store_true',          help='Verbose user info')
    l_ArgumentParser.add_argument('-i', '--ignore',     required=False,  action='store_true',          help='ignore result sent by ESP'                                        )
                                                        
    l_ArgumentParser.add_argument('-t', '--target',     required=False,  action='store' )
    l_ArgumentParser.add_argument('-u', '--usb',        nargs='?',       action='store', const='',     help='USB port to use. Tries to auto-detect if none given'              )
    l_ArgumentParser.add_argument('-b', '--broker',     required=False,  action='store', default=None, help='Use non-default broker to access ESP. Useful when changing broker')
    l_ArgumentParser.add_argument('-l', '--localfile',  required=False,  action='store',               help='Name of the local file to write to ESP'                           )
    l_ArgumentParser.add_argument('-s', '--source',     required=False,  action='store_true',          help='Do not compile Python sources before transfering'                 )

    l_ArgumentParser.add_argument('-c', '--command',    required=False,  action='store',               help='Execute command on ESP, print result upon completion'             )

    l_ArgumentParser.add_argument('-d', '--dir',        nargs='?',       action='store', const='/',    help='List files in directory from ESP'                                 )
    l_ArgumentParser.add_argument('-g', '--getfile',    required=False,  action='store',               help='Retrieve file from ESP'                                           )

    l_ArgumentParser.add_argument('-w', '--writefile',  required=False,  action='store',               help='Write file to ESP. Localfile is name to be send, '
                                                                                                            'parameter is name on target'                                      )
    l_ArgumentParser.add_argument(      '--base',       required=False,  action='store_true',          help='Update basic runtime'                                             )
    l_ArgumentParser.add_argument(      '--configure',  required=False,  action='store_true',          help='Update configuration'                                             )
    l_ArgumentParser.add_argument(      '--handlers',   required=False,  action='store_true',          help='Update libraries using Config content'                            )
    l_ArgumentParser.add_argument('-r', '--reset',      required=False,  action='store_true',          help='Restart the ESP'                                                  )

    l_ArgumentParser.add_argument(      '--flash',      required=False,  action='store_true',          help='Initialize chip using Esptool. Only in USB mode'                  )
                                                        
    l_ArgumentParser.add_argument(      '--rtc',        required=False,  action='store_true',          help='Update Real Time Clock on ESP.'                                   )

    l_ArgumentParser.add_argument(      '--setup',      required=False,  action='store',               help='Create a local working directory.'                                )
    
    g_Arguments  = l_ArgumentParser.parse_args()    
        
    # Done 'manually' here, allowing for further changes, such as config file in user main directory
    sys.path.append('.')
    EspyConfig = __import__('EspyConfig')
    DeviceList = __import__(EspyConfig.C_DeviceList)
           
    if g_Arguments.setup:
        setupLocalProjectDir()
        sys.exit()
        
    g_USB = USB(g_Arguments)
    if not g_USB.f_PyBoard:
        g_USB = None 
        
    if g_Arguments.broker:
        l_Broker = g_Arguments.broker
    else:
        l_Broker = DeviceList.C_DeviceDescriptor[g_Arguments.target][3]
        
    if g_Arguments.verbose:
        print (f'Broker: {l_Broker}')

    
    g_MQTT = MQTT(g_Arguments.target, l_Broker, DeviceList.C_MQTTCredentials[l_Broker][0], DeviceList.C_MQTTCredentials[l_Broker][1])
###
    if g_Arguments.command:
        l_Command = g_Arguments.command
        l_Result  = g_MQTT.sendCommand(l_Command, 0 if g_Arguments.ignore else 15)
        
#        print ('Client result', l_Result)
        
        if  not g_Arguments.ignore:
            if  l_Result[0]:
                if len(l_Result[1]) != 0:
                    print('Result:', l_Result[1].decode())
            else:
                print('Error:\n\n', l_Result[1].decode())
###
    if g_Arguments.dir:
        l_Files = readDirectory(g_Arguments.dir)
        print()
        for l_File in l_Files:
            print(l_File)
        print()
###
    if g_Arguments.getfile:
        l_Result = g_MQTT.sendCommand(f'''getFile('{g_Arguments.getfile}')''' )
        
#        print(l_Result, g_MQTT)
        
        if l_Result[0]:
            l_ResultString = g_MQTT.f_Data
            if g_Arguments.localfile:
                with open(g_Arguments.localfile, 'wb') as l_OutFile:
                    l_OutFile.write(l_ResultString)
            else:
                try:
                    print (l_ResultString.decode('utf-8'), end='')
                except UnicodeDecodeError:
                    print (f'Received non-UTF-8 content of length {len(l_ResultString)}')
                
            if g_Arguments.verbose:
                print(f'File length: {len(l_ResultString)}')
    
        else:
            print (f'Error getting file. Message:\n\n{l_Result[1].decode()}')
###
    if g_Arguments.writefile:
        l_Result = sendFile(g_Arguments.localfile, g_Arguments.writefile, not g_Arguments.source)
        if g_Arguments.verbose and (l_Result[1] == b'OK'):
            print('\nOK')
###
    if g_Arguments.base:
        l_Compile = not g_Arguments.source
        prepareConfig(g_Arguments.target)
        
        print (  'Main                   : ', end='')
        l_MainFilename = os.path.join(EspyConfig.C_RuntimeDirectory, 'main.py')
        sendFile(l_MainFilename, 'main.py', False) #never compile this
               
        for l_File in getRuntimeFiles():
            l_TargetName = l_File.rsplit('/',1)[1]
            print (f'\n{l_File:22s} : ', end='')
            sendFile(l_File, l_TargetName , l_Compile)
        
        if not g_USB:
            print ('\nClrlog  : ', end='')
            g_MQTT.sendCommand('g_Log.clear()' )
        
        resetTarget()
###
    if g_Arguments.configure:
        prepareConfig(g_Arguments.target)
        
        print (  'Config  : ', end='')
        l_Answer = sendFile(os.path.join(EspyConfig.C_TmpDirectory, 'Config.py'), '/Config.py', not g_Arguments.source)

        resetTarget()
###
    if g_Arguments.handlers:
        l_HandlerNames = getHandlerList(DeviceList.C_DeviceDescriptor[g_Arguments.target][0])
        for l_HandlerName in l_HandlerNames:
            if g_Arguments.verbose:
                print (f'Handler {l_HandlerName:20s}', end='', flush=True)
                
            sendFile(os.path.join(EspyConfig.C_HandlerDirectory, l_HandlerName+'.py'), f'{l_HandlerName}.py', not g_Arguments.source)
            if g_Arguments.verbose:
                print()
###    
    if g_Arguments.reset:
        resetTarget()
###    
    if g_Arguments.flash:
        flashESP8266()            
###    
    if g_Arguments.rtc:
        setRTC()
###    
                        
    g_MQTT.close()

####################################################################################################
   
if __name__ == '__main__':
    main()  
    
####################################################################################################

from car_pb2 import Info
from car_pb2 import Command
import car_pb2
import socket
from PySide import QtCore
from threading import Thread

UDP_PORT_INCOMING = 7778
UDP_PORT_OUTGOING = 7777
REMOTE_ADDRESS = 'localhost'
SUPPORTED_PROTO_INFO = ['lsens','rsens','fsens','bsens'] #the info supported in the info protocol

class UDPClient(QtCore.QObject):

    update = QtCore.Signal()
    
    def __init__(self):
        super(UDPClient, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        self.info = Info()
        self.cmd = Command()
        self.network_direct = False        
        self._connect()
        
        
    def send(self):
        self.csocket.sendto(self.cmd.SerializeToString(), (REMOTE_ADDRESS,UDP_PORT_OUTGOING))
        
    def _connect(self):
        
        self.socket.bind(('', UDP_PORT_INCOMING))
        self.cmd.name = "SIG_DIRECT_ENABLE"        
        self.send()
        self.running = True
        self.net_th = Thread(target = self.listen_th)
        self.net_th.setDaemon(True)
        self.net_th.start()
        
    def disconnect(self):
    
        self.cmd.name = "SIG_DIRECT_DISABLE"
        self.send()
        self.running = False
        self.csocket.close()
        self.socket.close()
        
    def sendCommand(self, **command):
        self.cmd.name = command['name']
        if 'value' in command:
            self.cmd.value = command['value']
        self.send()
        
    def listen_th(self):
    
        while self.running == True:
            
            dataFromClient, address = self.socket.recvfrom(60000) # blocks until packet received            
            self.info.ParseFromString(dataFromClient)
            self.update.emit()
            
    def getUpdate(self):
    
        return {
            'fsens':self.info.fsens,
            'bsens':self.info.bsens,
            'rsens':self.info.rsens,
            'lsens':self.info.lsens}
        
        







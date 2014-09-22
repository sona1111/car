import sys
from PySide import QtGui, QtCore
from udp import UDPClient

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.net = UDPClient()        
        self.initUI()
        self.log('ready!')
        self.net.update.connect(self.updateStatus)
        
        
    def initUI(self):      

        self.col = QtGui.QColor(0, 0, 0)       

        sendBtn = QtGui.QPushButton('Transmit', self)
        sendBtn.move(50, 100)

        sendBtn.clicked.connect(self.sendCmd)

        self.lbl = QtGui.QLabel("Choose...", self)

        self.combo = QtGui.QComboBox(self)
        self.combo.addItem("go")
        self.combo.addItem("stop") 

        self.combo.move(50, 50)
        self.lbl.move(50, 30)

        self.square = QtGui.QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)                    
            
        self.speedChooser = QtGui.QDoubleSpinBox(self)
        self.speedChooser.setRange(0.0, 100.0)
        self.speedChooser.move(130,50)
        
        self.logw = QtGui.QPlainTextEdit(self)
        self.logw.setReadOnly(True)
        self.logw.move(50, 150)
        
        self.statusw = QtGui.QPlainTextEdit(self)
        self.statusw.setReadOnly(True)
        self.statusw.move(210, 50)
        self.statusw.setMaximumSize(200,100)
        
        self.setGeometry(300, 300, 450, 400)
        self.setWindowTitle('Multifunction Car App')
        self.show()
        
    def sendCmd(self):
        
        if self.combo.currentText() == 'go':
            self.net.sendCommand(name='go', value=self.speedChooser.value())
            self.log("Sent packet 'go' with value %d" % self.speedChooser.value())
        elif self.combo.currentText() == 'stop':
            self.net.sendCommand(name='stop')
            self.log("Sent packet 'stop'")
            
    def updateStatus(self):
        
        update = self.net.getUpdate()
        self.log('Got info Update!')
        self.statusw.clear()
        self.statusw.appendPlainText("Front Sensor %s" % (round(update['fsens'],2)) +
                                   "\nBack Sensor %s" % (round(update['bsens'],2)) +
                                   "\nLeft Sensor %s" % (round(update['lsens'],2)) +
                                   "\nRight Sensor %s" % (round(update['rsens'],2)))
            
    def log(self, text):
        self.logw.appendPlainText(text)
            
    def closeEvent(self, event):
    
        self.net.disconnect()
        event.accept()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

from PyQt5.QtWidgets import *

from PyQt5.QtCore import QProcess, Qt
import sys

import socCommands as soc
import gnu_schematic as gnu

def textClickHandler(window : QMainWindow, qline : QLineEdit, proc : QProcess):
    window.write(proc, f'{qline.text()}\n')
    qline.clear()

class BeamFreqSetter:
    def __init__(self, window : QMainWindow, beamNumber):
        self.beamNumber = beamNumber
        self.beamFreqSetter = QHBoxLayout()
        self.beamFreqSetterLineEdit = QLineEdit()
        self.beamFreqSetterLineEdit.setPlaceholderText("Freq")
        self.beamFreqSetterLineEdit.returnPressed.connect(lambda: window.write(window.sshClient, soc.setBeamFreqCmd(self.beamNumber, float(self.beamFreqSetterLineEdit.text()))))
        self.beamFreqSetter.addWidget(self.beamFreqSetterLineEdit,1)
        self.beamFreqSetterSlider = QSlider(Qt.Horizontal)
        self.beamFreqSetterSlider.setMinimum(435000)
        self.beamFreqSetterSlider.setMaximum(438000)
        self.beamFreqSetterSlider.valueChanged.connect(lambda: self.beamFreqSetterLineEdit.setText(str(self.beamFreqSetterSlider.value()/1000)))
        self.beamFreqSetterSlider.sliderReleased.connect(lambda: window.write(window.sshClient, soc.setBeamFreqCmd(self.beamNumber, float(self.beamFreqSetterLineEdit.text()))))
        self.beamFreqSetter.addWidget(self.beamFreqSetterSlider,2)

    def getLayout(self):
        return self.beamFreqSetter

            
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍫🍓FranUI🍓🍫")

        #Set up processes
        self.server, self.serverMessenger = self.setUpProcess("server")
        self.sshClient, self.sshClientMessenger = self.setUpProcess("sshClient")
        self.write(self.sshClient, soc.startCmd())

        self.serverText = QLineEdit()
        self.serverText.setPlaceholderText("Write command to server")
        self.serverText.returnPressed.connect(lambda: textClickHandler(self, self.serverText, self.server))

        self.sshClientText = QLineEdit()
        self.sshClientText.setPlaceholderText("Write command to CIAA")
        self.sshClientText.returnPressed.connect(lambda: textClickHandler(self, self.sshClientText, self.sshClient))

        self.initLayout()      
    
    def initLayout(self):
        dataControlTab = QWidget()
        self.consolesTab = QWidget()
        dataControlTabLayout = QHBoxLayout()
        dataSelectorLayout = QVBoxLayout()

        #Data source
        dataSelectorVLayout = QVBoxLayout()
        dataSelectorVLayout.setAlignment(Qt.AlignTop)
        dataSourceLabel = QLabel("Data source")
        self.dataSourceSelector = QComboBox()
        self.dataSourceSelector.addItems([item.toString() for item in soc.DataSource])
        self.dataSourceSelector.currentIndexChanged.connect(lambda: self.write(self.sshClient, soc.setDataSourceCmd(soc.DataSource(self.dataSourceSelector.currentIndex()))))
        dataSelectorVLayout.addWidget(dataSourceLabel)
        dataSelectorVLayout.addWidget(self.dataSourceSelector)
        dataSelectorLayout.addLayout(dataSelectorVLayout)
        FIFOInputLabel = QLabel("FIFO input")
        self.FIFOInputSelector = QComboBox()
        self.FIFOInputSelector.addItems([item.toString() for item in soc.FIFOInput])
        self.FIFOInputSelector.currentIndexChanged.connect(lambda: self.write(self.sshClient, soc.setFIFOInputCmd(soc.FIFOInput(self.FIFOInputSelector.currentIndex()))))
        dataSelectorLayout.addWidget(FIFOInputLabel)
        dataSelectorLayout.addWidget(self.FIFOInputSelector)
        dataSelectorLayout.addStretch(1)

        beamFreqSetterLayout = QVBoxLayout()
        beamFreqSetterLayout.setAlignment(Qt.AlignTop)
        beamFreqSetterLabel = QLabel("Beam frequency Selector")
        beamFreqSetterLayout.addWidget(beamFreqSetterLabel)

        self.beamFreqSetters = []
        for i in range(5):
            beamFreqSetterLayout.addWidget(QLabel(f"Beam {i+1} frequency [MHz]"))
            beamFreqSetter = BeamFreqSetter(self, i)
            beamFreqSetterLayout.addLayout(beamFreqSetter.getLayout())
            self.beamFreqSetters.append(beamFreqSetter.getLayout())
        
        dataSelectorLayout.addLayout(beamFreqSetterLayout)
        dataSelectorLayout.addStretch(1)


        #Add button
        launchButton = QPushButton("Launch")
        dataSelectorLayout.addWidget(launchButton)
        dataSelectorLayout.addStretch(1)
        launchButton.clicked.connect(lambda: self.write(self.sshClient, soc.launchAcqCmd()))



        #GNU
        self.dataVisualizerLayout = QVBoxLayout()      
        self.gnuradio = self.runGnu()
        dataControlTabLayout.addLayout(dataSelectorLayout,1)
        dataControlTabLayout.addLayout(self.dataVisualizerLayout,100)
        dataControlTab.setLayout(dataControlTabLayout)

        consolesTabLayout = QHBoxLayout()
        firstConsole = QVBoxLayout()
        firstConsole.addWidget(self.sshClientMessenger)
        firstConsole.addWidget(self.sshClientText)
        consolesTabLayout.addLayout(firstConsole)
        secondConsole = QVBoxLayout()
        secondConsole.addWidget(self.serverMessenger)
        secondConsole.addWidget(self.serverText)
        consolesTabLayout.addLayout(secondConsole)
        self.consolesTab.setLayout(consolesTabLayout)

        tabs = QTabWidget()
        tabs.addTab(dataControlTab, "Data Control")
        tabs.addTab(self.consolesTab, "Consoles")

        ## Window
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(tabs)

        w = QWidget()
        w.setLayout(windowLayout)

        self.setCentralWidget(w)

    def setUpProcess(self, name):
        proc = self.startProcess(name)
        messenger = self.createMessanger()
        self.handleCommunications(proc, messenger)
        return proc, messenger

    def handleCommunications(self, process : QProcess, messenger):
        process.readyReadStandardOutput.connect(lambda: self.handleStdout(process, messenger))
        process.readyReadStandardError.connect(lambda: self.handleStderr(process, messenger))

    def createMessanger(self):
        msg = QPlainTextEdit()
        msg.setReadOnly(True)
        return msg

    def write(self, process : QProcess, msg):
        process.writeData(msg.encode("utf8"))

    def startProcess(self, name):
        proc = QProcess()
        proc.start("python3", [f'{name}.py'])
        return proc

    def handleStderr(self, process, messenger):
        data = process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        messenger.appendPlainText(stderr)

    def handleStdout(self, process : QProcess, messenger):
        data = process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        messenger.appendPlainText(stdout)

    def closeEvent(self, event):
        quit_msg = "Seguro que querés salir?"
        reply = QMessageBox.question(self, 'Cerrar', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.write(self.server, "stop\n")
            self.server.close()
            self.sshClient.close()
            event.accept()
        else:
            event.ignore()
            
    def runGnu(self, top_block_cls=gnu.bf_fixed_doa):
        try:
            self.tb = top_block_cls()
            self.tb.start()
            self.win = QMainWindow()
            self.main_widget = QWidget()
            self.main_layout = QVBoxLayout()
            self.main_widget.setLayout(self.main_layout)
            self.dataVisualizerLayout.addWidget(self.tb.top_scroll)
        except Exception as e:
            print(e)
            self.dataVisualizerLayout.addWidget(QLabel("No se pudo iniciar GNU, conecte la placa y reinicie el programa"))
            

app = QApplication(sys.argv)

w = MainWindow()
w.show()

def quitting():
    if hasattr(w, 'tb'):
        w.tb.stop()
        w.tb.wait()
app.aboutToQuit.connect(quitting)
app.exec_()
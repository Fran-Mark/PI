from PyQt5.QtWidgets import *

from PyQt5.QtCore import QProcess, Qt, QThread, QObject
import sys

from PyQt5.QtGui import QFont, QTextCursor, QDoubleValidator

import socCommands as soc
import gnu_schematic as gnu
from time import sleep
def textClickHandler(window : QMainWindow, qline : QLineEdit, proc : QProcess):
    window.write(proc, f'{qline.text()}\n')
    qline.clear()

class BeamFreqSetter:
    def __init__(self, window : QMainWindow, beamNumber, buttonGroup : QButtonGroup):
        self.window = window
        self.beamNumber = beamNumber
        self.beamFreqSetter = QHBoxLayout()
        self.buttonGroup = buttonGroup
        self.button = QPushButton(f'Beam {beamNumber + 1}')
        self.button.setCheckable(True)
        self.button.clicked.connect(lambda: self.buttonClickHandler())

        buttonGroup.addButton(self.button)

        self.beamFreqSetter.addWidget(self.button,3)
        self.beamFreqSetterLineEdit = QLineEdit(alignment=Qt.AlignCenter)
        self.beamFreqSetterLineEdit.setValidator(QDoubleValidator(bottom=435, top=438, decimals=3))
        self.beamFreqSetterLineEdit.setPlaceholderText("Freq")
        self.beamFreqSetterLineEdit.returnPressed.connect(self.onReturnPressed)
        self.beamFreqSetter.addWidget(self.beamFreqSetterLineEdit,3)
        self.beamFreqSetterSlider = QSlider(Qt.Horizontal)
        self.beamFreqSetterSlider.setMinimum(435000)
        self.beamFreqSetterSlider.setMaximum(438000)
        self.beamFreqSetterSlider.valueChanged.connect(lambda: self.beamFreqSetterLineEdit.setText(str(self.beamFreqSetterSlider.value()/1000)))
        self.beamFreqSetterSlider.sliderReleased.connect(lambda: window.write(window.sshClient, soc.setBeamFreqCmd(self.beamNumber, float(self.beamFreqSetterLineEdit.text()))))

        self.beamFreqSetter.addWidget(self.beamFreqSetterSlider,4)

        self.initValues()

    def initValues(self):
        self.button.setChecked(self.window.configData['activeBeam'] == self.beamNumber)
        self.buttonClickHandler()

        self.beamFreqSetterLineEdit.setText(str(self.window.configData[f'beam{self.beamNumber + 1}Freq']))

        self.beamFreqSetterSlider.setValue(int(self.window.configData[f'beam{self.beamNumber + 1}Freq']*1000))

    def onReturnPressed(self):  
        self.beamFreqSetterSlider.setValue(int(float(self.beamFreqSetterLineEdit.text())*1000))
        self.window.write(self.window.sshClient, soc.setBeamFreqCmd(self.beamNumber, float(self.beamFreqSetterLineEdit.text())))
    
    
    def getLayout(self):
        return self.beamFreqSetter

    def buttonClickHandler(self):
        if self.button.isChecked():
            self.window.write(self.window.sshClient, soc.selectBeamCmd(self.beamNumber))
            self.button.setStyleSheet('QPushButton:checked {background-color: green}')


class ServerStatusObject(QObject):
    def __init__(self, window : QMainWindow):
        super().__init__()
        self.window = window
    def run(self):
        while True:
            self.window.serverStatusTextBox.setText(self.window.serverMessenger.toPlainText())
            sleep(1)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍫🍓FranUI🍓🍫")

        #Set up processes
        self.server, self.serverMessenger = self.setUpProcess("server")
        self.sshClient, self.sshClientMessenger = self.setUpProcess("sshClient")

        self.configData = soc.readConfigData()
        self.serverText = QLineEdit()
        self.serverText.setPlaceholderText("Write command to server")
        self.serverText.returnPressed.connect(lambda: textClickHandler(self, self.serverText, self.server))

        self.sshClientText = QLineEdit()
        self.sshClientText.setPlaceholderText("Write command to CIAA")
        self.sshClientText.returnPressed.connect(lambda: textClickHandler(self, self.sshClientText, self.sshClient))

        self.configData = soc.readConfigData()
        self.initLayout()

    def initLayout(self):
        dataControlTab = QWidget()
        self.consolesTab = QWidget()
        dataControlTabLayout = QHBoxLayout()
        dataSelectorLayout = QVBoxLayout()

        #Data source
        dataSelectorGroupBox = QGroupBox()
        dataSelectorVLayout = QVBoxLayout()
        dataSelectorGroupBox.setLayout(dataSelectorVLayout)
        dataSelectorLayout.addWidget(dataSelectorGroupBox)

        dataSelectorVLayout.setAlignment(Qt.AlignTop)
        dataSourceLabel = QLabel("Data source", font=QFont("Utopia", 12, QFont.Bold))
        self.dataSourceSelector = QComboBox(font=QFont("Cantarell", 10))
        self.dataSourceSelector.addItems([item.toString() for item in soc.DataSource])
        self.dataSourceSelector.currentIndexChanged.connect(lambda: self.write(self.sshClient, soc.setDataSourceCmd(soc.DataSource(self.dataSourceSelector.currentIndex()))))
        #set default value
        self.dataSourceSelector.setCurrentIndex(self.configData['dataSource'])

        dataSelectorVLayout.addWidget(dataSourceLabel)
        dataSelectorVLayout.addWidget(self.dataSourceSelector)
        dataSelectorLayout.addLayout(dataSelectorVLayout)

        FIFOInputGroupBox = QGroupBox()
        FIFOInputVLayout = QVBoxLayout()
        FIFOInputGroupBox.setLayout(FIFOInputVLayout)
        dataSelectorLayout.addWidget(FIFOInputGroupBox)
        FIFOInputLabel = QLabel("FIFO input", font=QFont("Utopia", 12, QFont.Bold))
        self.FIFOInputSelector = QComboBox(font=QFont("Cantarell", 10))
        self.FIFOInputSelector.addItems([item.toString() for item in soc.FIFOInput])
        self.FIFOInputSelector.currentIndexChanged.connect(lambda: self.write(self.sshClient, soc.setFIFOInputCmd(soc.FIFOInput(self.FIFOInputSelector.currentIndex()))))
        #set default value
        self.FIFOInputSelector.setCurrentIndex(self.configData['fifoInput'])
        FIFOInputVLayout.addWidget(FIFOInputLabel)
        FIFOInputVLayout.addWidget(self.FIFOInputSelector)
        dataSelectorLayout.addLayout(FIFOInputVLayout)

        localOscGroupBox = QGroupBox()
        localOscFreqSetter = QVBoxLayout()
        localOscGroupBox.setLayout(localOscFreqSetter)
        dataSelectorLayout.addWidget(localOscGroupBox)
        localOscSetterLabel = QLabel("Local oscillator frequency [MHz]", font=QFont("Utopia", 12, QFont.Bold))
        localOscFreqSetter.addWidget(localOscSetterLabel)

        localOscFreqSetterHLayout = QHBoxLayout()
        localOscFreqSetterLineEdit = QLineEdit(alignment=Qt.AlignCenter)
        #set validation to only accept numbers
        localOscFreqSetterLineEdit.setValidator(QDoubleValidator(bottom=0, top=32.5, decimals=3))
        localOscFreqSetterLineEdit.setPlaceholderText("Freq")
        localOscFreqSetterLineEdit.returnPressed.connect(lambda: self.write(self.sshClient, soc.setLocalOscFreqCmd(float(localOscFreqSetterLineEdit.text()))))
        #set default value
        localOscFreqSetterLineEdit.setText(str(self.configData['localOscFreq']))
        localOscFreqSetterHLayout.addWidget(localOscFreqSetterLineEdit,1)
        localOscFreqSetterSlider = QSlider(Qt.Horizontal)
        localOscFreqSetterSlider.setMinimum(0)
        localOscFreqSetterSlider.setMaximum(32500)
        localOscFreqSetterSlider.valueChanged.connect(lambda: localOscFreqSetterLineEdit.setText(str(localOscFreqSetterSlider.value()/1000)))
        localOscFreqSetterSlider.sliderReleased.connect(lambda: self.write(self.sshClient, soc.setLocalOscFreqCmd(float(localOscFreqSetterLineEdit.text()))))
        #set default value
        localOscFreqSetterSlider.setValue(int(self.configData['localOscFreq']*1000))
        localOscFreqSetterHLayout.addWidget(localOscFreqSetterSlider,2)
        localOscFreqSetter.addLayout(localOscFreqSetterHLayout)
        dataSelectorLayout.addLayout(localOscFreqSetter)

        beamFreqSetterGroupBox = QGroupBox()
        beamFreqSetterLayout = QVBoxLayout()
        beamFreqSetterGroupBox.setLayout(beamFreqSetterLayout)
        dataSelectorLayout.addWidget(beamFreqSetterGroupBox)
        beamFreqSetterLabel = QLabel("Beam frequency selector [MHz]", font=QFont("Utopia", 12, QFont.Bold))
        beamFreqSetterLayout.addWidget(beamFreqSetterLabel)
        beamFreqSetterLayout.addSpacing(15)


        self.beamFreqSetters = []
        self.buttonGroup = QButtonGroup()

        for i in range(5):
            #beamFreqSetterLayout.addWidget(QLabel(f"Beam {i+1} frequency", font=QFont("Cantarell", 10)))
            beamFreqSetterLayout.addSpacing(1)
            beamFreqSetter = BeamFreqSetter(self, i, buttonGroup=self.buttonGroup)
            beamFreqSetterLayout.addLayout(beamFreqSetter.getLayout())
            beamFreqSetterLayout.addSpacing(10)
            self.beamFreqSetters.append(beamFreqSetter.getLayout())

        dataSelectorLayout.addLayout(beamFreqSetterLayout)
        dataSelectorLayout.addStretch(1)

        serverStatusGroupBox = QGroupBox()
        serverStatusLayout = QVBoxLayout()
        serverStatusGroupBox.setLayout(serverStatusLayout)
        dataSelectorLayout.addWidget(serverStatusGroupBox)
        serverStatusLabel = QLabel("Server status", font=QFont("Utopia", 12, QFont.Bold))
        serverStatusLayout.addWidget(serverStatusLabel)
        serverStatusLayout.addSpacing(15)
        #add non-editable text box
        # self.serverStatusTextBox = QTextEdit()
        # self.serverStatusTextBox.setReadOnly(True)
        # self.serverStatusTextBox.setFont(QFont("Cantarell", 10))
        # serverStatusLayout.addWidget(self.serverStatusTextBox)
        # serverStatusLayout.addStretch(1)
        #launch thread to update server status
        # self.serverStatusObject = ServerStatusObject(self)
        # self.serverStatusThread = QThread()
        # self.serverStatusObject.moveToThread(self.serverStatusThread)
        # self.serverStatusThread.started.connect(self.serverStatusObject.run)
        # self.serverStatusThread.start()
        



        launchButton = QPushButton("Launch capture")
        launchButton.setFont(QFont("Utopia", 12, QFont.Bold))
        dataSelectorLayout.addWidget(launchButton)
        launchButton.setStyleSheet("background-color: green; color: white")
        launchButton.setFixedHeight(50)
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

    def handleCommunications(self, process : QProcess, messenger : QPlainTextEdit):
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

    def handleStderr(self, process : QProcess, messenger : QPlainTextEdit):
        data = process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        messenger.appendPlainText(stderr)

    def handleStdout(self, process : QProcess, messenger : QPlainTextEdit):
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

    def runGnu(self, top_block_cls=gnu.maint):
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
            self.dataVisualizerLayout.addWidget(QLabel("No se pudo iniciar GNU, conecte la placa y reinicie el programa", font=QFont("Cantarell", 14), alignment=Qt.AlignCenter))





app = QApplication(sys.argv)

w = MainWindow()

w.show()

def quitting():
    if hasattr(w, 'tb'):
        w.tb.stop()
        w.tb.wait()
app.aboutToQuit.connect(quitting)
app.exec_()
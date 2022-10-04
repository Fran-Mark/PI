from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QTabWidget, QLineEdit, QMessageBox)
from PyQt5.QtCore import QProcess
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍫🍓FranUI🍓🍫")

        ## Processes
        self.server, self.serverMessenger = self.setUpProcess("server")
        self.dummy, self.dummyMessenger = self.setUpProcess("dummy")

        self.writeServerButton = QPushButton("Write command to server")
        self.writeDummyButton = QPushButton("Write command to dummy")

        self.serverText = QLineEdit()
        self.serverText.setPlaceholderText("Write command to server")
        self.serverText.returnPressed.connect(lambda: self.write(self.server, f'{self.serverText.text()}\n'))

        self.dummyText = QLineEdit()
        self.dummyText.setPlaceholderText("Write command to dummy")
        self.dummyText.returnPressed.connect(lambda: self.write(self.dummy, f'{self.dummyText.text()}\n'))

        self.writeServerButton.clicked.connect(lambda: self.write(self.server, f'{self.serverText.text()}\n'))
        self.writeDummyButton.clicked.connect(lambda: self.write(self.dummy, f'{self.dummyText.text()}\n'))

        ## Tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        tab1Layout = QVBoxLayout()
        tab1Layout.addWidget(self.serverText)
        tab1Layout.addWidget(self.writeServerButton)
        tab1Layout.addWidget(self.serverMessenger)
        self.tab1.setLayout(tab1Layout)

        tab2Layout = QVBoxLayout()
        tab2Layout.addWidget(self.dummyText)
        tab2Layout.addWidget(self.writeDummyButton)
        tab2Layout.addWidget(self.dummyMessenger)
        self.tab2.setLayout(tab2Layout)

        tabs = QTabWidget()
        tabs.addTab(self.tab1, "Server")
        tabs.addTab(self.tab2, "Dummy")

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
        process.stateChanged.connect(lambda state: self.handle_state(state, messenger))

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

    def handle_state(self, state, messenger):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        messenger.appendPlainText(f"State changed: {state_name}")

    def closeEvent(self, event):
        quit_msg = "Seguro que querés salir?"
        reply = QMessageBox.question(self, 'Cerrar', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.write(self.server, "stop\n")
            self.server.close()
            self.dummy.close()
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()
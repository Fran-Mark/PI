from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QProgressBar)
from PyQt5.QtCore import QProcess
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.writeServerButton = QPushButton("Write to server")

        self.writeDummyButton = QPushButton("Write to dummy")

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.server = self.start_process('server')
        self.dummy = self.start_process('dummy')
        self.writeServerButton.pressed.connect(lambda: self.write(self.server, "Hello server!\n"))
        self.writeDummyButton.pressed.connect(lambda: self.write(self.dummy, "Hello dummy!\n"))


        l = QVBoxLayout()
        l.addWidget(self.writeServerButton)
        l.addWidget(self.writeDummyButton)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)


    def message(self, s):
        self.text.appendPlainText(s)

    def write(self, process : QProcess, msg):
        process.writeData(msg.encode("utf8"))


    def start_process(self, name):
        self.message("Executing process")
        proc = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        proc.readyReadStandardOutput.connect(lambda: self.handle_stdout(proc))
        proc.readyReadStandardError.connect(lambda: self.handle_stderr(proc))
        proc.stateChanged.connect(self.handle_state)
        proc.start("python3", [f'{name}.py'])
        return proc

    def handle_stderr(self, process):
        data = process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self, process : QProcess):
        data = process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()
    
    
    
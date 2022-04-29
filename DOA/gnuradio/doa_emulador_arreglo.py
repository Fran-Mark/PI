#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DoA de señales adquiridas con emulador de arreglo
# Author: fran
# GNU Radio version: 3.8.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import beamforming

from gnuradio import qtgui

class doa_emulador_arreglo(gr.top_block, Qt.QWidget):

    def __init__(self, fc=146e6, mx=4, my=4):
        gr.top_block.__init__(self, "DoA de señales adquiridas con emulador de arreglo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DoA de señales adquiridas con emulador de arreglo")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "doa_emulador_arreglo")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc
        self.mx = mx
        self.my = my

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.fs = fs = 65e6
        self.element_separation = element_separation = 0.5*299792458/fc

        ##################################################
        # Blocks
        ##################################################
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_short*1, samp_rate,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 16)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(2/8192)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(16)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_short*1, '/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/capturas-jose/20201117_120307_sin_header', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*16, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-8191.5)
        self.beamforming_randomsampler_0 = beamforming.randomsampler(mx*my, 8)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(mx, my, fc, element_separation, 1, 128)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.beamforming_doaesprit_py_cf_0, 'doa_port'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.beamforming_randomsampler_0, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.beamforming_randomsampler_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_short_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "doa_emulador_arreglo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_element_separation(0.5*299792458/self.fc)

    def get_mx(self):
        return self.mx

    def set_mx(self, mx):
        self.mx = mx

    def get_my(self):
        return self.my

    def set_my(self, my):
        self.my = my

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs

    def get_element_separation(self):
        return self.element_separation

    def set_element_separation(self, element_separation):
        self.element_separation = element_separation




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--fc", dest="fc", type=eng_float, default="146.0M",
        help="Set Carrier frequency [default=%(default)r]")
    parser.add_argument(
        "--mx", dest="mx", type=intx, default=4,
        help="Set # elements in x [default=%(default)r]")
    parser.add_argument(
        "--my", dest="my", type=intx, default=4,
        help="Set # elements in y [default=%(default)r]")
    return parser


def main(top_block_cls=doa_emulador_arreglo, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(fc=options.fc, mx=options.mx, my=options.my)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()

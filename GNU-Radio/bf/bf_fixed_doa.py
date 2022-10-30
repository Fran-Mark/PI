#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BF for fixed DOA
# Author: fran
# GNU Radio version: v3.8.5.0-6-g57bd109d

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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from stream_demux import stream_demux_swig
import beamforming

from gnuradio import qtgui

class bf_fixed_doa(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "BF for fixed DOA")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BF for fixed DOA")
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

        self.settings = Qt.QSettings("GNU Radio", "bf_fixed_doa")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 65e3

        ##################################################
        # Blocks
        ##################################################
        self.stream_demux_stream_demux_0 = stream_demux_swig.stream_demux(gr.sizeof_short*1, (32000, 44))
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_gr_complex*1, 16)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, '192.168.0.21', 12345, 64088, True)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_char*1, 88)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 16)
        self.blocks_short_to_char_0 = blocks.short_to_char(1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_3 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_2_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_3 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_1_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.beamforming_HeaderReader_0 = beamforming.HeaderReader()


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_short_to_char_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_short_to_char_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_vector_to_streams_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.beamforming_HeaderReader_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.stream_demux_stream_demux_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 3), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 14), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 12), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 8), (self.blocks_null_sink_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 4), (self.blocks_null_sink_0_0_0_1, 0))
        self.connect((self.blocks_vector_to_streams_0, 10), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.blocks_vector_to_streams_0, 2), (self.blocks_null_sink_0_0_1_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_null_sink_0_0_1_0_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 6), (self.blocks_null_sink_0_0_2, 0))
        self.connect((self.blocks_vector_to_streams_0, 15), (self.blocks_null_sink_0_0_3, 0))
        self.connect((self.blocks_vector_to_streams_0, 13), (self.blocks_null_sink_0_1, 0))
        self.connect((self.blocks_vector_to_streams_0, 9), (self.blocks_null_sink_0_1_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 5), (self.blocks_null_sink_0_1_1, 0))
        self.connect((self.blocks_vector_to_streams_0, 11), (self.blocks_null_sink_0_2, 0))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.blocks_null_sink_0_2_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 7), (self.blocks_null_sink_0_3, 0))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.stream_demux_stream_demux_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.stream_demux_stream_demux_0, 1), (self.blocks_short_to_char_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bf_fixed_doa")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)





def main(top_block_cls=bf_fixed_doa, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

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

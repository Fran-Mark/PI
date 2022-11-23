#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
import pmt
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import beamforming

from gnuradio import qtgui

class default(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "default")

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
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_c(
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
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.hilbert_fc_0_0_1_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_1 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_1 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.hilbert_fc_0 = filter.hilbert_fc(16*4, firdes.WIN_HAMMING, 6.76)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_short*1, samp_rate,True)
        self.blocks_streams_to_vector_0_1 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 16)
        self.blocks_short_to_float_0_0 = blocks.short_to_float(1, 1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(2/8192)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0_0_1 = blocks.file_source(gr.sizeof_short*1, '/run/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/GitHub/DOA/test/remake_desde_csv.npy', True, 64, 0)
        self.blocks_file_source_0_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_deinterleave_0_0 = blocks.deinterleave(gr.sizeof_float*1, 1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(-8191.5)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(4, 4, 436e6, (299792458/(2*436e6)), 1, 128)
        self.beamforming_beamformer_0 = beamforming.beamformer(4, 4, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.beamforming_doaesprit_py_cf_0, 'doa_port'), (self.beamforming_beamformer_0, 'doa_port'))
        self.msg_connect((self.beamforming_doaesprit_py_cf_0, 'doa_port'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.beamforming_beamformer_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 5), (self.hilbert_fc_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 4), (self.hilbert_fc_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 3), (self.hilbert_fc_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 2), (self.hilbert_fc_0_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 13), (self.hilbert_fc_0_0_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 1), (self.hilbert_fc_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 8), (self.hilbert_fc_0_0_0_0_0_0_1, 0))
        self.connect((self.blocks_deinterleave_0_0, 9), (self.hilbert_fc_0_0_0_0_0_0_1_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 10), (self.hilbert_fc_0_0_0_0_0_0_1_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 11), (self.hilbert_fc_0_0_0_0_0_0_1_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 15), (self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 12), (self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 14), (self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0, 0))
        self.connect((self.blocks_deinterleave_0_0, 6), (self.hilbert_fc_0_0_1, 0))
        self.connect((self.blocks_deinterleave_0_0, 7), (self.hilbert_fc_0_0_1_0, 0))
        self.connect((self.blocks_file_source_0_0_1, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_deinterleave_0_0, 0))
        self.connect((self.blocks_short_to_float_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_streams_to_vector_0_1, 0), (self.beamforming_beamformer_0, 0))
        self.connect((self.blocks_streams_to_vector_0_1, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_short_to_float_0_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_streams_to_vector_0_1, 0))
        self.connect((self.hilbert_fc_0_0, 0), (self.blocks_streams_to_vector_0_1, 5))
        self.connect((self.hilbert_fc_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 4))
        self.connect((self.hilbert_fc_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 3))
        self.connect((self.hilbert_fc_0_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 2))
        self.connect((self.hilbert_fc_0_0_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 13))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 1))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1, 0), (self.blocks_streams_to_vector_0_1, 8))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0, 0), (self.blocks_streams_to_vector_0_1, 9))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0_0, 0), (self.blocks_streams_to_vector_0_1, 10))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 11))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 15))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 12))
        self.connect((self.hilbert_fc_0_0_0_0_0_0_1_0_0_0_0_0_0, 0), (self.blocks_streams_to_vector_0_1, 14))
        self.connect((self.hilbert_fc_0_0_1, 0), (self.blocks_streams_to_vector_0_1, 6))
        self.connect((self.hilbert_fc_0_0_1_0, 0), (self.blocks_streams_to_vector_0_1, 7))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "default")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)





def main(top_block_cls=default, options=None):

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

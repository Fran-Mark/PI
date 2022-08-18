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
        self.qtgui_sink_x_1 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            fs, #bw
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
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 16)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_short*1, samp_rate,True)
        self.blocks_streams_to_vector_0_1 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 16)
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 16)
        self.blocks_short_to_float_0_0 = blocks.short_to_float(1, 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*16)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(2/8192)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0_0_1 = blocks.file_source(gr.sizeof_short*1, '/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/GitHub/DOA/test/remake_desde_csv.npy', True, 64, 0)
        self.blocks_file_source_0_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*16, '/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/etc/output', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_deinterleave_0_0 = blocks.deinterleave(gr.sizeof_float*1, 1)
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_gr_complex*1, 1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(-8191.5)
        self.beamforming_randomsampler_1 = beamforming.randomsampler(16, 8)
        self.beamforming_doaesprit_py_cf_0 = beamforming.doaesprit_py_cf(mx, my, fc, element_separation, 1, 128)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.beamforming_doaesprit_py_cf_0, 'doa_port'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.beamforming_randomsampler_1, 0), (self.beamforming_doaesprit_py_cf_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_deinterleave_0, 5), (self.blocks_streams_to_vector_0, 5))
        self.connect((self.blocks_deinterleave_0, 4), (self.blocks_streams_to_vector_0, 4))
        self.connect((self.blocks_deinterleave_0, 7), (self.blocks_streams_to_vector_0, 7))
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_streams_to_vector_0, 0))
        self.connect((self.blocks_deinterleave_0, 12), (self.blocks_streams_to_vector_0, 12))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_streams_to_vector_0, 1))
        self.connect((self.blocks_deinterleave_0, 15), (self.blocks_streams_to_vector_0, 15))
        self.connect((self.blocks_deinterleave_0, 8), (self.blocks_streams_to_vector_0, 8))
        self.connect((self.blocks_deinterleave_0, 13), (self.blocks_streams_to_vector_0, 13))
        self.connect((self.blocks_deinterleave_0, 2), (self.blocks_streams_to_vector_0, 2))
        self.connect((self.blocks_deinterleave_0, 9), (self.blocks_streams_to_vector_0, 9))
        self.connect((self.blocks_deinterleave_0, 10), (self.blocks_streams_to_vector_0, 10))
        self.connect((self.blocks_deinterleave_0, 6), (self.blocks_streams_to_vector_0, 6))
        self.connect((self.blocks_deinterleave_0, 11), (self.blocks_streams_to_vector_0, 11))
        self.connect((self.blocks_deinterleave_0, 3), (self.blocks_streams_to_vector_0, 3))
        self.connect((self.blocks_deinterleave_0, 14), (self.blocks_streams_to_vector_0, 14))
        self.connect((self.blocks_deinterleave_0, 2), (self.qtgui_sink_x_1, 0))
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
        self.connect((self.blocks_streams_to_vector_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_streams_to_vector_0_1, 0), (self.beamforming_randomsampler_1, 0))
        self.connect((self.blocks_streams_to_vector_0_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_streams_to_vector_0_1, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_short_to_float_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_deinterleave_0, 0))
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
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.qtgui_sink_x_1.set_frequency_range(0, self.fs)

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

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
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from stream_demux import stream_demux_swig

from gnuradio import qtgui

class test(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "test")

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
        self.samp_rate = samp_rate = 162.5e3

        ##################################################
        # Blocks
        ##################################################
        self.stream_demux_stream_demux_2 = stream_demux_swig.stream_demux(gr.sizeof_int*1, 16*(1,))
        self.stream_demux_stream_demux_1 = stream_demux_swig.stream_demux(gr.sizeof_int*1, (16000,22))
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            4096, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(True)


        labels = ['Todas las señales', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            4096, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Una sola señal', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_udp_source_0_0_0 = blocks.udp_source(gr.sizeof_int*1, '192.168.0.21', 12345, 64088, True)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_3 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_2_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_2 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_1_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_1_0_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_1_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_2 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_1_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_0_1 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_0_0_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_0_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3_0 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_null_sink_0_0_3 = blocks.null_sink(gr.sizeof_int*1)
        self.blocks_int_to_float_0_0 = blocks.int_to_float(1, 1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_int*1, '/run/media/fran/46FAA90DFAA8FA77/Ventanas/IB/PI/GitHub/GNU-Radio/UDP_sock_test/UDP_to_file_sink/file_py', False)
        self.blocks_file_sink_0.set_unbuffered(True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_int_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_int_to_float_0_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_udp_source_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_udp_source_0_0_0, 0), (self.stream_demux_stream_demux_1, 0))
        self.connect((self.stream_demux_stream_demux_1, 0), (self.blocks_int_to_float_0_0, 0))
        self.connect((self.stream_demux_stream_demux_1, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.stream_demux_stream_demux_1, 0), (self.stream_demux_stream_demux_2, 0))
        self.connect((self.stream_demux_stream_demux_2, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 1), (self.blocks_null_sink_0_0_3, 0))
        self.connect((self.stream_demux_stream_demux_2, 0), (self.blocks_null_sink_0_0_3_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 2), (self.blocks_null_sink_0_0_3_0_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 6), (self.blocks_null_sink_0_0_3_0_0_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 14), (self.blocks_null_sink_0_0_3_0_0_0_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 10), (self.blocks_null_sink_0_0_3_0_0_1, 0))
        self.connect((self.stream_demux_stream_demux_2, 4), (self.blocks_null_sink_0_0_3_0_1, 0))
        self.connect((self.stream_demux_stream_demux_2, 12), (self.blocks_null_sink_0_0_3_0_1_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 8), (self.blocks_null_sink_0_0_3_0_2, 0))
        self.connect((self.stream_demux_stream_demux_2, 3), (self.blocks_null_sink_0_0_3_1, 0))
        self.connect((self.stream_demux_stream_demux_2, 7), (self.blocks_null_sink_0_0_3_1_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 15), (self.blocks_null_sink_0_0_3_1_0_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 11), (self.blocks_null_sink_0_0_3_1_1, 0))
        self.connect((self.stream_demux_stream_demux_2, 5), (self.blocks_null_sink_0_0_3_2, 0))
        self.connect((self.stream_demux_stream_demux_2, 13), (self.blocks_null_sink_0_0_3_2_0, 0))
        self.connect((self.stream_demux_stream_demux_2, 9), (self.blocks_null_sink_0_0_3_3, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)





def main(top_block_cls=test, options=None):

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 FranMark.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy as np
from gnuradio import gr

class beamformer_from_angles(gr.basic_block):
    """
    docstring for block beamformer_from_angles
    """
    def __init__(self, azimuth, elevation, freq):
        self.azimuth = np.deg2rad(azimuth)
        self.elevation = np.deg2rad(elevation)
        self.lambda_ = 299792458/(freq * 1e6)
        self.separation = self.lambda_/2 #Para cambiar esto hay que regenerar el bloque

        self.coefs = np.zeros(16, dtype=np.complex64)
        for j in range(4): 
            for i in range(4):
                self.coefs[j * 4 + i] = np.exp(-1j * 2 * np.pi/self.lambda_ * self.separation * np.cos(self.elevation)*(j*np.cos(self.azimuth) + i*np.sin(self.azimuth)))

        gr.basic_block.__init__(
            self,
            name="beamformer_from_angles",
            in_sig=[(np.complex64, 16)],
            out_sig=[np.complex64],
        )
    def forecast(self, noutput_items, ninput_items_required):
        ninput_items_required[0] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i in range(len(out)):
            out[i] = np.dot(in0[i], self.coefs)/16

        self.consume(0, len(out))
        return len(output_items[0])

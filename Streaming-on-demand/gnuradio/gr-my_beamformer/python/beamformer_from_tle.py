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

from orbit_predictor.locations import ET_CENTRO_ATOMICO, Location
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.predictors.accurate import HighAccuracyTLEPredictor
from datetime import timedelta as td

UTC_OFFSET = -3

def getAzimuthElevation(predictor : HighAccuracyTLEPredictor, location : Location):
    position = predictor.get_position()
    return location.get_azimuth_elev(position)

def getDopplerFactor(predictor : HighAccuracyTLEPredictor, location : Location):
    position = predictor.get_position()
    return location.doppler_factor(position)

class beamformer_from_tle(gr.decim_block):
    """
    docstring for block beamformer_from_tle
    """
    def __init__(self, line1, line2, freq):
        self.line1 = line1
        self.line2 = line2
        self.freq = freq*1e6
        self.predictor = get_predictor_from_tle_lines([line1, line2])
        self.dopplerFactor = getDopplerFactor(self.predictor, ET_CENTRO_ATOMICO)
        self.elevation = 0
        self.azimuth = 0

        gr.decim_block.__init__(self,
            name="beamformer_from_tle",
            in_sig=[(np.complex64, 16)],
            out_sig=[np.complex64], 
            decim=16)


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        #Every 1000 iteratrions 
        if self.nitems_read(0) % 1000 == 0:
            #self.lat, self.lon, self.alt = getCoordinates(self.predictor)
            self.dopplerFactor = getDopplerFactor(self.predictor, ET_CENTRO_ATOMICO)   
            self.azimuth, self.elevation = getAzimuthElevation(self.predictor, ET_CENTRO_ATOMICO)
        #Calculate Doppler shift
        dopplerShift = (self.dopplerFactor -1)*self.freq

        #Correct Doppler shift
        correctedSamples = in0 * np.exp(-1j*2*np.pi*dopplerShift*self.nitems_read(0))
     
        #Do digital beamforming
        exponents = np.zeros(16, dtype=np.complex64)
        for mx in range(4):
            for my in range(4):
                exponents[4*mx + my] = (mx - 1)*np.cos(self.elevation)*np.cos(self.azimuth) + (my - 1)*np.cos(self.elevation)*np.sin(self.azimuth)

        coefs = np.exp(-1j*2*np.pi*0.55*exponents)
        out[:] = np.average(correctedSamples*coefs)
        return len(output_items[0])


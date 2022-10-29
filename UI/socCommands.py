from enum import Enum

ELFS_LOCATION = '/mnt/currentVersions/'
BASE_REG = 0x43C3_0000
FIFO_INPUT_MUX_OFFSET = 4
DATA_SOURCE_MUX_OFFSET = 8
BEAM_FREQ_SETTER_OFFSET = 0xC

def axiWriteCmd(reg, data):
    cmd = ELFS_LOCATION + 'axi_rw_test.elf w {} {}\n'.format(reg, data)
    return cmd

class DataSource(Enum):
    ADC_DATA = 0
    DDS_COMPILER = 1
    COUNTER = 2

    def toString(self):
        if self == DataSource.ADC_DATA:
            return 'ADC data'
        elif self == DataSource.DDS_COMPILER:
            return 'Single tone'
        elif self == DataSource.COUNTER:
            return 'Counter'

class FIFOInput(Enum):
    NONE = 0
    PREPROC_DATA = 1
    COUNTER_POST_PROC = 2
    RAW_DATA = 3
    MUX_DATA = 4
    BAND_MIXER = 5
    BAND_FILTER = 6
    CH_MIXER = 7

    def toString(self):
        if self == FIFOInput.NONE:
            return 'None'
        elif self == FIFOInput.PREPROC_DATA:
            return 'Preprocessing Data'
        elif self == FIFOInput.COUNTER_POST_PROC:
            return 'Postprocessing debug counter'
        elif self == FIFOInput.RAW_DATA:
            return 'Raw ADC data'
        elif self == FIFOInput.MUX_DATA:
            return 'Data directly from the mux'
        elif self == FIFOInput.BAND_MIXER:
            return 'Band mixer output'
        elif self == FIFOInput.BAND_FILTER:
            return 'Band filter output'
        elif self == FIFOInput.CH_MIXER:
            return 'Channel mixer output'

_DataSource = DataSource.ADC_DATA
_FIFOInput = FIFOInput.NONE

def getFIFOInput():
    return _FIFOInput

def getDataSource():
    return _DataSource

def setDataSourceCmd(dataSource):
    return axiWriteCmd(hex(BASE_REG + DATA_SOURCE_MUX_OFFSET)[2:], dataSource.value)

def setFIFOInputCmd(FIFOInput):
    global _FIFOInput
    _FIFOInput = FIFOInput
    return axiWriteCmd(hex(BASE_REG + FIFO_INPUT_MUX_OFFSET)[2:], FIFOInput.value)

def startCmd():
    return ELFS_LOCATION + 'startup.elf\n'

def launchAcqCmd():
    return ELFS_LOCATION + 'sist_adq_1024.elf ' + ELFS_LOCATION + 'client_config\n'

def setBeamFreqCmd(beamNumber, freq : float):
    freqUndersampled = freq - 7*65
    freqBB = freqUndersampled + 18.5
    freqConf = abs(freqBB * 32 / 260.0 * 2**32)
    return axiWriteCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + beamNumber * 4)[2:], hex(int(freqConf))[2:])


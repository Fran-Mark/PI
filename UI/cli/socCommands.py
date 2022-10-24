from enum import Enum

ELFS_LOCATION = '/mnt/currentVersions/'
BASE_REG = 4000_0000
FIFO_INPUT_MUX_OFFSET = 4
DATA_SOURCE_MUX_OFFSET = 8

def formatCmd(reg, data):
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
    BAND_MIXER = 4
    CH_MIXER = 5
    COUNTER_PREPROC = 6

    def toString(self):
        if self == FIFOInput.NONE:
            return 'None'
        elif self == FIFOInput.PREPROC_DATA:
            return 'Preprocessing Data'
        elif self == FIFOInput.COUNTER_POST_PROC:
            return 'Postprocessing debug counter'
        elif self == FIFOInput.RAW_DATA:
            return 'Raw ADC data'
        elif self == FIFOInput.BAND_MIXER:
            return 'Band mixer'
        elif self == FIFOInput.CH_MIXER:
            return 'Channel mixer'
        elif self == FIFOInput.COUNTER_PREPROC:
            return 'Preprocessing debug counter'



_DataSource = DataSource.ADC_DATA
_FIFOInput = FIFOInput.NONE

def getFIFOInput():
    return _FIFOInput

def getDataSource():
    return _DataSource

def setDataSourceCmd(dataSource):
    return formatCmd(BASE_REG + DATA_SOURCE_MUX_OFFSET, dataSource.value)

def setFIFOInputCmd(FIFOInput):
    global _FIFOInput
    _FIFOInput = FIFOInput
    return formatCmd(BASE_REG + FIFO_INPUT_MUX_OFFSET, FIFOInput.value)

def startCmd():
    return ELFS_LOCATION + 'startup_1000.elf\n'
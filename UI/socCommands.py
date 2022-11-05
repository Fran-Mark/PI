from enum import Enum

ELFS_LOCATION = '/mnt/currentVersions/'
BASE_REG = 0x43C3_0000
FIFO_INPUT_MUX_OFFSET = 0x4
DATA_SOURCE_MUX_OFFSET = 0x8
LOCAL_OSC_FREQ_SETTER_OFFSET = 0x34
BEAM_FREQ_SETTER_OFFSET = 0xC
BEAM_SELECTOR_OFFSET = 0x38



def axiWriteCmd(reg, data, includesReturn=True):
    cmd = ELFS_LOCATION + 'axi_rw_test.elf w {} {}'.format(reg, data)
    if includesReturn:
        cmd = cmd + '\n'
    return cmd

def axiReadCmd(reg, includesReturn=True):
    cmd = ELFS_LOCATION + 'axi_rw_test.elf r {}'.format(reg)
    if includesReturn:
        cmd = cmd + '\n'
    return cmd

def updateConf(field : str, value):
    #update field in registers.conf file
    with open('registers.conf', 'r') as file:
        data = file.readlines()
    for i in range(len(data)):
        if field in data[i]:
            data[i] = field + '=' + str(value) + '\n'
            break
    with open('registers.conf', 'w') as file:
        file.writelines(data)
    print('Updated ' + field + ' to ' + str(value))
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
    updateConf('dataSource', dataSource.value)
    return axiWriteCmd(hex(BASE_REG + DATA_SOURCE_MUX_OFFSET)[2:], dataSource.value)

def setFIFOInputCmd(FIFOInput):
    global _FIFOInput
    _FIFOInput = FIFOInput
    updateConf('FIFOInput', FIFOInput.value)
    return axiWriteCmd(hex(BASE_REG + FIFO_INPUT_MUX_OFFSET)[2:], FIFOInput.value)

def startCmd():
    return ELFS_LOCATION + 'startup.elf\n'

def launchAcqCmd():
    return ELFS_LOCATION + 'sist_adq.elf ' + ELFS_LOCATION + 'client_config\n'





def setBeamFreqCmd(beamNumber, freq : float):
    #freqs > a 436.5 son positivas => Necesitamos signo negativo (1)
    #freqs < a 436.5 son negativas => Necesitamos signo positivo (0)
    updateConf(f'beam{beamNumber}Freq', freq)
    if freq > 436.5:
        freqSign = 1
    else:
        freqSign = 0

    freqBB = abs(436.5 - freq)
    freqConf = abs(freqBB * 32 / 260.0 * 2**32)

    freqAbsValCmd = axiWriteCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + beamNumber * 8)[2:], hex(int(freqConf))[2:], includesReturn=False)
    freqSignCmd = axiWriteCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 4 + beamNumber * 8)[2:], int(freqSign))
    return freqAbsValCmd + " && " + freqSignCmd

def setLocalOscFreqCmd(freq : float):
    updateConf('localOscFreq', freq)
    freqConf = abs(freq * 4 * 2**32 / 260.0)
    return axiWriteCmd(hex(BASE_REG + LOCAL_OSC_FREQ_SETTER_OFFSET)[2:], hex(int(freqConf))[2:])

def selectBeamCmd(beamNumber):
    updateConf('activeBeam', beamNumber)
    return axiWriteCmd(hex(BASE_REG + BEAM_SELECTOR_OFFSET)[2:], hex(int(beamNumber))[2:])



def sendReadCmd():
    localOscReg = axiReadCmd(hex(BASE_REG + LOCAL_OSC_FREQ_SETTER_OFFSET)[2:], includesReturn=False)
    beam1FreqReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET)[2:], includesReturn=False)
    beam1SignReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 4)[2:], includesReturn=False)
    beam2FreqReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 8)[2:], includesReturn=False)
    beam2SignReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 12)[2:], includesReturn=False)
    beam3FreqReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 16)[2:], includesReturn=False)
    beam3SignReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 20)[2:], includesReturn=False)
    beam4FreqReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 24)[2:], includesReturn=False)
    beam4SignReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 28)[2:], includesReturn=False)
    beam5FreqReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 32)[2:], includesReturn=False)
    beam5SignReg = axiReadCmd(hex(BASE_REG + BEAM_FREQ_SETTER_OFFSET + 36)[2:], includesReturn=False)
    activeBeamReg = axiReadCmd(hex(BASE_REG + BEAM_SELECTOR_OFFSET)[2:])

    return localOscReg + " && " + beam1FreqReg + " && " + beam1SignReg + " && " + beam2FreqReg + " && " + beam2SignReg + " && " + beam3FreqReg + " && " + beam3SignReg + " && " + beam4FreqReg + " && " + beam4SignReg + " && " + beam5FreqReg + " && " + beam5SignReg + " && " + activeBeamReg

def decodeLocalOscFreq(data : str):
    return int(data, 16) * 260.0 / (4 * 2**32)

def decodeBeamFreq(data : float, sign : int):
    freqBB = int(data, 16) * 260.0 / (32 * 2**32)
    if sign == 1:
        freq = 436.5 + freqBB
    else:
        freq = 436.5 - freqBB
    return freq

# def decodeReading(rawText : str):
#     global configData
#     values = []
#     for line in rawText:
#         if line.startswith('Valor leido: '):
#             line = line[13:]
#             values.append(line)
#     print("Len: ", len(values))
#     if len(values) > 0:
#         configData = { 'localOscFreq' : decodeLocalOscFreq(values[0]),
#                     'beam1Freq' : decodeBeamFreq(values[1], values[2]),
#                     'beam2Freq' : decodeBeamFreq(values[3], values[4]),
#                     'beam3Freq' : decodeBeamFreq(values[5], values[6]),
#                     'beam4Freq' : decodeBeamFreq(values[7], values[8]),
#                     'beam5Freq' : decodeBeamFreq(values[9], values[10]),
#                     'activeBeam' : int(values[11], 16) }
#     else:
#         configData = { 'localOscFreq' : 0,
#             'beam1Freq' : 1,
#             'beam2Freq' : 0,
#             'beam3Freq' : 0,
#             'beam4Freq' : 0,
#             'beam5Freq' : 0,
#             'activeBeam' : 0 }

#     return configData


def readConfigData():
    #open registes.conf
    with open('registers.conf', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('FIFOInput'):
                fifoInput = FIFOInput(int(line.split('=')[1])).value
            elif line.startswith('dataSource'):
                dataSource = DataSource(int(line.split('=')[1])).value
            elif line.startswith('localOscFreq'):
                localOscFreq = float(line.split('=')[1])
            elif line.startswith('beam1Freq'):
                beam1Freq = float(line.split('=')[1])
            elif line.startswith('beam2Freq'):
                beam2Freq = float(line.split('=')[1])
            elif line.startswith('beam3Freq'):
                beam3Freq = float(line.split('=')[1])
            elif line.startswith('beam4Freq'):
                beam4Freq = float(line.split('=')[1])
            elif line.startswith('beam5Freq'):
                beam5Freq = float(line.split('=')[1])
            elif line.startswith('activeBeam'):
                activeBeam = int(line.split('=')[1])

    configData ={'fifoInput' : fifoInput,
                'dataSource' : dataSource,
                'localOscFreq' : localOscFreq,
                'beam1Freq' : beam1Freq,
                'beam2Freq' : beam2Freq,
                'beam3Freq' :  beam3Freq,
                'beam4Freq' : beam4Freq,
                'beam5Freq' : beam5Freq,
                'activeBeam' : activeBeam}

    return configData

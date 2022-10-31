from signal import pause
import socket
import time

import numpy as np

serverAddress = ("127.0.0.1", 7070)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

contador = np.int32(0)
fs = 32000
f = 1000
packet_size = 1472 #bytes

#Cada complex tiene 8 bytes y el /2 lo agrego para testeo del stream demux
#nValues = packet_size /8 /2 

nValues = 1000

while True:
    # Send one number at a time
    #x = contador.tobytes()

    # Send a packet of nValues
    # x = np.arange(contador * nValues, (contador + np.int32(1)) * nValues, dtype=np.int32)

    # print("Sending packet: ", contador, " with size: ", len(x)*4, " bytes")
    # sock.sendto(x, serverAddress)
    # contador += np.int32(1)
    # time.sleep(1)

    #Send packet with ones
    ones = np.ones(100, dtype=np.int32)
    x = np.arange(contador * nValues, (contador + np.int32(1)) * nValues, dtype=np.int32)
    x = np.concatenate((x, ones))
    print("Sending packet: ", contador, " with size: ", len(x)*4, " bytes")
    sock.sendto(x, serverAddress)
    contador += np.int32(1)
    #time.sleep(0.1)
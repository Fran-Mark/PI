from ctypes import sizeof
import socket
import time
from turtle import delay

import numpy as np

# A tuple with server ip and port

serverAddress = ("127.0.0.1", 7070)

# Create a datagram socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

contador = 0
fs = 32000
f = 1000
packet_size = 1472

nValues = packet_size/4

while True:
    # Send data
    n = np.arange(contador*nValues, (contador+1)*nValues)
    seno = 2**10*(np.sin(2*np.pi*f*n/fs))
    seno = seno.astype(np.int32)
    sock.sendto(seno, serverAddress)
    contador += 1
    time.sleep(0.1)
    
    # # Send data
    # seno = int(2**10*(np.sin(2*np.pi*f*contador/fs)))
    # contador += 1
    # #diez = 10
    # sock.sendto(seno.to_bytes(1472, 'little', signed=True), ("127.0.0.1",7070))
    # time.sleep(1/1000000.0)
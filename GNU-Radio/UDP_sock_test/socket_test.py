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
nValues = packet_size /8 /2 

contNValues = packet_size / 4

while True:
    # Send data
    n = np.arange(contador*nValues, (contador+1)*nValues)
    z = np.exp(1j*2*np.pi*f*n/fs)
    y = np.exp(1j*2*np.pi*f*3*n/fs)
    x = np.append(z,y)
    x = x.astype(np.complex64).tobytes()
    print(len(x))
    sock.sendto(x, serverAddress)
    #print("Sending packet: ", contador)
    contador += 1
    time.sleep(0.1)

    # x = np.sin(2*np.pi*f*n/fs)
    # data = x.astype(np.float32).tostring()
    # sent = sock.sendto(data, serverAddress)
    # n = np.arange(contador*contNValues, (contador+1)*contNValues)
    # cont = n.astype(np.int32)
    # c = cont.tobytes()
    # sent = sock.sendto(c, serverAddress)
    # print(cont)
    # time.sleep(1)
    # contador += 1
    #pause()
    
    # # Send data
    # seno = int(2**10*(np.sin(2*np.pi*f*contador/fs)))
    # contador += 1
    # #diez = 10
    # sock.sendto(seno.to_bytes(1472, 'little', signed=True), ("127.0.0.1",7070))
    # time.sleep(1/1000000.0)
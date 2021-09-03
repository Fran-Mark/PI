import numpy as np

#Velocidad de la luz en m/s
c = 3e8

class Coord:
    @staticmethod
    def polar(modulo, angulo):
        x = modulo*np.cos(angulo)
        z = modulo*np.sin(angulo)
        return Coord(x,z)

    def __init__(self, x, z):
        self.x = x
        self.z = z 
    
    def __repr__(self):
        return "x = " + str(self.x) + "\nz = " + str(self.z)

    def __sub__(self, punto):
        return Coord(self.x - punto.x, self.z - punto.z)

    def modulo(self):
        return np.sqrt(self.x**2 + self.z**2)

class Arreglo:
    def __init__(self, cantDeElementos, separacion):
        self.cantDeElementos = cantDeElementos
        self.separacion = separacion
        self.coordsAntena = [Coord(-i*separacion, 0) for i in range(cantDeElementos)]

    def calcularCoefs (self, anguloDeArribo):
        i = np.arange(self.cantDeElementos)
        return np.exp(-1j*2*np.pi*f*i*self.separacion*np.cos(anguloDeArribo)/c)


class Satelite:
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas

    def emitirSeñal(self, signal):
        self.signal = signal
        return

    def getSignalAt(self, coords, ruido = False, varianza = 1):
        ##Muestrea la señal con (o sin) ruido AWGN
        if hasattr(self, 'signal'):
            distanciaAlSatelite = (self.coordenadas - coords).modulo()
            if ruido:           
                return self.signal(distanciaAlSatelite) + varianza*np.random.standard_normal()
            return self.signal(distanciaAlSatelite)
        else:
            raise ValueError("El satélite no está emitiendo ninguna señal, usá el método Satelite.emitirSeñal(señal)")



#%% Simulación de arribo

#Parametros de la señal
f = 436.5e6 #436.5 MHz es la frec central de la banda UHF amateur
A = 10
signal = lambda dist : A*np.exp(1j*2*np.pi*f*dist/c)

#Parametros del arreglo y el satelite
separacion = 0.5 * c/f #Separamos los elementos media long de onda
cantDeElementos = 6
anguloDeArribo = np.deg2rad(30) #Angulo respecto al horizonte (medido en sentido antihorario con el origen usual)
alturaSatelite = 400e3 #400 km


satelite = Satelite(Coord.polar(alturaSatelite, anguloDeArribo))
arreglo = Arreglo(cantDeElementos, separacion)
coefs = arreglo.calcularCoefs(anguloDeArribo)

satelite.emitirSeñal(signal)
señalRecibida = [satelite.getSignalAt(arreglo.coordsAntena[i]) for i in range(cantDeElementos)]


señalFinal = sum(coefs*señalRecibida)


#%% Chequeo de coeficientes (solo sirve para ver si todo fue bien)
from cmath import polar as toPolar
señalReferencia = señalRecibida[0]
señalNormalizada = señalRecibida/señalReferencia
coefsPolares = [toPolar(coefs[i]) for i in range(cantDeElementos)]
variacionPolar = [toPolar(señalNormalizada[i]) for i in range(cantDeElementos)]
error = [abs(señalNormalizada[i] * coefs[i]) - 1 for i in range(cantDeElementos)]

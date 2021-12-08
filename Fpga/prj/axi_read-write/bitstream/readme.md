# Contador de 4 bits a 1 Hz

## Controles por AXI
Para comenzar a contar se deben escribir un 1 en los primeros dos registros, que corresponden al vadj_en (activa la tensión hacia los leds) y enable (habilita el contador).
Los registros 4 y 3 permiten cargar un número desde el registo y habilitar dicha carga, respectivamente.
El registro 5 es read-only y reporta en valor actual del contador

# UI

La UI se compondrá de 3 partes principales interconectadas:

## SoC Control

- **Init**:
  - SSH Connection
  - Seteo de tensiones
  - Reset de registros de configuración
- **Show status**:
  - Channel

    Channel number | Freq [MHz] | Link Status
    ---------------|------------|------------
    1              |436.95      |Up
    2              |437         |Down
    ...
- **Config**:
  - channel *\<num>* tune *\<freq>* tle_file *\<tle>*
  - set data_source *\<data_source>*
  - disable/enable filter *\<filter>*

## SDR Control

- **Show status**:
  - Freq detectada
  - Ángulo de arribo (diff con TLE)
  - Potencia recibida por antena
- **Calibrate**:
  - Calibración de potencia y fase para cada cadena de RF
  - Calibración de orientación del arreglo en elevación y acimut
- **Waterfall**:
  - Mostrar waterfall (desde GNU Radio) de lo que se detecta

## Server Control

- **Init**:
  - Correr el server.o
- **Show status**:

Client Number |Channel Number| Freq [MHz] | Status
--------------|--------------|------------|-------
1             |1             |436.95      |Processing
2             |2             |437         |Streaming
...

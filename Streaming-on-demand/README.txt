Crear un directorio build y correr cmake ..
Para compilar se necesita tener instalado GNU Radio (un software teleco). Si lo prefieren puedo pasarles la parte de GNU Radio ya compilada y ejecutarla con un execl (así lo hacía antes). De todas formas, haré la demostración en clase.

Breve explicación:
En el marco de mi proyecto integrador, hice un server capaz de atender a varios clientes simultáneamente. Los clientes piden información de un satélite en particular proveyendo sus TLEs (Two-Line Elements), y el server en base a eso puede determinar cuando será visible desde Argentina y a qué angulos en el cielo apuntar para verlo. También es necesario proveer la información de la frecuencia, ya que no viene dentro de los TLEs.
El server entonces espera a la próxima pasada del satélite y dispara la captura junto con el procesamiento y el streaming al cliente, todo de manera simultánea.
El cliente recibe la información del server y la almacena en un archivo

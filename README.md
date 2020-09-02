# pyreportntw

Este programa comprueba la conectividad hacia una dirección IP. En caso de que no se escribirá en un archivo CSV la fecha, hora, 
la ip de la maquina local y la ip destino.

## Requisitos
* Sistema operativo: **GNU/Linux**
* Tener instalado **python** version 3.5 o posteriores.
* Tener instalado la libreria de python **netifaces** `pip install netifaces`

## Setup
1. Abrir el sistema de tareas progradas de Linux: `crontab -e`
2. Añadir la tarea programada:
  * Opcion 1: Indicar solamente la ip destino y el archivo .csv se guarda en la carpeta *home* del usuario. `* * * * * /bin/python3 </path/to/pyreportntw.py> <ip_destino>` 
  * Opcion 2: Indicar la ip destino, la ruta de la carpeta donde se almacenará el fichero csv y el nombre del fichero csv. `* * * * * /bin/python3 </path/to/pyreportntw.py> <ip_destino> </path/to/the/folder/to/save> <namefile.csv>`

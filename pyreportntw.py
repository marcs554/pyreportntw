#!/bin/python3

import csv
from datetime import datetime
import os
import getpass
import netifaces as ni
import sys


"""
Esta aplicación esta diseñada con el proposito de monitorizar la conectividad de la red
para ello es preferible que la aplicación sea ejecutada por el cron (administrador regular 
de procesos en segundo plano de Linux) y que el firewall permita el trafico ICMP.
Si la aplicación detecta una caida de la conectividad escribirá en un archivo .csv la fecha 
y hora que se produjo el fallo así como la ip de origen y la ip destino.

---------------------------------------------------------------------------------------------

(Opción 1)
# m h  dom mon dow   command
* * * * *   /bin/python3 /path/to/pyreportntw.py <ip destino>

(Opción 2)
# m h  dom mon dow   command
* * * * *   /bin/python3 /path/to/pyreportntw.py <ip destino> </path/to/save_csv> <filename>
"""

class pyreportntw:
    __id_last = 0

    def __init__(self, dir_path="/home/" + getpass.getuser() + "/", file_name="pyreportntw"):
        """
        Constructor de la clase pyreportntw.

        Al llamar a la clase se guarda en variables: dia, mes, año, hora, min, ruta absoluta,
        nombre del fichero y la cabecera del documento csv.
        Despues se llama a la función __checkifexists() para comprobar si se creó o no el fichero
        csv.
        
        Parameters
        ----------
        dir_path : str
            Pasa por parametro la ruta absoluta donde se almacenará el fichero
            csv
        file_name : str
            Pasa por parametro el nombre del fichero .csv
        """

        self.dia = datetime.now().day
        self.mes = datetime.now().month
        self.anho = datetime.now().year
        self.hora = datetime.now().hour
        self.min = datetime.now().minute

        self.__main_path = dir_path
        self.__file_name = file_name + ".csv"
        self.__header = ('\'id\'', '\'fecha\'', '\'hora\'', '\'ip_origen\'' ,'\'ip_destino\'')

        self.__checkifexists()

    def __checkifexists(self):
        """
        Esta función se encarga de chequear si el archivo .csv existe.
        En caso de que no lo creara en la ruta que tenga designada en la variable: 
        self.main_path
        """

        if not os.path.exists(self.__main_path + self.__file_name):
            with open(self.__main_path + self.__file_name, 'w') as f:
                CSVWriter = csv.writer(f, delimiter=';')
                CSVWriter.writerow(self.__header)

    def chknetwork(self, destino):
        """
        Esta función se encarga de enviar un ping a la dirección ip que es
        pasada por parametro {destino}.
        Si el ping falla se añadirá una fila al archivo csv indicando la hora,
        fecha, ip origen y la ip destino.

        Si en la columna ip origen aparece una ip: 0.0.0.0 significa que la conexión dispositivo
        central (Switch, Router, etc...) no esta funcionando correctamente.

        Parameters
        ----------
        destino : str
            Ip destino a la cual se le enviará un ping para hacer la prueba de conectividad.
        """

        def writeCSV():
            """
            Esta función se encargará de escribir en el archivo csv
            1- Comprueba el ultimo digito de la columna id. Si existe toma el ultimo digito y lo incrementa
                uno más. En caso que no empieza por el valor 0.
            2- Añade una nueva fila en el archivo csv con los siguientes datos:
                "id, fecha, hora, ip origen, ip destino".
            """

            fila = []

            with open(self.__main_path + self.__file_name, 'r') as fr:
                get_info_csv = csv.reader(fr, delimiter=';')
               
                for i in get_info_csv:
                    fila = i

                if fila[0].isdigit(): self.__id_last = int(fila[0]) + 1
            
            with open(self.__main_path + self.__file_name, 'a') as fa:
                CSVAppend = csv.writer(fa, delimiter=';', quotechar='\n')
                CSVAppend.writerow([self.__id_last, f'"{self.dia}-{self.mes}-{self.anho}"', 
                                        f'"{self.hora}:{self.min}"', f'"{ip_local}"', f'"{destino}"'])

        """Si el equipo no tiene una ip fija o dada por un DHCP saltará una excepción y en ella 
        se añadira como ip origen: 0.0.0.0"""
        try:
            ip_local = ni.ifaddresses(ni.interfaces()[1])[ni.AF_INET][0]["addr"]
            
            if os.system(f"ping -c 1 {destino}") is not 0: writeCSV()
                
        except Exception:
            ip_local = "0.0.0.0"
            writeCSV()


if __name__ == "__main__":
    #Comprueba el numero de parametros pasados
    try:
        rg = pyreportntw(sys.argv[2], sys.argv[3])
        rg.chknetwork(sys.argv[1])
    except:
        rg = pyreportntw()
        rg.chknetwork(sys.argv[1])

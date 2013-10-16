#!/bin/bash

echo "Ejecutando pruebas automáticas"
echo "################################"
echo "#          Prueba1             #"
echo "################################"
./tdatp1.py 2 grafoej3

echo -e "Presione enter para la siguiente prueba\n"
read opcion

echo "################################"
echo "#          Prueba2             #"
echo "################################"
./tdatp1.py 4 grafoej3

echo  -e "Presione enter para la siguiente prueba\n"
read opcion

echo "################################"
echo "#          Prueba3             #"
echo "################################"
./tdatp1.py 3 grafoej1

echo -e "Presione enter para la siguiente prueba\n"
read opcion

echo "################################"
echo "#          Prueba4             #"
echo "################################"
./tdatp1.py 40 grafoej1

echo -e "Presione enter para la siguiente prueba\n"
read opcion

echo "################################"
echo "#          Prueba5             #"
echo "################################"
./tdatp1.py 6 grafoej2

echo -e "Presione enter para la siguiente prueba\n"
read opcion

echo "################################"
echo "#          Prueba6             #"
echo "################################"
./tdatp1.py 3 grafoej2
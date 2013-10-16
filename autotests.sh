#!/bin/bash

count=1

test(){
echo "################################"
echo "#          Prueba$count        #"
echo "################################"

./tdatp1.py $1 grafoej$2
count=$((count+1))
echo -e "Presione enter para la siguiente prueba\n"
read opcion
}

test 2 3
test 4 3
test 3 1
test 40 1
test 6 2 
test 3 2

echo "No hay más pruebas"
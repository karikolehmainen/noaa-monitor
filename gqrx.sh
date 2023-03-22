#!/bin/bash
gqrx -c $1 &
sleep 5
gqrxWindow=$(xdotool search --name "Gqrx()")
# IFS=' ' read -r -a array <<< "$gqrxWindow"
array=($gqrxWindow)
echo $gqrxWindow
echo "${array[@]}"
echo "${#array[@]}"
xdotool windowactivate --sync ${array[${#array[@]}-1]} key ctrl+d

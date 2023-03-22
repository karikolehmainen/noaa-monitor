#!/bin/bash
gqrxWindow=$(xdotool search --name "Gqrx()")
array=($gqrxWindow)
xdotool windowactivate --sync ${array[${#array[@]}-1]} key ctrl+q

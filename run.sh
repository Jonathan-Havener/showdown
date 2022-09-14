#!/bin/bash
declare -a TYPES
TYPES=(bug dark dragon electric fairy fighting fire flying ghost grass ground ice normal poison psychic rock steel water)
now=`date +"%Y-%m-%d_%H-%M-%S"`
for i in "${TYPES[@]}"
do
    python run.py "$i" > logs/"$i"/"${now}".txt &
done
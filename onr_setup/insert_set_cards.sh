#!/bin/bash

FILENAME="onr_out/onr-base.edn"
FILES="onr_out/cards/*.edn"

counter=700001
position=1
echo -n '['
for f in $FILES
do
    idline=$(grep ':id' $f)
    echo ${idline/":id"/"{:card-id"}
    echo ' :code "'$counter'"'
    echo ' :illustrator "Unknown (will add later)"'
    echo ' :position '$position
    echo ' :quantity 99'
    echo ' :set-id "onr-base"}'

    counter=$((counter+1))
    position=$((position+1))
done
echo ']'
## format:
## {:card-id "chrysalis"
##  :code "11013"
##  :illustrator "Donald Crank"
##  :position 13
##  :quantity 3
##  :set-id "23-seconds"}

#!/bin/bash

FILENAME="onr_out/onr-base.edn"
FILES="onr_out/cards/*.edn"

counter=700001
position=1
echo -n '['
for f in $FILES
do
    idline=$(grep ':id' $f)
    smallid=${idline/" :id "/""}
    smallid=${smallid%?}
    smallid=${smallid:1}

    #use smallid to get the artist information
    artist=`echo $smallid | python3 onr_setup/artist_lookup.py`
#    echo "$artist"
    echo ${idline/":id"/"{:card-id"}
    echo ' :code "'$counter'"'
    echo ' :illustrator "'$artist'"'
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

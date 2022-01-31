#!/bin/bash

# replaces the factions.edn file with one that contains the ONR factions

if ! grep -q "onr_" "edn/factions.edn"; then
    echo "didn't find ONR entries - altering factions.edn file"
    FILE=$(<edn/factions.edn)
    FILE=${FILE%?}
    APPEND=`cat onr_setup/factions.edn`
    OUTPUT=$FILE$APPEND
    echo "$OUTPUT" > "edn/factions.edn"
else
    echo "ONR factions already exist"
fi

#!/bin/bash

# replaces the factions.edn file with one that contains the ONR factions

if ! grep -q "onr-" "edn/cycles.edn"; then
    echo "didn't find ONR entries - altering cycles.edn file"
    FILE=`cat edn/cycles.edn`
    FILE=${FILE%?}
    APPEND=`cat onr_setup/cycles.edn`
    OUTPUT=$FILE$APPEND
    echo $OUTPUT > "edn/cycles.edn"
else
    echo "ONR cycles already exist"
fi

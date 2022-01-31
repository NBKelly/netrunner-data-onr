#!/bin/bash

# replaces the factions.edn file with one that contains the ONR factions

if ! grep -q "onr-" "edn/sets.edn"; then
    echo "didn't find ONR entries - altering sets.edn file"
    FILE=$(<edn/sets.edn)
    FILE=${FILE%?}
    APPEND=`cat onr_setup/sets.edn`
    OUTPUT=$FILE$APPEND']'
    echo "$OUTPUT" > "edn/sets.edn"
else
    echo "ONR sets already exist"
fi

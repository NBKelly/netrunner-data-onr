#!/bin/bash

# replaces the factions.edn file with one that contains the ONR factions

if ! grep -q "onr_" "edn/factions.edn"; then
    echo "didn't find ONR entries - replacing factions.edn file"
    cp "onr_setup/factions.edn" "edn/factions.edn"
else
    echo "ONR factions already exist"
fi

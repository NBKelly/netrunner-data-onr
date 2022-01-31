#!/bin/bash

#If we haven't scraped the card data from emergency shutdown, do that
if test -f "onr_out/stage_one.txt"; then
    echo "Using cached data from Emergency Shutdown"
else
    mkdir onr_out
    echo "fetching from Emergency Shutdown"
    python3 onr_setup/scrape.py > onr_out/stage_one.txt
fi

#check the cycles entry
onr_setup/insert_cycles.sh

#check the factions entry
onr_setup/insert_factions.sh

#check the sets entry
onr_setup/insert_sets.sh

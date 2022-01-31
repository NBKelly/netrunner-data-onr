#!/bin/bash

#If we haven't scraped the card data from emergency shutdown, do that
if test -f "onr_out/stage_one.txt"; then
    echo "Using cached data from Emergency Shutdown"
else
    mkdir onr_out
    echo "fetching from Emergency Shutdown"
    python3 scrape.py > onr_out/stage_one.txt
fi
   

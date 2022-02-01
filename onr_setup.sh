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

#make the new cards
echo "creating card entries"
python3 onr_setup/convert.py onr_out/stage_one.txt > onr_out/onr_subtypes.edn
cp onr_setup/onr-braniac.edn onr_out/cards/.
cp onr_setup/onr-friend-corp.edn onr_out/cards/.

#create the set-cards entry and copy it over
echo "associating sets and finding artist information"
onr_setup/insert_set_cards.sh > "onr_out/onr-base.edn"
cp onr_out/onr-base.edn edn/set-cards/.

#copy over the new cards
cp onr_out/cards/*.edn edn/cards/.

#copy over all the onr subtypes
onr_setup/insert_subtypes.sh

#scrape all the images
onr_setup/image_fetch.sh
mogrify -format png onr_out/images/*.jpg

#compile a new raw data file
clj -X nr-data.combine/combine-for-jnet

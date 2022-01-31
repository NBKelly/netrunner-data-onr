# Goal

Convert the ONR cards into a format usable by Jinteki. 

The cards will be placed under the factions "onr_corp" and "onr_runner", and all the card titles will be prefaced by "onr_" to maintain compatability.

Types will be mapped to the android: netrunner counterparts, and two new IDs will be added.

### Workflow

* ~~scrape data from emergency shutdown~~
* scrape card images from emergency shutdown
* seperate cards by set
* seperate cards within set by type
* map card representations into identical formats/types as jinteki representations
* ~~insert onr factions into data~~
* ~~insert onr cycles into data~~
* add card entries in edn/set-cards
* add the actual card entries 
* automate all of this so that it can be realistically done on any release of netrunner-data

To convert, use the `onr_setup.sh` script.

To figure out how to use the data, refer to https://github.com/mtgred/netrunner/issues/6202

# netrunner-cards-edn

The clojure app is internal only, p much. If you want the edn data, look under `/edn`.
This app only transforms that data into a jnet-usable format.

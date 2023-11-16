#!/bin/bash

subtypes_file=`cat edn/subtypes.edn`
subtypes_file=${subtypes_file%?}
addendum=`cat onr_out/onr_subtypes.edn`
res="$subtypes_file
$addendum]"
echo "$res" > "edn/subtypes.edn"


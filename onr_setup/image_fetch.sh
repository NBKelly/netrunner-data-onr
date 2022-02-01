#!/bin/bash

mkdir "onr_out/images"
while read p; do
    left=${p% *}
    right=${p:6}
    echo "$right"
    if [ "$right" = "unknown" ]; then
	echo "missing image for $left" > "onr_out/image_$left.txt"
    else
	#echo "fetching $right..."
	wget "$right" -O "onr_out/images/$left.jpg" > /dev/null 2>&1 &
    fi    
done <onr_out/image_urls.txt

#wait for everything to finish
FAIL=0
for job in `jobs -p`
do
    wait $job || let "FAIL+=1"
done

echo "done"

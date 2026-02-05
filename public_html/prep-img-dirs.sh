#!/bin/sh

JSFILE="./images_steward.js"

IMGDIR1="./images/gallery_steward/"
echo "var stewardImages = [" > $JSFILE
for f in $(ls $IMGDIR1); do echo "\"$f\"," >> $JSFILE; done
echo "]" >> $JSFILE

echo "" >> $JSFILE

IMGDIR2="./images/gallery_gradlife/"
echo "var gradlifeImages = [" >> $JSFILE
for f in $(ls $IMGDIR2); do echo "\"$f\"," >> $JSFILE; done
echo "]" >> $JSFILE


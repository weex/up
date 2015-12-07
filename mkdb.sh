#!/bin/sh

SN=up
FN=$SN.db

if [ -f $FN ]
then
	echo Database $FN for $SN already exists.  Will not overwrite
	exit 1
fi
sqlite3 $FN < $SN.schema

cat $SN-test.schema
echo
read -p "Add above test endpoints? [y/N]" -n 1 -r
echo   
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sqlite3 $FN < $SN-test.schema
fi

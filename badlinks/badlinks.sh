#!/usr/bin/env bash

for i in $(find -L $1 -mtime +7); # File is older then 7 days
do
	if [ -L $i ]; then # File is symbolic link
		if [ ! -e $i ]; then # File does not exist
			echo $i
		fi
	fi
done
#!/bin/bash


if [ $# -eq 0 ]
		then echo "Upload file"
		exit 0
fi

./script_1.sh
./script_2.sh $@

#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Incorrect number of arguments provided. Received $# instead of 1."
    exit 1
fi

DIR=$1

if [ ! -d "$DIR" ]; then
    echo "'$DIR' is not a valid directory."
    exit 1
fi

EMPTY_FILES=$(find "$DIR" -type f -empty)

echo "Deleting empty files:"
echo "$EMPTY_FILES"
find "$DIR" -type f -empty -delete

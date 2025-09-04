#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Incorrect number of arguments provided. Received $# instead of 2."
    exit 1
fi

FILENAME=$1
WORD=$2

if [ ! -f "$FILENAME" ]; then
    echo "File '$FILENAME' is not found. Please check that requested file exist."
    exit 1
fi

COUNT=$(grep -o -i -w "$WORD" "$FILENAME" | wc -l)

echo "The word '$WORD' appears $COUNT times in '$FILENAME'."
#!/bin/bash
CURRENT_TIME_IN_MINUTES=$((10#$(date +%H) * 60 + 10#$(date +%M)))
END_TIME_IN_MINUTES=1080

if [ "$CURRENT_TIME_IN_MINUTES" -lt "$END_TIME_IN_MINUTES" ]; then
    REMAINING_TIME_IN_MINUTES=$((END_TIME_IN_MINUTES - CURRENT_TIME_IN_MINUTES))
    HOURS_LEFT=$((REMAINING_TIME_IN_MINUTES / 60))
    MINUTES_LEFT=$((REMAINING_TIME_IN_MINUTES % 60))
    echo "Current time: $(date +%H:%M). Work day ends after $HOURS_LEFT hours and $MINUTES_LEFT minutes."
else
    echo "Current time: $(date +%H:%M). Work day has already ended."
fi
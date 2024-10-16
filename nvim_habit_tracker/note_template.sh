#!/bin/bash
habit_file="/Volumes/notes/habit_tracker.txt"

start_date="30/09/2024"
current_date=$(date +"%s")
start_date_sec=$(date -j -f "%d/%m/%Y" "$start_date" +"%s")
diff_sec=$((current_date - start_date_sec))
diff_days=$((diff_sec / 86400))

week=$((diff_days / 7 + 1))
day=$((diff_days % 7 + 1))

echo "# Week $week, Day $day"
echo "*Daily highlight: ()*"
echo
echo "---"

echo "Did I read yesterday? ()"

echo "Did I meditate yesterday? ()"

echo "Did I exercise yesterday? ()"
echo
echo "Did I eat as expected yesterday? ()"
echo

echo "---"

echo "If I died yesterday, would I have been proud of my last day? If not, think of the reason why. ()"
echo

# Curls a dadjoke
echo "---"
echo "**Daily dadjoke:**"
echo
echo "$(curl -s -H "Accept: text/plain" https://icanhazdadjoke.com/)"
echo
echo "---"

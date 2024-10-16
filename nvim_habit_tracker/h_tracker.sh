#!/bin/bash

habits=("Journal" "Meditate" "Read" "Exercise" "testing")
daily_notes_location="/Volumes/notes/test/"

start_date="30/09/2024"
current_date=$(date +"%s")
start_date_sec=$(date -j -f "%d/%m/%Y" "$start_date" +"%s")
diff_sec=$((current_date - start_date_sec))
diff_days=$((diff_sec / 86400))

week=$((diff_days / 7 + 1))
day=$((diff_days % 7 + 1))

current_file_path=$(pbpaste)
current_file=$(echo "$current_file_path" | awk -F'/' '{print $NF}')
base_name="${current_file%.md}"

# Handle the edge case where the current file is 1.md
if [ "$base_name" -eq 1 ]; then
  previous_file="1.md" # or some default behavior like skipping this step
else
  previous_file=$((base_name - 1)).md
fi

habit_file="/Volumes/notes/habit_tracker.txt"
habit_to_increment="Meditate" # Could be passed as an argument or dynamically determined
temp_file=$(mktemp)

# Read through the habit tracker file and increment the streak for the specified habit
while read -r habit streak; do
  if [ "$habit" = "$habit_to_increment" ]; then
    # Increment the streak by 1
    new_streak=$((streak + 1))
    echo "$habit $new_streak" >>"$temp_file"
  else
    # Leave other habits unchanged
    echo "$habit $streak" >>"$temp_file"
  fi
done <"$habit_file"

# Replace the original file with the updated file
mv "$temp_file" "$habit_file"

echo "Updated the streak for $habit_to_increment."

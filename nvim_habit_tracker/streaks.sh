habit_file="/Volumes/notes/habit_tracker.txt"
habits=("meditate" "exercise" "read")

current_file_path=$(pbpaste)
current_file=$(echo "$current_file_path" | awk -F'/' '{print $NF}')
base_name="${current_file%.md}"

for HABIT in "${habits[@]}"; do
  # Check if the habit was done yesterday
  if grep -q "$HABIT yesterday? (x)" "$current_file_path"; then
    awk -v habit="$HABIT" 'BEGIN {OFS=FS=" "} {if ($1 == habit) $2 = $2 + 1} 1' $habit_file >temp.txt && mv temp.txt $habit_file
  else
    echo "$HABIT not done yesterday, resetting streak."
    awk -v habit="$HABIT" 'BEGIN {OFS=FS=" "} {if ($1 == habit) $2 = 0} 1' $habit_file >temp.txt && mv temp.txt $habit_file
  fi
done

echo "## Streaks:"
echo
while read -r line; do
  habit=$(echo "$line" | awk '{print $1}')
  streak=$(echo "$line" | awk '{print $2}')

  echo "- $habit"
  echo "  - $streak-day streak"
done <"$habit_file"

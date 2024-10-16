#!/bin/bash
# Set the base path for the cowformula project
cowformula_path="$HOME/Documents/GitHub/one_project_per_week/cowformula"

# Checks if the user wants to display an image of the formula
if [ "$1" == "-i" ]; then
  eog "$cowformula_path/images/$(ls $cowformula_path/previous_cow/)" &
  exit 0
fi

if [ ! -d "$cowformula_path/previous_cow" ]; then
  echo "Directory 'previous_cow' does not exist. Creating..."
  mkdir "$cowformula_path/previous_cow"
fi

if [ -n "$(ls -A $cowformula_path/previous_cow/)" ]; then
  rm "$cowformula_path/previous_cow/"*
fi

tags=("-b" "-d" "-g" "-p" "-s" "-t" "-w" "-y")
num_tags=${#tags[@]}
random_index=$((RANDOM % num_tags))
random_tag=${tags[random_index]}

filename="$cowformula_path/formulas.txt"
total_lines=$(wc -l <"$filename")
random_line=$((RANDOM % total_lines + 1))

cowline=$(sed -n "${random_line}p" "$filename")
img_name=$(echo "$cowline" | awk '{print $1}')
touch "$cowformula_path/previous_cow/$img_name.png"
img_name="$cowformula_path/images/${img_name}.png"
cowsay -W 1000 $random_tag "$cowline"

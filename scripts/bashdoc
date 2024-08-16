#!/usr/bin/env bash
#
# Prints out the top block comment of a script file

# Check if a file is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
  echo "File not found!"
  exit 1
fi

# Read the file line by line
while IFS= read -r line; do
  # If the line starts with '#', print it
  if [[ $line =~ ^# ]]; then
    echo "$line"
  else
    # Stop reading if we encounter a line that doesn't start with '#'
    break
  fi
done < "$1"

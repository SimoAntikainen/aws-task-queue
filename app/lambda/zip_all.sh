#!/bin/bash
# This script creates an individual ZIP file for each Python (.py) file in the current directory,
# naming the zip file with the base name and a .zip extension (e.g., example.py -> example.zip).

# Enable nullglob so that the loop doesn't execute with the literal pattern if no .py files are present.
shopt -s nullglob

for file in *.py; do
  # Check if the item is a regular file
  if [ -f "$file" ]; then
    # Remove the .py extension and add .zip
    zip_file="${file%.py}.zip"
    echo "Zipping $file into $zip_file"
    zip "$zip_file" "$file"
  fi
done
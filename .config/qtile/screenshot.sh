#!/bin/bash

# Define directories and filenames
SCREENSHOT_DIR="$HOME/Pictures/screenshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILE_PATH="$SCREENSHOT_DIR/screenshot_$TIMESTAMP.png"

# Create directory if it doesn't exist
mkdir -p "$SCREENSHOT_DIR"

# Take screenshot
maim -s "$FILE_PATH"

# Copy screenshot to clipboard
xclip -selection clipboard -t image/png -i "$FILE_PATH"


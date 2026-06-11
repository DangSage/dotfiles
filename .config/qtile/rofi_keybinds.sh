#!/bin/bash

# Extract keybindings from qtile config and display in rofi
config_file="$HOME/.config/qtile/config.py"

# Parse the keymap dictionary from config.py and format for rofi
keybindings=$(python3 << 'EOF'
import re

config_file = "/home/khai/.config/qtile/config.py"

with open(config_file, 'r') as f:
    content = f.read()

# Extract the keymap dictionary
keymap_match = re.search(r'keymap\s*=\s*{(.*?)\n}', content, re.DOTALL)

if keymap_match:
    keymap_content = keymap_match.group(1)

    # Parse key-value pairs
    pattern = r"'([^']+)':\s*\([^,]+,\s*\"([^\"]+)\"\)"
    matches = re.findall(pattern, keymap_content)

    # Format for rofi display
    max_key_len = max(len(key) for key, _ in matches) if matches else 0

    for key, desc in matches:
        # Clean up the key representation
        clean_key = key.replace('M-', 'Mod+').replace('A-', 'Alt+').replace('S-', 'Shift+').replace('C-', 'Ctrl+')
        clean_key = clean_key.replace('<', '').replace('>', '')
        print(f"{clean_key:<20} {desc}")

EOF
)

# Display in rofi
echo "$keybindings" | rofi -dmenu -i -p "Keybindings" -theme-str '
window {
    background-color: #303030FF;
    border:           0;
    padding:          3;
    width:            1000;
    border-color:     #72D5A3;
}
mainbox {
    border:  1;
    padding: 10;
    border-color: #72D5A3;
}
listview {
    lines: 20;
    spacing: 2px;
    padding: 2px 10px 0px;
}
element-text {
    font: "Hack Nerd Font Mono Regular 10";
}
'

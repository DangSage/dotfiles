#!/bin/bash

# Define the options with icons
options=" Shutdown\n Reboot\n Suspend\n Logout"

# Show the options using rofi with custom appearance
selected_option=$(echo -e "$options" | rofi -dmenu -i -p "Power Menu" -theme-str '
window {
    background-color: #000000;
    border:           0;
    padding:          3;
    width:            300;
}
mainbox {
    border:  1;
    padding: 10;
    border-color: @red;
}
listview {
    lines: 4;
    spacing: 5px;
    padding: 2px 10px 0px;
}
element-text {
    font: "Caskaydia Cove Nerd Font Mono SemiLight 15";
}
')

# Handle the selected option
case "$selected_option" in
    *Shutdown)
        systemctl poweroff
        ;;
    *Reboot)
        systemctl reboot
        ;;
    *Suspend)
        systemctl suspend
        ;;
    *Logout)
        qtile cmd-obj -o cmd -f shutdown
        ;;
    *)
        echo "No valid option selected"
        ;;
esac

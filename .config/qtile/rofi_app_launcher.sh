#!/bin/bash

# Simple rofi app launcher with green borders
rofi -show drun -theme-str '
window {
    background-color: #303030FF;
    border:           0;
    padding:          3;
    width:            500;
    border-color:     #72D5A3;
}
mainbox {
    border:  1;
    padding: 10;
    border-color: #72D5A3;
}
'

local interface = io.popen("ip route get 8.8.8.8 | awk '{print $5}'"):read("*a"):gsub("%s+", "")

conky.text = conky.text .. [[
${color #ec93d3}󱚶  Networking ${hr 1}$color
    ${color #aaaaaa}Interface: $color${alignr} ]] .. interface .. [[${if_match "${exec cat /sys/class/net/]] .. interface .. [[/operstate}" == "up"} ${color FFFFFF}ONLINE${else}${color red}OFFLINE${endif}$color
    ${color #aaaaaa}Connected to: $color${alignr} ${execi 5 iwgetid -r}
        ${color #aaaaaa}MAC Address: $color${alignr} ${execi 5 cat /sys/class/net/]] .. interface .. [[/address}
        ${color #aaaaaa}Local IP: $color${alignr} ${addr ]] .. interface .. [[}
        ${color #aaaaaa}Public IP: $color${alignr} ${execi 600 wget http://ipinfo.io/ip -qO -}

    Signal Strength: $color${alignr} ${execi 5 iwconfig ]] .. interface .. [[ | awk '/Link Quality/{split($2,a,"-|/");print int((a[2]/a[3])*100)"%"}'}$alignr ${tcp_portmon 1 65535 count} Connections
        ${color #aaaaaa}Ping to 192.168.1.1: $alignr ${texeci 15 output=$(ping -c 10 192.168.1.1); avg=$(printf "%0.1f" `echo $output | awk -F '/' 'END {print $5}'` | sed 's/,/./'); mdev=$(printf "%0.1f" `echo $output | awk -F '/' 'END {print $7}' | sed 's/ .*//'` | sed 's/,/./'); echo $avg ± $mdev ms}
        ${color #aaaaaa}Ping to 8.8.8.8: $alignr ${texeci 15 output=$(ping -c 10 8.8.8.8); avg=$(printf "%0.1f" `echo $output | awk -F '/' 'END {print $5}'` | sed 's/,/./'); mdev=$(printf "%0.1f" `echo $output | awk -F '/' 'END {print $7}' | sed 's/ .*//'` | sed 's/,/./'); echo $avg ± $mdev ms}

    ${color #ec93d3} Down: ${downspeed ]] .. interface .. [[} / s ${alignr} ${color #ec93d3} Up: ${upspeed ]] .. interface .. [[} / s$color
    ${color #aaaaaa}${downspeedgraph ]] .. interface .. [[ 25,200 ff00ff ff00ff} ${alignr}${upspeedgraph ]] .. interface .. [[ 25,200 ff00ff ff00ff}
    ${color #aaaaaa}Inbound Packets: ${tcp_portmon 1 65535 count} ${alignr} Outbound Packets: ${tcp_portmon 1 65535 count}

]]
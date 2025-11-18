-- Detect active network interface
local interface = io.popen("ip route get 8.8.8.8 2>/dev/null | awk '{print $5; exit}'"):read("*a"):gsub("%s+", "")
if interface == "" then
    interface = "wlan0"  -- fallback to default wireless interface
end

conky = conky or {}
conky.text = conky.text or ""

conky.text = conky.text .. [[
${color #ec93d3}󱚶  Networking ${hr 1}$color
    ${color #aaaaaa}Interface: $color]] .. interface .. [[ ${if_up ]] .. interface .. [[}${color FFFFFF}ONLINE${else}${color red}OFFLINE${endif}$color
    ${if_up ]] .. interface .. [[}${color #aaaaaa}Connected to: $color${alignr}${wireless_essid ]] .. interface .. [[}
        ${color #aaaaaa}Signal Strength: $color${alignr}${wireless_link_qual_perc ]] .. interface .. [[}%
        ${color #aaaaaa}MAC Address: $color${alignr}${execi 60 cat /sys/class/net/]] .. interface .. [[/address 2>/dev/null || echo "N/A"}
        ${color #aaaaaa}Local IP: $color${alignr}${addr ]] .. interface .. [[}
        ${color #aaaaaa}Public IP: $color${alignr}${execi 600 wget -qO- http://ipinfo.io/ip 2>/dev/null || echo "N/A"}

    ${color #ec93d3} Down: ${downspeed ]] .. interface .. [[}/s ${alignr} ${color #ec93d3} Up: ${upspeed ]] .. interface .. [[}/s$color
    ${color #aaaaaa}${downspeedgraph ]] .. interface .. [[ 25,200 ec93d3 ec93d3} ${alignr}${upspeedgraph ]] .. interface .. [[ 25,200 ec93d3 ec93d3}
    ${color #aaaaaa}Total Down: ${totaldown ]] .. interface .. [[} ${alignr}Total Up: ${totalup ]] .. interface .. [[}${endif}

]]

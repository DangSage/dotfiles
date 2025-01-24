conky.text = conky.text .. [[
${color #72d5a3}  CPU Usage:$color $cpu% ${color #72d5a3}${cpubar 4}$color
    ${color #aaaaaa}Processes:$color $processes ${alignr}${color #aaaaaa}Running:$color $running_processes
    ${color #aaaaaa}Threads:$color $threads ${alignr}${color #aaaaaa}Load Average:$color $loadavg
    ${color #aaaaaa}CPU Temp:$color ${alignr}${exec sensors|grep 'Package id 0'|awk '{print $4}'}
    
    ${color #aaaaaa}Core 1: ${if_match ${freq 1}<1000} ${endif}${freq 1} MHz - ${cpu cpu1}% ${alignr}Temp: $color ${exec sensors|grep 'Core 0'|awk '{print $3}'}
    ${color #aaaaaa}Core 2: ${if_match ${freq 2}<1000} ${endif}${freq 2} MHz - ${cpu cpu2}% ${alignr}Temp: $color ${exec sensors|grep 'Core 1'|awk '{print $3}'}
    ${color #aaaaaa}Core 3: ${if_match ${freq 3}<1000} ${endif}${freq 3} MHz - ${cpu cpu3}% ${alignr}Temp: $color ${exec sensors|grep 'Core 2'|awk '{print $3}'}
    ${color #aaaaaa}Core 4: ${if_match ${freq 4}<1000} ${endif}${freq 4} MHz - ${cpu cpu4}% ${alignr}Temp: $color ${exec sensors|grep 'Core 3'|awk '{print $3}'}
]]
conky.text = conky.text .. [[
${color #72d5a3}  CPU Usage:$color $cpu% ${color #72d5a3}${cpubar 4}$color
    ${color #aaaaaa}Processes:$color $processes ${alignr}${color #aaaaaa}Running:$color $running_processes
    ${color #aaaaaa}Threads:$color $threads ${alignr}${color #aaaaaa}Load Average:$color $loadavg
    ${color #aaaaaa}CPU Temp:$color ${alignr}${exec sensors|grep 'Package id 0'|awk '{print $4}'}

]]
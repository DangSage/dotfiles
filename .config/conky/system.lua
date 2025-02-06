conky.text = conky.text .. [[
${color #aaaaaa}  Machine:$color ${execi 1000 whoami}@${nodename}  ${alignr}${color #aaaaaa}Uptime:$color ${color #94bff3}$uptime$color
${color #aaaaaa}  OS:$color ${execi 1000 . /etc/os-release; echo $NAME $VERSION}
${color #aaaaaa}Kernel:$color $sysname $kernel $machine
${color #aaaaaa}CPU:$color ${execi 86400 cat /proc/cpuinfo | grep 'model name' | uniq | sed 's/model name\t: //'}
${if_existing /proc/driver/nvidia/version}${color #aaaaaa}GPU:$color ${execi 1000 nvidia-smi --query-gpu=gpu_name --format=csv,noheader,nounits}${endif}
$hr
${color #93e0e3}RAM Usage:$color $mem/$memmax - ${color #93e0e3}$memperc% ${membar 4}$color
    ${color #aaaaaa}Name${alignr}PID   MEM%
    ${top_mem name 1} ${alignr}${top_mem pid 1} ${top_mem mem 1}
    ${top_mem name 2} ${alignr}${top_mem pid 2} ${top_mem mem 2}
    ${top_mem name 3} ${alignr}${top_mem pid 3} ${top_mem mem 3}

]]
-- detect storage devices and display their usageoc

local conky = conky or {}

conky.text = conky.text .. [[
${color #dfaf8f}  File systems ${hr 1}
    /    $color${fs_used /}/${fs_size /} ${color #dfaf8f}${fs_bar 6 /}
    ${color #dfaf8f}Home $color${fs_used /home}/${fs_size /home} ${color #dfaf8f}${fs_bar 6 /home}$color
]]
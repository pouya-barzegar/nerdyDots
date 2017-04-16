#!/bin/bash

# Description:
# for any user with i3 or other WMs
# that have problem  with keyboard layout,
# mouse scrolling,specially on thinkpads without touchpads
# or want to use another fast & easy way 
# around the extensions, plugins,... ;)

# Setting the keyboard layout
setxkbmap 'dvorak,ir'
# Setting a shortcut for switching between layouts
setxkbmap -option 'grp:shifts_toggle'

# keyboard delay for repeating.
xset r rate 200 20
xset b off
xset m 40

# Changing the mouse speed by modifying its matrix XD
#just for thinkpads:
xinput set-prop 10 139 2.700000, 0.000000, 0.000000, 0.000000, 2.700000, 0.000000, 0.000000, 0.000000, 1.000000

# Only for vim users
setxkbmap -option 'caps:swapescape'

#not to forget:

#for configuring x11 lightdm keymap
localectl set-x11-keymap dvorak

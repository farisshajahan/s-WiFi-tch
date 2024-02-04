To upload files from system to chip flash, use ampy after flashing micropython
`ampy -p /dev/cu.usbserial-10 put <filename> <path-on-device>`
<path-on-device> is optional and will default to root path /

To connect to serial port, find out baud rate and use screen command
`screen /dev/cu.usbserial-10 <baud rate>`
Baud rate is usually 115200 but depends on what you set it to
Ctrl A + Ctrl \ - kill all screen sessions
Ctrl A + D to detach
Ctrl A + K to kill current session
`screen -r` to reattach to detached session

To find IP of the chip, use nmap
`nmap <network-address>/<subnet-mask-bits>`
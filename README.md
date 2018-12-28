# Completely random openvpn autoconnect!

Randomly selects from list of available NordVPN profiles a IP address to connect to

Auto-enters your username and password.

Handy if you are a targeted individual that wants a completely quick and random method of picking a VPN server to choose from.

# Installation instructions

Copy both ovpn_tcp and ovpn_udp folders to /etc/openvpn

`cp -r ovpn_* /etc/openvpn`

Create a symbolic link like vpn-autoconnect

`ln -s $PWD/openvpn_autoconnect.py /usr/local/bin/vpn-autoconnect`

Create two files containing your NordVPN username and password

`echo {username} > /root/nordvpnuser`
`echo {password} > /root/nordvpnpass`

Now you can randomly pick out of 9,760 IP addresses to choose from to autoconnect each time!


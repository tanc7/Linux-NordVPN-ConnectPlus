# Completely random openvpn autoconnect!

Randomly selects from list of available NordVPN profiles a IP address to connect to

Auto-enters your username and password.

Handy if you are a targeted individual that wants a completely quick and random method of picking a VPN server to choose from.

# New Update, Connect-OpenVPN-over-Shadowsocks support

**Random-OVPN-Autoconnect now supports connecting over Shadowsocks** to protect the identity of the VPN from being discovered by your fascist oppressors.

This prevents the VPN from being identified and blocked, which is common in both China and the United States.

How to use.

`vpn-autoconnect.py 1` is the standard way of connecting directly to OpenVPN without the anonymizing web-traffic look of Shadowsocks

`vpn-autoconnect.py 2 127.0.0.1 1080 198.199.98.12` uses the alternative Shadowsocks-mode to utilize a EXISTING Shadowsocks session, to have the traffic first routed through your remote Shadowsocks server at 198.199.98.12, before reaching back to your randomly chosen OpenVPN server while appearing to be unassuming HTTPS traffic (as in you must already have connected to the server, if you need a remote Shadowsocks server, consider using Streisand.) 

# Warning about using Westerner Cloud Services to host a Shadowsocks server

Do not use the recommended builds of Amazon EC2 Cloud Instances, DigitalOcean Droplets, or Rackspace sessions to host your remote Shadowsocks server, these cloud-based Infrastructure-as-a-Service providers serve 'Big Brother' before they ever consider serving you. It's not commonly known, but Amazon is the largest IaaS provider for the United States government, including their feared CIA-NSA private-cloud infrastructure, where no ordinary United States citizen is allowed access, unless they were infected with malware with a specialized TLS certificate that allows the Remote Access Trojan's traffic to pass through into the private cloud's Command-and-Control servers.

**In other words, if you were allowed to touch the private cloud. You got owned by a three letter agency.**

If you are some God-fearing, Sieg-Heiling, White Nationalist and Alt-Right self-hating nutcase that loves the taste of mayonaise, and you do not use a alternative to what I just warned you about, you are a stupid ass that earned your spot in prison. Take what I am telling you with more than a grain of salt, and put more effort into covering your tracks. I am doing this because you're my customer, and this is what you paid me to tell you. Technically, I failed you if you got caught up.

Here is a good example of a alternative to the oppressor's military-industrial IT complex, it is a similar service to Amazon AWS but it's provided by a offshore entity and they accept bitcoin (they are in fact, Bulgarian-owned): https://www.superbithost.com/offshore-bitcoin-vps/linux/russia

Make sure you pre-plan the process. Figure out what distro of Linux you want to host and install in the alt-cloud. Figure out if it smoothly configures Shadowsocks, Wireguard, OpenVPN, SSL-Tunnel, and Tor obfs4 relays properly. And always procure vital services from a country that has "strained diplomatic ties" with Big Brother. The more unwilling or resistant to law enforcement cooperation/coercion the entity/country is, the longer it takes for the Feds to gain any reasonable or workable amount of intelligence about you.


# Installation instructions

Edit permissions of the python file and then copy to your executable path

`chmod 755 *.py && cp -r openvpn_autoconnect.py /usr/local/bin/vpn_autoconnect`

Create two files containing your NordVPN username and password

`echo {username} > /root/nordvpnuser`
`echo {password} > /root/nordvpnpass`

Now you can randomly pick out of 9,760 IP addresses to choose from to autoconnect each time!


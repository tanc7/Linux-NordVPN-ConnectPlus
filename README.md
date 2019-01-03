# Completely random openvpn autoconnect!

Randomly selects from list of available NordVPN profiles a IP address to connect to

Auto-enters your username and password.

Handy if you are a targeted individual that wants a completely quick and random method of picking a VPN server to choose from.

# New Update, Connect-OpenVPN-over-Shadowsocks support

**Random-OVPN-Autoconnect now supports connecting over Shadowsocks** to protect the identity of the VPN from being discovered by your fascist oppressors.

This prevents the VPN from being identified and blocked, which is common in both China and the United States. It appears on Wireshark as both HTTP/HTTPS (requests made by Shadowsocks) and TCP traffic (OpenVPN). The normal looking traffic doesn't set off alarms like VPNs and Tor do.

***Warning: When you wrap a OpenVPN session with Shadowsocks, only the traffic that passes through the Shadowsocks listener port will be proxified and therefore, sent to the VPN server to be anonymized***

That means all other traffic that is NOT proxy-aware OR NOT transparently proxyfied using either tsocks or proxychains will OPEN to packet sniffers and deep packet inspection. Please check that you can proxify your traffic of your app if it has proxy settings (use SOCKS5) or if you can proxify the app with `proxychains command`. See this diagram...

Unproxified App ----Transparent Proxifier----> Shadowsocks listener 1080 ----Forwards----> OpenVPN session

Proxychains will also need to be configured by editing the configuration file `nano /etc/proxychains.conf` and removing `socks4 127.0.0.1 9050` and replacing it with `socks5 127.0.0.1 1080`. You also need to edit your proxyresolv script, `nano /usr/lib/proxychains3/proxyresolv` and change `4.2.2.2` to `1.1.1.1` or `8.8.8.8`.

***Only traffic that is transparently proxified such as `proxychains firefox google.com` will be protected through this scheme***

# Usage syntax

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

# Locally hosted Shadowsocks proxy server

Edit your shadowsocks configuration, `nano /etc/shadowsocks/config.json` and enter the following...

    "server":"127.0.0.1",
    "server_port":8388,
    "local_address": "127.0.0.1",
    "local_port":1080,
    "password":"PASSWORD",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open": false,
    "workers": 1,
    "prefer_ipv6": false

Edit your crontab, `crontab -e` and add this to the bottom

`@reboot ss-server -c /etc/shadowsocks/config.json -d 1.1.1.1,8.8.8.8,8.8.4.4 start`

Download the graphical Shadowsocks Client at https://github.com/shadowsocks/shadowsocks-qt5/releases

Run the AppImage file

`chmod a+x Shadowsocks-Qt5-3.0.1-x86_64.AppImage && ./Shadowsocks-Qt5-3.0.1-x86_64.AppImage`

Then use the GUI and enter the information that was contained in your config.json above. Now my Python app automatically reconfigures your OVPN profile files for Shadowsocks use, but for the sake of learning, you simp
ly add...

`socks-proxy $LOCAL_SERVER_IP $LOCAL_LISTEN_PORT`

and

`route $LOCALHOST 255.255.255.255 net_gateway`

to the bottom of the .ovpn file and then run it with `openvpn file.ovpn`

In my situation I simply entered this at the bottom of my many ovpn files

`socks-proxy 127.0.0.1 1080`
`route 127.0.0.1 255.255.255.255 net_gateway`

**All my app did is wait for you to connect to Shadowsocks before proceeding with the last step**


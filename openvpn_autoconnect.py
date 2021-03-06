#!/usr/bin/python
#coding=utf-8
import pexpect, os, sys, operator, subprocess, threading, random, re

# autoconnects to NordVPN and enters login info

credsuser = "/root/nordvpnuser"
credspass = "/root/nordvpnpass"

def popen_background(cmd):
    p = subprocess.Popen(
        cmd,
        shell=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    o = p.stdout.read()
    output = str(o.encode('utf-8')).strip().rstrip()
    return output

# insert code to allow openvpn to be connected over shadowsocks
def ovpn_over_shadowsocks_enable(local_server,listen_port,shadowsocks_server,ovpn_file):# temporarily writes the shadowsocks routing info into the ovpn file
    content = """socks-proxy {} {}\r\nroute {} 255.255.255.255 net_gateway""".format(
        str(local_server),
        str(listen_port),
        str(shadowsocks_server)
    )

    # saves a copy of the original ovpn profile to edit with shadowsocks information
    temp_file = ovpn_file + "over-shadowsocks.ovpn"
    del_cmd = "rm -rf {}".format(str(temp_file))
    os.system(del_cmd)
    r = open(ovpn_file,'r')
    L = r.readlines()

    w = open(temp_file,'a+')
    for line in L:# Deletes old/existing configuration lines
        if re.search("socks-proxy",line):
            L.remove(line)
        if re.search("net_gateway",line):
            L.remove(line)
    
    for line in L:
        w.write(line)

        
    # writes the new configuration line on bottom of ovpn profile

    w.write(content)
    w.close()
    return temp_file
def readcreds():
    return

def decisionloop(child):
    # print "DEBUG: child process is",child
    # print "DEBUG: In function decisionloop()"
    result=child.expect(
        [
            pexpect.EOF,
            'Enter Auth Username',
            'Enter Auth Password',
            pexpect.TIMEOUT
        ]
    )
    try:
        if(result==0):
            child.sendline('\n')
            decisionloop(child)
        if(result==1):
            child.sendline(username)
            decisionloop(child)
            # if(result==2):
            #     child.sendline(password)
        if(result==2):
            child.sendline(password)
            decisionloop(child)
        if(result==3):
            child.interact()
            # child.interact()
        # err = child.read()
        # print err
    except:
        err = child.read()
        # print "UNKNOWN EXCEPTION:\r\n",err
    return
def autoentry(cmd):
    print "DEBUG: In function autoentry(cmd)"

    username = popen_background("cat /root/nordvpnuser")
    password = popen_background("cat /root/nordvpnpass")
    child = pexpect.spawn(
        cmd,
        logfile=sys.stdout,
        timeout=20
     )
    result=child.expect(
        [
            pexpect.EOF,
            'Enter Auth Username',
            'Enter Auth Password',
            pexpect.TIMEOUT
        ]
    )
    try:
        if(result==0):# If EOF error, send new line to keep process running
            child.sendline('\n')
            decisionloop(child)
        if(result==1):# If it asks for username
            child.sendline(username)
            # Wait 10 seconds for password prompt
            child.expect_exact('Password',timeout=10)
            child.sendline(password)
            decisionloop(child)
        if(result==2):# if it asks for password
            child.sendline(password)
            decisionloop(child)
        if(result==3):# if timed out in 20 seconds. Release control to user
            child.interact()
    except:
        err = child.read()
        # print "UNKNOWN EXCEPTION:\r\n",err    
    return

def shadowsocks_mode():
    # activates shadowsocks mode that is, encapsulating your openvpn session over shadowsocks HTTPS/SOCKS5 proxies
    # prevents detection of VPN from your oppressors

    # Need to connect to shadowsocks server manually!

    # After connecting to shadowsocks servers, process user input parameters
    local_server = sys.argv[2]
    listen_port = sys.argv[3]
    shadowsocks_server = sys.argv[4]

    # randomly picks a openvpn profile and then creates a clone with additional shadowsocks configs in it
    ovpn_file = randselectserver()
    ovpn_profile = ovpn_over_shadowsocks_enable(local_server,listen_port,shadowsocks_server,ovpn_file)

    # launches shadowsocks version of ovpn profile instead
    cmd = "openvpn {}".format(str(ovpn_profile))
    print "DEBUG: Running command\r\n",cmd
    autoentry(cmd)
    return

def launch_openvpn(selected_server):
    cmd = "openvpn {}".format(str(selected_server))
    print "DEBUG: Running command\r\n",cmd
    autoentry(cmd)
    return
def randselectserver():
    # path where I stored all my nordvpn profiles *.ovpn files
    path = "/etc/openvpn/ovpn_udp"
    cmd = "ls /etc/openvpn/ovpn_udp"
    servers = popen_background(cmd)
    L = servers.splitlines()
    # print "DEBUG: Server list\r\n",L
    # amt = sys.getsizeof(L)-1
    # R = random.randint(0,amt)
    selected_server = random.choice(L)
    print "DEBUG: Selected server %s" % str(selected_server)
    os.chdir(path)
    os.system(cmd)

    # launch_openvpn(selected_server)
    # os.system(cmd)
    return selected_server

def main():
    print "Operating modes\r\n\t1 = 'Straight-Connect Mode', connect directly via OpenVPN\r\n\t2 = 'Shadowsocks-Connect Mode' connect to your OpenVPN server utilizing Shadowsocks HTTPS/SOCKS encapsulation, prevents discovery by oppressive governments"
    print "Syntax:\r\n\tpython openvpn_autoconnect.py <2> <127.0.0.1> <local proxy listen port> <remote shadowsocks server>"
    opmode = int(sys.argv[1])

    if opmode == 1:
        selected_server = randselectserver()
        launch_openvpn(selected_server)
    elif opmode == 2:
        shadowsocks_mode()
    else:
        os.system('clear')
        print "Exception: Syntax error. To use this program...\r\nNormal Straight-Connect Mode\tpython openvpn_autoconnect.py 1\r\nConnect-over-Shadowsocks Mode\tpython openvpn_autoconnect.py 2 127.0.0.1 1080 <remote shadowsocks server IP>"
        main()
    return
main()
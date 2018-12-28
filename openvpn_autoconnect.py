#!/usr/bin/python
#coding=utf-8
import pexpect, os, sys, operator, subprocess, threading, random

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
def readcreds():
    return

def decisionloop(child):
    print "DEBUG: child process is",child
    print "DEBUG: In function decisionloop()"
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
        print "UNKNOWN EXCEPTION:\r\n",err
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
        print "UNKNOWN EXCEPTION:\r\n",err    
    return

def randselectserver():
    # path where I stored all my nordvpn profiles *.ovpn files
    path = "/etc/openvpn/ovpn_tcp"
    cmd = "ls /etc/openvpn/ovpn_tcp"
    servers = popen_background(cmd)
    L = servers.splitlines()
    print "DEBUG: Server list\r\n",L
    # amt = sys.getsizeof(L)-1
    # R = random.randint(0,amt)
    selected_server = random.choice(L)
    print "DEBUG: Selected server %s" % str(selected_server)
    os.chdir(path)
    os.system(cmd)

    cmd = "openvpn {}".format(str(selected_server))
    print "DEBUG: Running command\r\n",cmd
    autoentry(cmd)
    # os.system(cmd)
    return

def main():
    randselectserver()
    return
main()
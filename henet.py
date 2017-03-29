#!/usr/bin/env python3

import requests
from subprocess import check_output
from shlex import split as ssplit
from shutil import which
from datetime import datetime
import socket


url = 'https://ipv6.he.net/certification/login.php'
auth_data = {
    'f_user': '',
    'f_pass': ''
}

def get_domain():
    dayofyear = datetime.now().timetuple().tm_yday
    with open('aaaa_domains.txt', 'r') as f:
        for lineix in range(dayofyear):
            domain = f.readline()
    return domain.replace('\n','')

def runtest(test, jar):
    testurl = 'https://ipv6.he.net/certification/daily.php?test='+test
    domain = get_domain()
    ip6 = socket.getaddrinfo(domain, None, socket.AF_INET6)[0][4][0]
    if test == 'aaaa':
        cmd = 'dig -t AAAA '+domain
    elif test == 'ptr':
        cmd = 'dig -x '+ip6
    elif test == 'ping':
        cmd = 'ping -6 -c3 '+domain
    # apparently those two tests don't need unique values every day..
    elif test == 'traceroute':
        cmd = 'traceroute -6 he.net'
    elif test == 'whois':
        cmd = 'whois 2001:470:0:76::2'
    print('running test "{}" with "{}"'.format(test, cmd))
    data = check_output(ssplit(cmd)).decode('utf-8')
    r = requests.post(testurl, data={'input': data}, cookies=jar)

def main():
    assert auth_data['f_user'] is not '', 'missing auth_data'
    for cmd in ['dig', 'whois', 'traceroute', 'ping']:
        assert which(cmd) is not None, "command {} is missing".format(cmd)
    r = requests.post(url, data = auth_data)
    assert r.status_code is 200, 'login failed'
    jar = r.history[0].cookies
    tests = ['aaaa', 'ptr', 'ping', 'traceroute', 'whois']
    for testparm in tests:
        runtest(testparm, jar)

if __name__ == "__main__":
    main()

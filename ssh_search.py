"""
script to pull an onion services server SSH key and HTTPS key and then send
said keys to Shodan via their API to check if Shodan knows if the keys
correspond to the any data entries in Shodan that can be used to generate leads
for investigators

Author: B00099224 - Paddy Kerley - LegendaryPatMan

"""

#!/usr/bin/env python

import socket
import socks
import urllib2 # ?
import paramiko
import hashlib
import shodan

# site list to be read in by urllib2
sites = []

# get ssh key

try:
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    for x in sites:
        urllib2.urlopen(x)
except socket.error:
    print "Error opening socket"
    quit()

try:
    myTransport = paramiko.Transport(mySocket)
    myTransport.start_client()
    sshKey = myTransport.get_remote_server_key()
except paramiko.SSHException:
    print "SSH error"
    quit()

myTransport.close()
mySocket.close()

# store the key in md5, sha1, sha224, sha256, sha384 and sha512

printableType = sshKey.get_name()
printableKey = base64.encodestring(sshKey.__str__()).replace('\n', '')
sshFingerprintmd5 = hashlib.md5(sshKey.__str__()).hexdigest()
sshFingerprintsha1 = hashlib.sha1(sshKey.__str__()).hexdigest()
sshFingerprintsha224 = hashlib.sha224(sshKey.__str__()).hexdigest()
sshFingerprintsha256 = hashlib.sha256(sshKey.__str__()).hexdigest()
sshFingerprintsha384 = hashlib.sha384(sshKey.__str__()).hexdigest()
sshFingerprintsha512 = hashlib.sha512(sshKey.__str__()).hexdigest()

#get ssl/tls keys

# Shodan API configuration
API_KEY = 'YOUR API KEY'

try:
    # API setup
    api = shodan.Shodan(API_KEY)

    #API search
    md5 = shodan.search(sshFingerprintmd5)
    for result in md5['matches']:
            print('IP: {}'.format(result['ip_str']))
            print(result['data'])
            print('')

    sha1 = shodan.search(sshFingerprintsha1)
    for result in sha1['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')

    sha224 = shodan.search(sshFingerprintsha224)
    for result in sha224['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')

    sha256 = shodan.search(sshFingerprintsha256)
    for result in sha256['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')

    sha384 = shodan.search(sshFingerprintsha384)
    for result in sha384['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')

    sha512 = shodan.search(sshFingerprintsha512)
    for result in sha512['matches']:
                print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')

    #Shodan error handling
except Exception as e:
    print('Error: {}'.format(e))
    sys.exit(1)



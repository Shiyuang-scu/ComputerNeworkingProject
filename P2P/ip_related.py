import subprocess
import re
import platform
from socket import *


def find_all_ip(platform):
    ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    if platform == "Darwin" or platform == "Linux":
        ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        ip_pattern = re.compile('(inet %s)' % ipstr)
        if platform == "Linux":
            ip_pattern = re.compile('(inet %s)' % ipstr)
        pattern = re.compile(ipstr)
        iplist = []
        for ipaddr in re.finditer(ip_pattern, str(output)):
            ip = pattern.search(ipaddr.group())
            if ip.group() != "127.0.0.1":
                iplist.append(ip.group())
        return iplist
    elif platform == "Windows":
        ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        ip_pattern = re.compile("IPv4 Address(\. )*: %s" % ipstr)
        pattern = re.compile(ipstr)
        iplist = []
        for ipaddr in re.finditer(ip_pattern, str(output)):
            ip = pattern.search(ipaddr.group())
            if ip.group() != "127.0.0.1":
                iplist.append(ip.group())
        return iplist

def str2ip(arg1: str):
    temp = int(arg1, 16)
    a1 = str((temp >>24)&0xff)
    a2 = str((temp >>16)&0xff)
    a3 = str((temp >>8)&0xff)
    a4 = str(temp&0xff)
    return a1+'.'+a2+'.'+a3+'.'+a4


def find_all_mask(platform):
    ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    maskstr = '0x([0-9a-f]{8})'
    if platform == "Darwin" or platform == "Linux":
        ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        mask_pattern = re.compile('(netmask %s)' % maskstr)
        pattern = re.compile(maskstr)
        if platform == "Linux":
            mask_pattern = re.compile(r'Mask:%s' % ipstr)
            pattern = re.compile(ipstr)
        masklist = []
        for maskaddr in re.finditer(mask_pattern, str(output)):
            mask = pattern.search(maskaddr.group())
            if mask.group() != '0xff000000' and mask.group() != '255.0.0.0':
                masklist.append(str2ip(mask.group()))
        return masklist
    elif platform == "Windows":
        ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        mask_pattern = re.compile(r"Subnet Mask (\. )*: %s" % ipstr)
        pattern = re.compile(ipstr)
        masklist = []
        for maskaddr in mask_pattern.finditer(str(output)):
            mask = pattern.search(maskaddr.group())
            if mask.group() != '255.0.0.0':
                masklist.append(mask.group())
        return masklist


def get_broad_addr(ipstr, maskstr):
    iptokens = map(int, ipstr.split("."))
    masktokens = map(int, maskstr.split("."))
    broadlist = []
    for i in range(len(iptokens)):
        ip = iptokens[i]
        mask = masktokens[i]
        broad = ip & mask | (~mask & 255)
        broadlist.append(broad)
    return '.'.join(map(str, broadlist))


def find_all_broad(platform):
    ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    if platform == "Darwin" or platform == "Linux":
        ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
        output = (ipconfig_process.stdout.read())
        broad_pattern = re.compile('(broadcast %s)' % ipstr)
        # if platform == "Linux":
        #     broad_pattern = re.compile(r'Bcast:%s' % ipstr)
        pattern = re.compile(ipstr)
        broadlist = []
        for broadaddr in broad_pattern.finditer(str(output)):
            broad = pattern.search(broadaddr.group())
            broadlist.append(broad.group())
        return broadlist
    elif platform == "Windows":
        iplist = find_all_ip(platform)
        masklist = find_all_mask(platform)
        broadlist = []
        for i in range(len(iplist)):
            broadlist.append(get_broad_addr(iplist[i], masklist[i]))
        return broadlist


def ip2num(ip: str):
    a = [int(i) for i in ip.split('.')]
    result = (a[0] << 24) + (a[1] << 16) + (a[2] << 8) + a[3]
    return result


def isSameSubnet(ip1: str, ip2: str, mask: str):
    ma = ip2num(mask)
    return (ip2num(ip1) & ma) == (ip2num(ip2) & ma)


def findFreePort():
    current_port = 11415
    while current_port < 65535:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(('', current_port))
            sock.listen(1)
            return current_port, sock
        except:
            current_port += 1
    raise RuntimeError('can\'t find free port')


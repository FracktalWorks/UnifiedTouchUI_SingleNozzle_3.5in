import subprocess
import re

def getIP(interface):
    try:
        scan_result = \
            (subprocess.Popen("ifconfig | grep " + interface + " -A 1", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")
        # Processing STDOUT into a dictionary that later will be converted to a json file later
        rInetAddr = r"inet\s*([\d.]+)"
        rInet6Addr = r"inet6"
        mt6Ip = re.search(rInet6Addr, scan_result)
        mtIp = re.search(rInetAddr, scan_result)
        if not(mt6Ip) and mtIp and len(mtIp.groups()) == 1:
            return str(mtIp.group(1))
    except Exception as e:
        print(e)
        return None

def getMac(interface):
    try:
        mac = subprocess.Popen(" cat /sys/class/net/" + interface + "/address",
                               stdout=subprocess.PIPE, shell=True).communicate()[0].rstrip()
        if not mac:
            return "Not found"
        return mac.upper()
    except:
        return "Error"


def getWifiAp():
    try:
        ap = subprocess.Popen("iwgetid -r", 
                              stdout=subprocess.PIPE, shell=True).communicate()[0].rstrip()
        if not ap:
            return "Not connected"
        return ap.decode("utf-8")
    except:
        return "Error"


def getHostname():
    try:
        hostname = subprocess.Popen("cat /etc/hostname", stdout=subprocess.PIPE, shell=True).communicate()[0].rstrip()
        if not hostname:
            return "Not connected"
        return hostname.decode("utf-8")  + ".local"
    except:
        return "Error"

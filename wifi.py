import subprocess
import nmcli

def getWifiInterface():
    try:
        fields = 'DEVICE,TYPE,STATE'
        args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'device']
        outf = subprocess.check_output(args, stderr = subprocess.STDOUT)
        va =  nmcli.parse(outf)
        r = {}
        for i in va:
            device, type, state = i
            if type == "wifi" and state != "unmanaged":
                r[device] = state
        return r
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}


def getScanResult():
    try:
        fields = 'SSID,MODE,CHAN,RATE,SIGNAL,SECURITY'
        args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'device', 'wifi']
        outf = subprocess.check_output(args, stderr = subprocess.STDOUT)
        va =  nmcli.parse(outf)
        r = {}
        for i in va:
            ssid, mode, chan, rate, signal, enc = i
            r[ssid] = {"mode": mode, "channel": chan, "rate": rate, "signal": signal, "encryption": enc}
        return r
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}

def getWifiConnection():
    try:
        fields = 'NAME,UUID,TYPE,DEVICE'
        args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'connection']
        outf = subprocess.check_output(args, stderr = subprocess.STDOUT)
        va =  nmcli.parse(outf)
        r = {}
        for i in va:
            name, uuid, type, device = i
            if type == "802-11-wireless":
                r[uuid] = {"name": name, "device": device}
        return r
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}

def activateWifiConnection(uuid, iface = None):
    if uuid == None:
        return {"error": "invalid parameter"}
    try:
        args = ['env', 'LC_ALL=C', 'nmcli', 'connection', 'up', uuid]
        if iface:
            args.append("ifname")
            args.append(iface)
        outf = subprocess.check_output(args, stderr= subprocess.STDOUT)
        return {"msg": nmcli.strip(outf)}
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}


def createWifiConnection(ssid, password = None, iface=None):
    timeout = '20'
    if ssid == None:
        return {"error": "invalid parameter"}
    args = ['env', 'LC_ALL=C', 'nmcli', '--wait', timeout, 'device', 'wifi', 'connect', ssid]
    if password:
        args.append("password")
        args.append(password)
    if iface:
        args.append("ifname")
        args.append(iface)
    try:
        outf = subprocess.check_output(args, stderr= subprocess.STDOUT)
        return {"msg": nmcli.strip(outf)}
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}

def deleteWifiConnection(uuid):
    if uuid == None:
        return {"error": "invalid parameter"}
    try:
        args = ['env', 'LC_ALL=C', 'nmcli', 'connection', 'delete', uuid]
        outf = subprocess.check_output(args, stderr= subprocess.STDOUT)
        return {"msg": "ok"}
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}

def disconnectWifi(iface):
    if iface == None:
        return {"error": "invalid parameter"}
    try:
        args = ['env', 'LC_ALL=C', 'nmcli', 'device', 'disconnect', iface]
        outf = subprocess.check_output(args, stderr= subprocess.STDOUT)
        return {"msg": "ok"}
    except subprocess.CalledProcessError as e:
        return {"error": nmcli.strip(e.output)}

if __name__ == "__main__":
    print(getWifiInterface())
    print(getScanResult())
    print(getWifiConnection())

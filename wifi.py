import subprocess
import nmcli

def runSubProc(args):
    import os
    po, pi = os.pipe()
    try:
        out = subprocess.check_output(args, stderr = pi)
        os.close(pi)
        os.close(po)
        return True, out
    except subprocess.CalledProcessError as e:
        out = os.read(po, 1<<12)
        os.close(pi)
        os.close(po)
        return False, nmcli.strip(out)

def getWifiInterface():
    fields = 'DEVICE,TYPE,STATE'
    args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'device']
    ok, out = runSubProc(args)
    if ok:
        va =  nmcli.parse(out)
        r = {}
        for i in va:
            device, type, state = i
            if type == "wifi" and state != "unmanaged":
                r[device] = state
        return r
    else:
        return {"error": out}

def getScanResult():
    fields = 'SSID,MODE,CHAN,RATE,SIGNAL,SECURITY'
    args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'device', 'wifi']
    ok, out = runSubProc(args)
    if ok:
        va = nmcli.parse(out)
        r = {}
        for i in va:
            ssid, mode, chan, rate, signal, enc = i
            r[ssid] = {"mode": mode, "channel": chan, "rate": rate, "signal": signal, "encryption": enc}
        return r
    else:
        return {"error": out}

def getWifiConnection():
    fields = 'NAME,UUID,TYPE,DEVICE'
    args = ['env', 'LC_ALL=C', 'nmcli', '-t', '-f', fields, 'connection']
    ok, out = runSubProc(args)
    if ok:
        va =  nmcli.parse(out)
        r = {}
        for i in va:
            name, uuid, type, device = i
            if type == "802-11-wireless":
                r[uuid] = {"name": name, "device": device}
        return r
    else:
        return {"error": out}

def activateWifiConnection(uuid, iface = None):
    if uuid == None:
        return {"error": "invalid parameter"}
    args = ['env', 'LC_ALL=C', 'nmcli', 'connection', 'up', uuid]
    if iface:
        args.append("ifname")
        args.append(iface)
    ok, out = runSubProc(args)
    if ok:
        return {"msg": nmcli.strip(out)}
    else:
        return {"error": out}

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
    ok, out = runSubProc(args)
    if ok:
        return {"msg": nmcli.strip(out)}
    else:
        return {"error": out}

def deleteWifiConnection(uuid):
    if uuid == None:
        return {"error": "invalid parameter"}
    args = ['env', 'LC_ALL=C', 'nmcli', 'connection', 'delete', uuid]
    ok, out = runSubProc(args)
    if ok:
        return {"msg": "ok"}
    else:
        return {"error": out}

def disconnectWifi(iface):
    if iface == None:
        return {"error": "invalid parameter"}
    args = ['env', 'LC_ALL=C', 'nmcli', 'device', 'disconnect', iface]
    ok, out = runSubProc(args)
    if ok:
        return {"msg": "ok"}
    else:
        return {"error": out}

if __name__ == "__main__":
    print(getWifiInterface())
    print(getScanResult())
    print(getWifiConnection())

#!/usr/bin/env python3
import subprocess
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("install|uninstall")
        sys.exit(2)

    if sys.argv[1] == 'install':
        args = ["pip3", "install", "PyBluez"]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print("can't install PyBluez", file=sys.stderr)
            sys.exit(1)

        with open("pybtsp.service.template") as temp:
            s = temp.read()
            fs = s.format(pwd=os.getcwd())
        try:
            os.unlink("/etc/systemd/system/pybtsp.service")
        except FileNotFoundError:
            pass

        with open("/etc/systemd/system/pybtsp.service", 'x') as target:
            print("writing unit file for systemd")
            target.write(fs)

        args = ["systemctl", "enable", "pybtsp"]
        try:
            subprocess.check_call(args)
        except CalledProcessError:
            print("can't enable pybtsp", file=sys.stderr)
            os.unlink("/etc/systemd/system/pybtsp.service")
            sys.exit(1)
    elif sys.argv[1] == 'uninstall':
        args = ["systemctl", "disable", "pybtsp"]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print("can't disable pybtsp", file=sys.stderr)
            sys.exit(1)
        os.unlink("/etc/systemd/system/pybtsp.service")
    else:
        print("install|uninstall")


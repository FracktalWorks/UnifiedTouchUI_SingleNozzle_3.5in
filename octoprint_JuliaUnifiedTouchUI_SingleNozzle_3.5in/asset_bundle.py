#!/usr/bin/env python
import subprocess
import math
import os
from datetime import datetime
import argparse


class AssetBundle:
    def __init__(self):
        self.h = self.hc()
        self.u = self.uc(self.h)

    def hc(self):
        x = -1
        try:
            proc = subprocess.Popen(["cat", "/sys/class/net/wlan0/address"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            op, _ = proc.communicate()
            if proc.returncode == 0:
                if op is not None:
                    op = op.replace(":", "")
                    op = op.lower()
                    # op = op[7:12]
                    op = op[::-1]
                    # op = "ffffffbe728b"
                    # print(op)
                    for i, c in enumerate(op):
                        # x += (ord(c) + 7) * (i * 3)
                        if c.isdigit():
                            x += int(c) * (i * 3)
                        elif c.isalpha():
                            x += (ord(c) - ord('a') + 10) * (i * 3)
        except Exception as e:
            print(e)
        return x

    def uc(self, i):
        return int(i ** 2) + int(math.floor(67 / i)) + int(math.floor(167 * (i / 4)))

    def match(self, k):
        if k is None:
            return False
        if self.h <= 0:
            return None
        return self.u == k

    def save(self, k):
        try:
            if self.match(k):
                with open("/home/pi/.fw_logo.dat", "w") as f:
                    f.write(str(k))
                    return True
        except Exception as e:
            print(e)
        return False

    def read_match(self):
        try:
            if os.path.exists("/home/pi/.fw_logo.dat"):
                with open("/home/pi/.fw_logo.dat", "r") as f:
                    x = f.readline().replace("\n", "")
                    return self.match(int(x))
            else:
                return False
        except Exception as e:
            print(e)
        return None

    def save_time(self):
        try:
            if os.path.exists("/home/pi/.screendrv.dat"):
                return False
            with open("/home/pi/.screendrv.dat", "w") as f:
                f.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True
        except Exception as e:
            print(e)
        return None

    def read_time(self):
        try:
            if os.path.exists("/home/pi/.screendrv.dat"):
                with open("/home/pi/.screendrv.dat", "r") as f:
                    x = f.readline().replace("\n", "")
                    return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(e)
        return datetime.now()

    def time_delta(self):
        delta = datetime.now() - self.read_time()
        # return delta.seconds > 30
        return (delta.total_seconds() / 3600) >= 12


if __name__ == "__main__":
    parser = argparse.ArgumentParser("TROJAN")
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-u", "--unlock", type=int, default=0)
    args = parser.parse_args()

    a = AssetBundle()
    h = a.hc()
    u = a.uc(h)

    if args.test:
        # a.save(u)
        a.save_time()
        print("Hardware ID = {}, Unlock code = {}".format(h, u))
        print("Match = {}, Match from file = {}".format(a.match(u), a.read_match()))
        print("File time = {}, Now = {}, Demo = {}".format(a.read_time(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), not a.time_delta()))

    elif args.unlock > 0:
        print(a.uc(args.unlock))

from PyQt5 import QtCore
from logger import *
from MainUIClass.config import Development, ip, apiKey
from octoprintAPI import octoprintAPI
import subprocess
import time

class ThreadSanityCheck(QtCore.QThread):

    loaded_signal = QtCore.pyqtSignal()
    startup_error_signal = QtCore.pyqtSignal()

    def __init__(self, logger = None, virtual=False): 
        log_info("Starting sanity check init.")
        super(ThreadSanityCheck, self).__init__()
        self.octopiclient = None
        self.MKSPort = None
        self.virtual = virtual
        if not Development:
            self._logger = logger

        log_debug("Exiting sanity check init.")

    def run(self):
        # global octopiclient
        self.shutdown_flag = False
        # get the first value of t1 (runtime check)
        uptime = 0
        # keep trying untill octoprint connects
        while (True):
            # Start an object instance of octopiAPI
            try:
                if (uptime > 30):
                    self.shutdown_flag = True
                    self.startup_error_signal.emit()
                    break
                log_debug("initialising octopiclient in threads.")
                self.octopiclient = octoprintAPI(ip, apiKey)
                log_debug(self.octopiclient)
                if not self.virtual:
                    result = subprocess.Popen("dmesg | grep 'ttyUSB'", stdout=subprocess.PIPE, shell=True).communicate()[0]
                    result = result.split(b'\n')  # each ssid and pass from an item in a list ([ssid pass,ssid paas])
                    result = [s.strip() for s in result]
                    for line in result:
                        if b'FTDI' in line:
                            self.MKSPort = line[line.index(b'ttyUSB'):line.index(b'ttyUSB') + 7].decode('utf-8')
                            print(self.MKSPort)
                        if b'ch34' in line:
                            self.MKSPort = line[line.index(b'ttyUSB'):line.index(b'ttyUSB') + 7].decode('utf-8')
                            print(self.MKSPort)

                    if not self.MKSPort:
                        self.octopiclient.connectPrinter(port="VIRTUAL", baudrate=115200)
                    else:
                        log_debug("Octopiclient connected.")
                        self.octopiclient.connectPrinter(port="/dev/" + self.MKSPort, baudrate=115200)
                break
            except Exception as e:
                time.sleep(1)
                uptime = uptime + 1
                print("Not Connected!")
        if not self.shutdown_flag:
            self.loaded_signal.emit()

    def get_octopiclient(self):
        while self.octopiclient == None:
            log_warning("octopiclient: " + str(self.octopiclient) + "\t not returning.")
        log_info("returning octopiclient successfully.")
        return self.octopiclient
import json
import os
from PyQt5 import QtCore
import sys
from MainUIClass.config import Development

if not Development:
    json_file_name = '/home/pi/printer_name.json'
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    json_file_name = os.path.join(parent_dir, 'printer_name.json')
    
allowed_names = ["Julia Advanced", "Julia Extended", "Julia Pro Single Nozzle"]

class printerName:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj
        self.initialisePrinterNameJson()
        print(self.getPrinterName())

    def connect(self):
        self.MainUIObj.enterPrinterName.clicked.connect(self.enterPrinterName_function)

    def enterPrinterName_function(self):
        temp_printerName = self.getPrinterName()
        if temp_printerName != self.MainUIObj.printerNameComboBox.currentText():
            self.setPrinterName(self.MainUIObj.printerNameComboBox.currentText())
            if Development:
                sys.exit()
            else:
                if not self.MainUIObj.homePageInstance.askAndReboot("Reboot to reflect changes?"):
                    self.setPrinterName(temp_printerName)

    def getPrinterName(self):
        try:
            with open(json_file_name, 'r') as file:
                data = json.load(file)
                return data.get('printer_name', 'Julia Advanced')  # Default to 'Julia Advanced'
        except (FileNotFoundError, json.JSONDecodeError):
            return 'Julia Advanced'

    def initialisePrinterNameJson(self):
        try:
            if not os.path.exists(json_file_name):
                data = {'printer_name': 'Julia Advanced'}
                self.writePrinterNameJson(data)
            else:
                try:
                    with open(json_file_name, 'r') as file:
                        data = json.load(file)
                    if data.get('printer_name') not in allowed_names:
                        self.setPrinterName("Julia Advanced")
                except (FileNotFoundError, json.JSONDecodeError):
                    self.setPrinterName("Julia Advanced")
        except Exception as e:
            self.MainUIObj._logger.error(e)

    def setPrinterName(self, name):
        data = {"printer_name": name}
        self.writePrinterNameJson(data)

    def writePrinterNameJson(self, data):
        with open(json_file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def setPrinterNameComboBox(self):
        current_printer_name = self.getPrinterName()
        index = self.MainUIObj.printerNameComboBox.findText(current_printer_name, QtCore.Qt.MatchFixedString)
        if index != -1:  # Check if a valid index was found
            self.MainUIObj.printerNameComboBox.setCurrentIndex(index)

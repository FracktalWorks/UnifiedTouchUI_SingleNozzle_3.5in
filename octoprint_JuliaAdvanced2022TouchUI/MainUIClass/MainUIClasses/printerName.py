import json
import os
from PyQt5 import QtCore
import sys
from MainUIClass.config import Development
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import askAndReboot

if not Development:
    json_file_name = '/home/pi/printer_name.json'
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    json_file_name = os.path.join(parent_dir, 'printer_name.json')
    
allowed_names = ["Julia Advanced", "Julia Extended", "Julia Pro Single Nozzle"]

class printerName(mainGUI.Ui_MainWindow):
    def __init__(self):
        self.initialisePrinterNameJson()
        print(self.getPrinterName())
        self.enterPrinterName.clicked.connect(self.enterPrinterName_function)
        super().__init__()

    def enterPrinterName_function(self):
        temp_printerName = self.getPrinterName()
        if temp_printerName != self.printerNameComboBox.currentText():
            self.setPrinterName(self.printerNameComboBox.currentText())
            if Development:
                sys.exit()
            else:
                if not askAndReboot(self, "Reboot to reflect changes?"):
                    self.setPrinterName(temp_printerName)

    @classmethod
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
            self._logger.error(e)

    def setPrinterName(self, name):
        data = {"printer_name": name}
        self.writePrinterNameJson(data)

    def writePrinterNameJson(self, data):
        with open(json_file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def setPrinterNameComboBox(self):
        current_printer_name = self.getPrinterName()
        index = self.printerNameComboBox.findText(current_printer_name, QtCore.Qt.MatchFixedString)
        if index != -1:  # Check if a valid index was found
            self.printerNameComboBox.setCurrentIndex(index)

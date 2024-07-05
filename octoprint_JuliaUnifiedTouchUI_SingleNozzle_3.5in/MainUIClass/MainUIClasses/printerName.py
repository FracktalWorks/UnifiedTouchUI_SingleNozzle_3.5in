import json
import os
from PyQt5 import QtCore
import sys
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import askAndReboot
from logger import *
import dialog
from MainUIClass.config import Development

if not Development:
    json_file_name = '/home/pi/printer_name.json'
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    json_file_name = os.path.join(parent_dir, 'printer_name.json')

allowed_names = ["Julia Advanced", "Julia Extended", "Julia Pro Single Nozzle"]

class printerName(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting printer name init.")
        log_debug("Printer name self parameter passed: " + str(self))
        try:
            self.initialisePrinterNameJson()
        except Exception as e:
            error_message = "Error initializing printerName JSON: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
        super().__init__()

    def setup(self):
        try:
            self.printerName = self.getPrinterName()
            self.enterPrinterName.clicked.connect(self.enterPrinterName_function)
        except Exception as e:
            error_message = "Error setting up printer name: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def enterPrinterName_function(self):
        try:
            temp_printerName = printerName.getPrinterName()
            if temp_printerName != self.printerNameComboBox.currentText():
                self.setPrinterName(self.printerNameComboBox.currentText())
                if Development:
                    sys.exit()
                else:
                    if not askAndReboot(self, "Reboot to reflect changes?"):
                        self.setPrinterName(temp_printerName)
        except Exception as e:
            error_message = "Error updating printer name: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

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
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    error_message = "Error loading printerName JSON: " + str(e)
                    log_error(error_message)
                    self.setPrinterName("Julia Advanced")
        except Exception as e:
            error_message = "Error initializing printerName JSON: " + str(e)
            log_error(error_message)

    def setPrinterName(self, name):
        try:
            data = {"printer_name": name}
            self.writePrinterNameJson(data)
        except Exception as e:
            error_message = "Error setting printer name: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def writePrinterNameJson(self, data):
        try:
            with open(json_file_name, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            error_message = "Error writing printerName JSON: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def setPrinterNameComboBox(self):
        try:
            current_printer_name = self.getPrinterName()
            index = self.printerNameComboBox.findText(current_printer_name, QtCore.Qt.MatchFixedString)
            if index != -1:  # Check if a valid index was found
                self.printerNameComboBox.setCurrentIndex(index)
        except Exception as e:
            error_message = "Error setting printer name combo box: " + str(e)
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    @classmethod
    def getPrinterName(cls):
        try:
            with open(json_file_name, 'r') as file:
                data = json.load(file)
                return data.get('printer_name', 'Julia Advanced')  # Default to 'Julia Advanced'
        except (FileNotFoundError, json.JSONDecodeError) as e:
            error_message = "Error loading printerName JSON: " + str(e)
            log_error(error_message)
            return 'Julia Advanced'
        except Exception as e:
            error_message = "Unexpected error while loading printerName JSON: " + str(e)
            log_error(error_message)
            return 'Julia Advanced'

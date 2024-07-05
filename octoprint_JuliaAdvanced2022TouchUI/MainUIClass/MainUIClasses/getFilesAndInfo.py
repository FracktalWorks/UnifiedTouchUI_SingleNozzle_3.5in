import dialog
import os
import subprocess
from datetime import datetime
from PyQt5 import QtGui, QtCore
from MainUIClass.config import _fromUtf8
from hurry.filesize import size
import mainGUI
from logger import *

class getFilesAndInfo(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting get files init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        """
        Sets up signal connections for various UI elements.
        """
        log_info("Setting up getFilesAndInfo.")
        try:
            # self.octopiclient = octopiclient
            log_debug("Octopiclient inside class getFilesAndInfo: " + str(self.octopiclient))
            
            # Connect signals for USB storage
            self.USBStorageBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.printLocationPage))
            self.USBStorageScrollUp.pressed.connect(lambda: self.fileListWidgetUSB.setCurrentRow(self.fileListWidgetUSB.currentRow() - 1))
            self.USBStorageScrollDown.pressed.connect(lambda: self.fileListWidgetUSB.setCurrentRow(self.fileListWidgetUSB.currentRow() + 1))
            self.USBStorageSelectButton.pressed.connect(self.printSelectedUSB)
            self.USBStorageSaveButton.pressed.connect(lambda: self.transferToLocal(prnt=False))

            # Connect signals for local storage
            self.localStorageBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.printLocationPage))
            self.localStorageScrollUp.pressed.connect(lambda: self.fileListWidget.setCurrentRow(self.fileListWidget.currentRow() - 1))
            self.localStorageScrollDown.pressed.connect(lambda: self.fileListWidget.setCurrentRow(self.fileListWidget.currentRow() + 1))
            self.localStorageSelectButton.pressed.connect(self.printSelectedLocal)
            self.localStorageDeleteButton.pressed.connect(self.deleteItem)

            # Connect signals for file selections
            self.fileSelectedBackButton.pressed.connect(self.fileListLocal)
            self.fileSelectedPrintButton.pressed.connect(self.printFile)
            self.fileSelectedUSBBackButton.pressed.connect(self.fileListUSB)
            self.fileSelectedUSBTransferButton.pressed.connect(lambda: self.transferToLocal(prnt=False))
            self.fileSelectedUSBPrintButton.pressed.connect(lambda: self.transferToLocal(prnt=True))

            log_info("Setup for getFilesAndInfo complete.")
        except Exception as e:
            error_message = f"Error setting up getFilesAndInfo: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def fileListLocal(self):
        '''
        Gets the file list from octoprint server, displays it on the list, as well as
        sets the stacked widget page to the file list page
        '''
        try:
            log_info("Fetching local file list.")
            self.stackedWidget.setCurrentWidget(self.fileListLocalPage)
            files = []
            for file in self.octopiclient.retrieveFileInformation()['files']:
                if file["type"] == "machinecode":
                    files.append(file)

            self.fileListWidget.clear()
            files.sort(key=lambda d: d['date'], reverse=True)
            for f in files:
                if ".gcode" in f['name']:
                    self.fileListWidget.addItem(f['name'])
            self.fileListWidget.setCurrentRow(0)
            log_info("Local file list fetched successfully.")
        except Exception as e:
            error_message = f"Error fetching local file list: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def fileListUSB(self):
        '''
        Gets the file list from USB and displays it on the list.
        '''
        try:
            log_info("Fetching USB file list.")
            self.stackedWidget.setCurrentWidget(self.fileListUSBPage)
            files = subprocess.Popen("ls /media/usb0 | grep gcode", stdout=subprocess.PIPE, shell=True).communicate()[0]
            files = files.decode('utf-8').split('\n')
            files = filter(None, files)
            self.fileListWidgetUSB.addItems(files)
            self.fileListWidgetUSB.setCurrentRow(0)
            log_info("USB file list fetched successfully.")
        except Exception as e:
            error_message = f"Error fetching USB file list: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def printSelectedLocal(self):
        '''
        Displays selected local file information and preview image.
        '''
        try:
            log_info("Printing selected local file.")
            self.fileSelected.setText(self.fileListWidget.currentItem().text())
            self.stackedWidget.setCurrentWidget(self.printSelectedLocalPage)
            file = self.octopiclient.retrieveFileInformation(self.fileListWidget.currentItem().text())
            
            # Display file details
            try:
                self.fileSizeSelected.setText(size(file['size']))
            except KeyError:
                self.fileSizeSelected.setText('-')
            try:
                self.fileDateSelected.setText(datetime.fromtimestamp(file['date']).strftime('%d/%m/%Y %H:%M:%S'))
            except KeyError:
                self.fileDateSelected.setText('-')
            try:
                m, s = divmod(file['gcodeAnalysis']['estimatedPrintTime'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.filePrintTimeSelected.setText("%dd:%dh:%02dm:%02ds" % (d, h, m, s))
            except KeyError:
                self.filePrintTimeSelected.setText('-')
            try:
                self.filamentVolumeSelected.setText("%.2f cm" % file['gcodeAnalysis']['filament']['tool0']['volume'] + chr(179))
            except KeyError:
                self.filamentVolumeSelected.setText('-')
            try:
                self.filamentLengthFileSelected.setText("%.2f mm" % file['gcodeAnalysis']['filament']['tool0']['length'])
            except KeyError:
                self.filamentLengthFileSelected.setText('-')
            
            # Load preview image
            img = self.octopiclient.getImage(self.fileListWidget.currentItem().text().replace(".gcode", ".png"))
            if img:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(img)
                self.printPreviewSelected.setPixmap(pixmap)
            else:
                self.printPreviewSelected.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))
            
            log_info("Selected local file printed successfully.")
        except Exception as e:
            error_message = f"Error printing selected local file: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def printSelectedUSB(self):
        '''
        Displays selected USB file information and preview image.
        '''
        try:
            log_info("Printing selected USB file.")
            self.fileSelectedUSBName.setText(self.fileListWidgetUSB.currentItem().text())
            self.stackedWidget.setCurrentWidget(self.printSelectedUSBPage)
            file = '/media/usb0/' + str(self.fileListWidgetUSB.currentItem().text().replace(".gcode", ".png"))
            
            # Check if image exists and display it
            try:
                exists = os.path.exists(file)
                if exists:
                    self.printPreviewSelectedUSB.setPixmap(QtGui.QPixmap(_fromUtf8(file)))
                else:
                    self.printPreviewSelectedUSB.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))
            except Exception as e:
                log_error(f"Error displaying USB image preview: {str(e)}")
                self.printPreviewSelectedUSB.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))
            
            log_info("Selected USB file printed successfully.")
        except Exception as e:
            error_message = f"Error printing selected USB file: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def transferToLocal(self, prnt=False):
        '''
        Transfers a selected USB file to local storage.
        '''
        try:
            log_info("Transferring file from USB to local.")
            file = '/media/usb0/' + str(self.fileListWidgetUSB.currentItem().text())
            self.uploadThread = ThreadFileUpload(file, prnt=prnt)
            self.uploadThread.start()
            if prnt:
                self.stackedWidget.setCurrentWidget(self.homePage)
            log_info("File transferred successfully from USB to local.")
        except Exception as e:
            error_message = f"Error transferring file from USB to local: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def printFile(self):
        '''
        Prints the selected file.
        '''
        try:
            log_info("Printing selected file.")
            self.octopiclient.selectFile(self.fileListWidget.currentItem().text(), True)
            self.stackedWidget.setCurrentWidget(self.homePage)
            log_info("File printed successfully.")
        except Exception as e:
            error_message = f"Error printing file: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def deleteItem(self):
        '''
        Deletes the selected file and its associated image file.
        '''
        try:
            log_info("Deleting selected file.")
            self.octopiclient.deleteFile(self.fileListWidget.currentItem().text())
            self.octopiclient.deleteFile(self.fileListWidget.currentItem().text().replace(".gcode", ".png"))
            self.fileListLocal()
            log_info("Selected file deleted successfully.")
        except Exception as e:
            error_message = f"Error deleting file from USB to local: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

class ThreadFileUpload(QtCore.QThread):
    def __init__(self, file, prnt=False):
        super(ThreadFileUpload, self).__init__()
        self.file = file
        self.prnt = prnt

    def run(self):
        '''
        Uploads the file and optionally prints it.
        '''
        try:
            log_info("Starting file upload.")
            exists = os.path.exists(self.file.replace(".gcode", ".png"))
            if exists:
                self.octopiclient.uploadImage(self.file.replace(".gcode", ".png"))

            if self.prnt:
                self.octopiclient.uploadGcode(file=self.file, select=True, prnt=True)
            else:
                self.octopiclient.uploadGcode(file=self.file, select=False, prnt=False)
            
            log_info("File upload completed successfully.")
        except Exception as e:
            error_message = f"Error uploading file: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

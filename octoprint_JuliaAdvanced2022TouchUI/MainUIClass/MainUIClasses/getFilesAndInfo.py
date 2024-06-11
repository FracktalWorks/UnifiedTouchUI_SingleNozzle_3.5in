from MainUIClass.config import octopiclient
import os
import subprocess
from datetime import datetime
from PyQt5 import QtGui, QtCore
from MainUIClass.config import _fromUtf8
from hurry.filesize import size

class getFilesAndInfo:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        # fileListUSBPage
        self.MainUIObj.USBStorageBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printLocationPage))
        self.MainUIObj.USBStorageScrollUp.pressed.connect(
            lambda: self.MainUIObj.fileListWidgetUSB.setCurrentRow(self.MainUIObj.fileListWidgetUSB.currentRow() - 1))
        self.MainUIObj.USBStorageScrollDown.pressed.connect(
            lambda: self.MainUIObj.fileListWidgetUSB.setCurrentRow(self.MainUIObj.fileListWidgetUSB.currentRow() + 1))
        self.MainUIObj.USBStorageSelectButton.pressed.connect(self.printSelectedUSB)
        self.MainUIObj.USBStorageSaveButton.pressed.connect(lambda: self.transferToLocal(prnt=False))

        # fileListLocalScreen
        self.MainUIObj.localStorageBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printLocationPage))
        self.MainUIObj.localStorageScrollUp.pressed.connect(
            lambda: self.MainUIObj.fileListWidget.setCurrentRow(self.MainUIObj.fileListWidget.currentRow() - 1))
        self.MainUIObj.localStorageScrollDown.pressed.connect(
            lambda: self.MainUIObj.fileListWidget.setCurrentRow(self.MainUIObj.fileListWidget.currentRow() + 1))
        self.MainUIObj.localStorageSelectButton.pressed.connect(self.printSelectedLocal)
        self.MainUIObj.localStorageDeleteButton.pressed.connect(self.deleteItem)

        # selectedFileLocalScreen
        self.MainUIObj.fileSelectedBackButton.pressed.connect(self.fileListLocal)
        self.MainUIObj.fileSelectedPrintButton.pressed.connect(self.printFile)

        # selectedFile USB Screen
        self.MainUIObj.fileSelectedUSBBackButton.pressed.connect(self.fileListUSB)
        self.MainUIObj.fileSelectedUSBTransferButton.pressed.connect(lambda: self.transferToLocal(prnt=False))
        self.MainUIObj.fileSelectedUSBPrintButton.pressed.connect(lambda: self.transferToLocal(prnt=True))

    def fileListLocal(self):
        '''
        Gets the file list from octoprint server, displays it on the list, as well as
        sets the stacked widget page to the file list page
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.fileListLocalPage)
        files = []
        for file in octopiclient.retrieveFileInformation()['files']:
            if file["type"] == "machinecode":
                files.append(file)

        self.MainUIObj.fileListWidget.clear()
        files.sort(key=lambda d: d['date'], reverse=True)
        # for item in [f['name'] for f in files] :
        #     self.fileListWidget.addItem(item)
        for f in files:
            if ".gcode" in f['name']:
                self.MainUIObj.fileListWidget.addItem(f['name'])
        #self.fileListWidget.addItems([f['name'] for f in files])
        self.MainUIObj.fileListWidget.setCurrentRow(0)

    def fileListUSB(self):
        '''
        Gets the file list from octoprint server, displays it on the list, as well as
        sets the stacked widget page to the file list page
        ToDO: Add deapth of folders recursively get all gcodes
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.fileListUSBPage)
        self.MainUIObj.fileListWidgetUSB.clear()
        files = subprocess.Popen("ls /media/usb0 | grep gcode", stdout=subprocess.PIPE, shell=True).communicate()[0]
        files = files.decode('utf-8').split('\n')
        files = filter(None, files)
        # for item in files:
        #     self.fileListWidgetUSB.addItem(item)
        self.MainUIObj.fileListWidgetUSB.addItems(files)
        self.MainUIObj.fileListWidgetUSB.setCurrentRow(0)

    def printSelectedLocal(self):

        '''
        gets information about the selected file from octoprint server,
        as well as sets the current page to the print selected page.
        This function also selects the file to print from octoprint
        '''
        try:
            self.MainUIObj.fileSelected.setText(self.MainUIObj.fileListWidget.currentItem().text())
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printSelectedLocalPage)
            file = octopiclient.retrieveFileInformation(self.MainUIObj.fileListWidget.currentItem().text())
            try:
                self.MainUIObj.fileSizeSelected.setText(size(file['size']))
            except KeyError:
                self.MainUIObj.fileSizeSelected.setText('-')
            try:
                self.MainUIObj.fileDateSelected.setText(datetime.fromtimestamp(file['date']).strftime('%d/%m/%Y %H:%M:%S'))
            except KeyError:
                self.MainUIObj.fileDateSelected.setText('-')
            try:
                m, s = divmod(file['gcodeAnalysis']['estimatedPrintTime'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.MainUIObj.filePrintTimeSelected.setText("%dd:%dh:%02dm:%02ds" % (d, h, m, s))
            except KeyError:
                self.filePrintTimeSelected.setText('-')
            try:
                self.MainUIObj.filamentVolumeSelected.setText(
                    ("%.2f cm" % file['gcodeAnalysis']['filament']['tool0']['volume']) + chr(179))
            except KeyError:
                self.MainUIObj.filamentVolumeSelected.setText('-')

            try:
                self.MainUIObj.filamentLengthFileSelected.setText(
                    "%.2f mm" % file['gcodeAnalysis']['filament']['tool0']['length'])
            except KeyError:
                self.MainUIObj.filamentLengthFileSelected.setText('-')
            # uncomment to select the file when selectedd in list
            # octopiclient.selectFile(self.fileListWidget.currentItem().text(), False)
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printSelectedLocalPage)

            '''
            If image is available from server, set it, otherwise display default image
            '''
            img = octopiclient.getImage(self.MainUIObj.fileListWidget.currentItem().text().replace(".gcode", ".png"))
            if img:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(img)
                self.MainUIObj.printPreviewSelected.setPixmap(pixmap)

            else:
                self.MainUIObj.printPreviewSelected.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))
        except:
            print ("Log: Nothing Selected")
            # Set image fot print preview:
            # self.printPreviewSelected.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/fracktal.png")))
            # print self.fileListWidget.currentItem().text().replace(".gcode","")
            # self.printPreviewSelected.setPixmap(QtGui.QPixmap(_fromUtf8("/home/pi/.octoprint/uploads/{}.png".format(self.FileListWidget.currentItem().text().replace(".gcode","")))))

            # Check if the PNG file exists, and if it does display it, or diplay a default picture.

    def printSelectedUSB(self):
        '''
        Sets the screen to the print selected screen for USB, on which you can transfer to local drive and view preview image.
        :return:
        '''
        try:
            self.MainUIObj.fileSelectedUSBName.setText(self.MainUIObj.fileListWidgetUSB.currentItem().text())
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printSelectedUSBPage)
            file = '/media/usb0/' + str(self.fileListWidgetUSB.currentItem().text().replace(".gcode", ".png"))
            try:
                exists = os.path.exists(file)
            except:
                exists = False

            if exists:
                self.MainUIObj.printPreviewSelectedUSB.setPixmap(QtGui.QPixmap(_fromUtf8(file)))
            else:
                self.MainUIObj.printPreviewSelectedUSB.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))
        except:
            print ("Log: Nothing Selected")

            # Set Image from USB

    def transferToLocal(self, prnt=False):
        '''
        Transfers a file from USB mounted at /media/usb0 to octoprint's watched folder so that it gets automatically detected bu Octoprint.
        Warning: If the file is read-only, octoprint API for reading the file crashes.
        '''

        file = '/media/usb0/' + str(self.fileListWidgetUSB.currentItem().text())

        self.uploadThread = ThreadFileUpload(file, prnt=prnt)
        self.uploadThread.start()
        if prnt:
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)

    def printFile(self):
        '''
        Prints the file selected from printSelected()
        '''
        octopiclient.selectFile(self.MainUIObj.fileListWidget.currentItem().text(), True)
        # octopiclient.startPrint()
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)

    def deleteItem(self):
        '''
        Deletes a gcode file, and if associates, its image file from the memory
        '''
        octopiclient.deleteFile(self.MainUIObj.fileListWidget.currentItem().text())
        octopiclient.deleteFile(self.MainUIObj.fileListWidget.currentItem().text().replace(".gcode", ".png"))

        # delete PNG also
        self.fileListLocal()

class ThreadFileUpload(QtCore.QThread):
    def __init__(self, file, prnt=False):
        super(ThreadFileUpload, self).__init__()
        self.file = file
        self.prnt = prnt

    def run(self):

        try:
            exists = os.path.exists(self.file.replace(".gcode", ".png"))
        except:
            exists = False
        if exists:
            octopiclient.uploadImage(self.file.replace(".gcode", ".png"))

        if self.prnt:
            octopiclient.uploadGcode(file=self.file, select=True, prnt=True)
        else:
            octopiclient.uploadGcode(file=self.file, select=False, prnt=False)


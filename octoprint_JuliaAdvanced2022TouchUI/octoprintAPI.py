from contextlib import contextmanager
import os
import requests
import json

'''
ToDo:
Check response codes for important functions
Check header content types in the GET/POST requests
'''


class octoprintAPI:
    def __init__(self, ip=None, apiKey=None):
        '''
        Initialize the object with URL and API key

        If a session is provided, it will be used (mostly for testing)
        '''
        if not ip:
            raise TypeError('Required argument \'ip\' not found or emtpy')
        if not apiKey:
            raise TypeError('Required argument \'apiKey\' not found or emtpy')
        self.ip = ip
        self.apiKey = apiKey
        # Try a simple request to see if the API key works
        # Keep the info, in case we need it later
        self.version = self.version()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++ File Handling  ++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def _prepend_local(cls, location):
        if location.split('/')[0] not in ('local', 'sdcard'):
            return 'local/' + location
        return location

    def retrieveFileInformation(self, location=None, force="false", recursive="false"):
        '''
        Retrieve information regarding all files currently available and
        regarding the disk space still available locally in the system

        If location is used, retrieve information regarding the files currently
        available on the selected location and - if targeting the local
        location - regarding the disk space still available locally in the
        system

        If location is a file, retrieves the selected file''s information
        '''
        headers = {'X-Api-Key': self.apiKey}
        if location:
            location = self._prepend_local(location)
            url = 'http://' + self.ip + '/api/files/{}'.format(location)
        else:
            url = 'http://' + self.ip + '/api/files'
        payload = {"recursive": recursive, "force": force}
        response = requests.get(url, headers=headers, params=payload)
        temp = response.json()
        return temp

    @contextmanager
    def _file_tuple(self, file):
        '''
        Yields a tuple with filename and file object

        Expects the same thing or a path as input
        '''
        mime = 'application/octet-stream'

        try:
            exists = os.path.exists(file)
        except:
            exists = False

        if exists:
            filename = os.path.basename(file)
            with open(file, 'rb') as f:
                yield (filename, f, mime)
        else:
            yield file + (mime,)

    def uploadGcode(self, file, location='local', select=False, prnt=False):
        '''
        Upload a given file
        It can be a path or a tuple with a filename and a file-like object
        :param file: path to file, eg /media/usb0/file1.gcode
        :param location: location to upload to on the server
        :param select: bool, selecting the file after uploading
        :param prnt: bool, start print after uploading
        :return: json response, with success of the upload and location
        '''
        with self._file_tuple(file) as file_tuple:
            files = {'file': file_tuple}
            payload = {'select': str(select).lower(), 'print': str(prnt).lower()}
            url = 'http://' + self.ip + '/api/files/{}'.format(location)
            headers = {'X-Api-Key': self.apiKey}
            response = requests.post(url, files=files, data=payload, headers=headers)
            temp = response.json()
            return temp



            # Should add error/status cheking in the response

    @contextmanager
    def _file_tuple_png(self, file):
        '''
        Yields a tuple with filename and file object

        Expects the same thing or a path as input
        '''
        # mime = 'application/octet-stream'
        mime = 'image/png'
        try:
            exists = os.path.exists(file)
        except:
            exists = False

        if exists:
            filename = os.path.basename(file)
            with open(file, 'rb') as f:
                yield (filename, f, mime)
        else:
            yield file + (mime,)

    def uploadImage(self, file, location='local'):
        '''
        Upload a given file
        It can be a path or a tuple with a filename and a file-like object
        :param file: path to file, eg /media/usb0/file1.gcode
        :param location: location to upload to on the server
        :param select: bool, selecting the file after uploading
        :param prnt: bool, start print after uploading
        :return: json response, with success of the upload and location
        '''

        with self._file_tuple_png(file) as file_tuple:
            files = {'file': file_tuple}
            url = 'http://' + self.ip + '/api/files/{}'.format(location)
            headers = {'X-Api-Key': self.apiKey}
            response = requests.post(url, files=files, headers=headers)
            temp = response.json()
            return temp

    def deleteFile(self, location):
        '''
        Delete the selected filename on the selected target

        Location is target/filename, defaults to local/filename
        '''
        location = self._prepend_local(location)
        url = 'http://' + self.ip + '/api/files/{}'.format(location)
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.delete(url, headers=headers)

    def selectFile(self, location, prnt=False):
        '''
        Selects a file for printing

        Location is target/filename, defaults to local/filename
        If print is True, the selected file starts to print immediately
        '''
        location = self._prepend_local(location)
        payload = {'command': 'select', 'print': prnt}
        url = 'http://' + self.ip + '/api/files/{}'.format(location)
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def getImage(self, name):
        url = 'http://' + self.ip + '/downloads/files/local/' + name
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            return response.content
        else:
            return False

    # Upload directly to directory
    # Download Timelapse
    # Print from USB
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++ Job Handeling+++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    '''
    Job Handeling functions, print pause, get cureent file info etc
    '''

    def getJobInformation(self):
        '''
        Retrieve information about the current job (if there is one)
        '''
        url = 'http://' + self.ip + '/api/job'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def startPrint(self):
        '''
        Starts the print of the currently selected file

        Use select() to select a file
        '''
        url = 'http://' + self.ip + '/api/job'
        payload = {'command': 'start'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def pausePrint(self):
        '''
        Pauses/unpauses the current print job

        There must be an active print job for this to work
        '''
        url = 'http://' + self.ip + '/api/job'
        payload = {'command': 'pause'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def restartPrint(self):
        '''
        Starts the print of the currently selected file

        Use select() to select a file
        '''
        url = 'http://' + self.ip + '/api/job'
        payload = {'command': 'restart'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def cancelPrint(self):
        '''
        Starts the print of the currently selected file

        Use select() to select a file
        '''
        url = 'http://' + self.ip + '/api/job'
        payload = {'command': 'cancel'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++ Connection Handling +++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def version(self):
        '''
        Retrieve information regarding server and API version
        '''
        url = 'http://' + self.ip + '/api/version'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def getPrinterConnectionSettings(self):
        '''
        Retrieve the current connection settings, including information
        regarding the available baudrates and serial ports and the
        current connection state.
        '''

        url = 'http://' + self.ip + '/api/connection'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def connectPrinter(self, port=None, baudrate=None, printer_profile=None, save=None, autoconnect=None):
        '''
        Instructs OctoPrint to connect to the printer

        port: Optional, specific port to connect to. If not set the current
        portPreference will be used, or if no preference is available auto
        detection will be attempted.

        baudrate: Optional, specific baudrate to connect with. If not set
        the current baudratePreference will be used, or if no preference
        is available auto detection will be attempted.

        printer_profile: Optional, specific printer profile to use for
        connection. If not set the current default printer profile
        will be used.

        save: Optional, whether to save the request's port and baudrate
        settings as new preferences. Defaults to false if not set.

        autoconnect: Optional, whether to automatically connect to the printer
        on OctoPrint's startup in the future. If not set no changes will be
        made to the current configuration.
        '''
        payload = {'command': 'connect'}
        if port is not None:
            payload['port'] = port
        if baudrate is not None:
            payload['baudrate'] = baudrate
        if printer_profile is not None:
            payload['printerProfile'] = printer_profile
        if save is not None:
            payload['save'] = save
        if autoconnect is not None:
            payload['autoconnect'] = autoconnect
        url = 'http://' + self.ip + '/api/connection'
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def disconnect(self):
        '''
        Instructs OctoPrint to disconnect from the printer
        '''

        url = 'http://' + self.ip + '/api/connection'
        payload = {'command': 'disconnect'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++ Printer Operations ++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def getPrinterState(self, exclude=None, history=False, limit=None):
        '''
        Retrieves the current state of the printer
        Returned information includes:
        * temperature information
        * SD state (if available)
        * general printer state
        Temperature information can also be made to include the printer's
        temperature history by setting the history argument.
        The amount of data points to return here can be limited using the limit
        argument.
        Clients can specify a list of attributes to not return in the response
        (e.g. if they don't need it) via the exclude argument.
        '''
        url = 'http://' + self.ip + '/api/printer'
        headers = {'X-Api-Key': self.apiKey}
        payload = {"exclude": exclude, "history": history, "limit": limit}
        response = requests.get(url, params=payload, headers=headers)
        # Handle error exception
        if response.status_code == 409:
            return response.text, response.status_code
        else:
            return response.json(), response.status_code

    def getToolState(self, history=False, limit=None):
        '''
        Retrieves the current temperature data (actual, target and offset) plus
        optionally a (limited) history (actual, target, timestamp) for all of
        the printer's available tools.

        It's also possible to retrieve the temperature history by setting the
        history argument. The amount of returned history data points can be
        limited using the limit argument.
        '''
        url = 'http://' + self.ip + '/api/tool'
        headers = {'X-Api-Key': self.apiKey}
        payload = {"history": history, "limit": limit}
        response = requests.get(url, params=payload, headers=headers)
        temp = response.json()
        return temp

    def getBedState(self, history=False, limit=None):
        '''
        Retrieves the current temperature data (actual, target and offset) plus
        optionally a (limited) history (actual, target, timestamp) for all of
        the printer's available tools.

        It's also possible to retrieve the temperature history by setting the
        history argument. The amount of returned history data points can be
        limited using the limit argument.
        '''
        url = 'http://' + self.ip + '/api/bed'
        headers = {'X-Api-Key': self.apiKey}
        payload = {"history": history, "limit": limit}
        response = requests.get(url, params=payload, headers=headers)
        temp = response.json()
        return temp

    def jog(self, x=None, y=None, z=None, absolute=False, speed=None):

        '''
        Jogs the print head (relatively or absolutly) by a defined amount in one or more
        axes. Additional parameters are:
        x: Optional. Amount to jog print head on x axis, must be a valid
        number corresponding to the distance to travel in mm.
        y: Optional. Amount to jog print head on y axis, must be a valid
        number corresponding to the distance to travel in mm.
        z: Optional. Amount to jog print head on z axis, must be a valid
        number corresponding to the distance to travel in mm.
        '''
        url = 'http://' + self.ip + '/api/printer/printhead'
        payload = {'command': 'jog', 'absolute': absolute}
        if x != None:
            payload['x'] = x
        if y != None:
            payload['y'] = y
        if z != None:
            payload['z'] = z
        if speed != None:
            payload['speed'] = speed
        print ("jog called" + str(payload))
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def home(self, axes=None):
        '''
        Homes the print head in all of the given axes.
        Additional parameters are:

        axes: A list of axes which to home, valid values are one or more of
        'x', 'y', 'z'. Defaults to all.
        '''
        url = 'http://' + self.ip + '/api/printer/printhead'
        axes = [a.lower()[:1] for a in axes] if axes else ['x', 'y', 'z']
        payload = {"command": "home", "axes": axes}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def feedrate(self, factor):
        '''
        Changes the feedrate factor to apply to the movement's of the axes.

        factor: The new factor, percentage as integer or float (percentage
        divided by 100) between 50 and 200%.
        '''
        url = 'http://' + self.ip + '/api/printer/printhead'
        payload = {'command': 'feedrate', 'factor': factor}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    @classmethod
    def _tool_dict(cls, data):
        if isinstance(data, (int, float)):
            data = (data,)
        if isinstance(data, dict):
            ret = data
        else:
            ret = {}
            for n, thing in enumerate(data):
                ret['tool{}'.format(n)] = thing
        return ret

    def setToolTemperature(self, targets):
        '''
        Sets the given target temperature on the printer's tools.
        Additional parameters:
        targets: Target temperature(s) to set.
        Can be one number (for tool0), list of numbers or dict, where keys
        must match the format tool{n} with n being the tool's index starting
        with 0.
        '''
        url = 'http://' + self.ip + '/api/printer/tool'
        targets = self._tool_dict(targets)
        payload = {"command": "target", 'targets': targets}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def setToolOffsets(self, offsets):
        '''
        Sets the given target temperature on the printer's tools.
        Additional parameters:
        targets: Target temperature(s) to set.
        Can be one number (for tool0), list of numbers or dict, where keys
        must match the format tool{n} with n being the tool's index starting
        with 0.
        '''
        url = 'http://' + self.ip + '/api/printer/tool'
        offsets = self._tool_dict(offsets)
        payload = {"command": "target", 'offsets': offsets}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def selectTool(self, tool):
        '''
        Selects the printer's current tool.
        Additional parameters:

        tool: Tool to select, format tool{n} with n being the tool's index
        starting with 0. Or integer.
        '''
        url = 'http://' + self.ip + '/api/printer/tool'
        if isinstance(tool, int):
            tool = 'tool{}'.format(tool)
        payload = {'command': 'select', 'tool': tool}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def extrude(self, amount):
        '''
        Extrudes the given amount of filament from the currently selected tool

        Additional parameters:

        amount: The amount of filament to extrude in mm.
        May be negative to retract.
        '''
        url = 'http://' + self.ip + '/api/printer/tool'
        payload = {'command': 'extrude', 'amount': amount}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def retract(self, amount):
        '''
        Retracts the given amount of filament from the currently selected tool

        Additional parameters:

        amount: The amount of filament to retract in mm.
        May be negative to extrude.
        '''
        self.extrude(-amount)

    def flowrate(self, factor):
        '''
        Changes the flow rate factor to apply to extrusion of the tool.

        factor: The new factor, percentage as integer or float
        (percentage divided by 100) between 75 and 125%.
        '''
        url = 'http://' + self.ip + '/api/printer/tool'
        payload = {'command': 'flowrate', 'factor': factor}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def setBedTemperature(self, target):
        '''
        Sets the given target temperature on the printer's bed.

        target: Target temperature to set.
        '''
        url = 'http://' + self.ip + '/api/printer/bed'
        payload = {'command': 'target', 'target': target}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def setbedOffset(self, offset):
        '''
        Sets the given temperature offset on the printer's bed.

        offset: Temperature offset to set.
        '''
        url = 'http://' + self.ip + '/api/printer/bed'
        payload = {'command': 'offset', 'offset': offset}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def initialiseSd(self):
        '''
        Initializes the printer's SD card, making it available for use.
        This also includes an initial retrieval of the list of files currently
        stored on the SD card, so after issuing files(location=sd) a retrieval
        of the files on SD card will return a successful result.

        If OctoPrint detects the availability of a SD card on the printer
        during connection, it will automatically attempt to initialize it.
        '''
        url = 'http://' + self.ip + '/api/printer/sd'
        payload = {'command': 'init'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def sdRefresh(self):
        '''
        Refreshes the list of files stored on the printer''s SD card.
        Will raise a 409 Conflict if the card has not been initialized yet
        with sd_init().
        '''
        url = 'http://' + self.ip + '/api/printer/sd'
        payload = {'command': 'refresh'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def sdRelease(self):
        '''
        Releases the SD card from the printer. The reverse operation to init.
        After issuing this command, the SD card won't be available anymore,
        hence and operations targeting files stored on it will fail.
        Will raise a 409 Conflict if the card has not been initialized yet
        with sd_init().
        '''
        url = 'http://' + self.ip + '/api/printer/sd'
        payload = {'command': 'release'}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def getSdState(self):
        '''
        Retrieves the current state of the printer's SD card.

        If SD support has been disabled in OctoPrint's settings,
        a 404 Not Found is risen.
        '''
        url = 'http://' + self.ip + '/api/printer/sd'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def gcode(self, command):
        '''
        Sends any command to the printer via the serial interface.
        Should be used with some care as some commands can interfere with or
        even stop a running print job.

        command: A single string command or command separated by newlines
        or a list of commands
        '''
        try:
            commands = command.split('\n')
        except AttributeError:
            # already an iterable
            commands = list(command)
        url = 'http://' + self.ip + '/api/printer/command'
        payload = {'commands': commands}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)

    def getSoftwareUpdateInfo(self):
        '''
        get information from the software update API about software module versions, ad if updates are available
        :return:
        '''
        url = 'http://' + self.ip + '/plugin/softwareupdate/check'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def performSoftwareUpdate(self,force = False):
        url = 'http://' + self.ip + '/plugin/softwareupdate/update'
        payload = {'force': str(force).lower()}
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        requests.post(url, data=json.dumps(payload), headers=headers)


    def isFailureDetected(self):
        url = 'http://' + self.ip + '/plugin/Julia2018PrintRestore/isFailureDetected'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def restore(self, restore = False):
        url = 'http://' + self.ip + '/plugin/Julia2018PrintRestore/restore'
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        payload = {'restore': restore}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        temp = response.json()
        return temp

    def getPrintRestoreSettings(self):
        url = 'http://' + self.ip + '/plugin/Julia2018PrintRestore/getSettings'
        headers = {'X-Api-Key': self.apiKey}
        response = requests.get(url, headers=headers)
        temp = response.json()
        return temp

    def savePrintRestoreSettigns(self, restore = False, enabled = True, interval = 1):
        url = 'http://' + self.ip + '/plugin/Julia2018PrintRestore/saveSettings'
        headers = {'content-type': 'application/json', 'X-Api-Key': self.apiKey}
        payload = {'restore': restore, "interval" : interval, "enabled": enabled}
        requests.post(url, data=json.dumps(payload), headers=headers)


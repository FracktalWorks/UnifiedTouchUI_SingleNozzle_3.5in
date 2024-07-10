from PyQt5 import QtCore
from MainUIClass.decorators import run_async
from MainUIClass.config import ip, apiKey
import random
import uuid
import json
import websocket
import requests
import time
import threading
from logger import *
import dialog


class QtWebsocket(QtCore.QThread):
    '''
    https://pypi.python.org/pypi/websocket-client
    https://wiki.python.org/moin/PyQt/Threading,_Signals_and_Slots
    '''

    z_home_offset_signal = QtCore.pyqtSignal(str)
    temperatures_signal = QtCore.pyqtSignal(dict)
    status_signal = QtCore.pyqtSignal(str)
    print_status_signal = QtCore.pyqtSignal('PyQt_PyObject')
    update_started_signal = QtCore.pyqtSignal(dict)
    update_log_signal = QtCore.pyqtSignal(dict)
    update_log_result_signal = QtCore.pyqtSignal(dict)
    update_failed_signal = QtCore.pyqtSignal(dict)
    connected_signal = QtCore.pyqtSignal()
    filament_sensor_triggered_signal = QtCore.pyqtSignal(dict)
    firmware_updater_signal = QtCore.pyqtSignal(dict)
    z_probe_offset_signal = QtCore.pyqtSignal(str)
    z_probing_failed_signal = QtCore.pyqtSignal()

    def __init__(self):
        print("Starting init of websocket.")
        super(QtWebsocket, self).__init__()

        url = "ws://{}/sockjs/{:0>3d}/{}/websocket".format(
            ip,  # host + port + prefix, but no protocol
            random.randrange(0, stop=999),  # server_id
            uuid.uuid4()  # session_id
        )

        self.stop_event = threading.Event()
        self.heartbeat_checker = HeartbeatChecker(self, self.stop_event)

        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

    def run(self):
        self.ws.run_forever()

    def send(self, data):
        payload = '["' + json.dumps(data).replace('"', '\\"') + '"]'
        self.ws.send(payload)

    def authenticate(self):
        print("Starting handshake in authenticate method.")
        # perform passive login to retrieve username and session key for API key
        url = 'http://' + ip + '/api/login'
        headers = {'content-type': 'application/json', 'X-Api-Key': apiKey}
        payload = {"passive": True}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        data = response.json()

        # prepare auth payload
        auth_message = {"auth": "{name}:{session}".format(**data)}

        # send it
        self.send(auth_message)

    def on_message(self, ws, message):
        message_type = message[0]
        if message_type == "h":
            # "heartbeat" message
            self.heartbeat_checker.update_heartbeat_time()
            return
        elif message_type == "o":
            # "open" message
            return
        elif message_type == "c":
            # "close" message
            return

        message_body = message[1:]
        if not message_body:
            return
        data = json.loads(message_body)[0]

        if message_type == "m":
            data = [data, ]

        if message_type == "a":
            self.process(data)


    @run_async
    def process(self, data):
        # print(json.dumps(data, indent=4))
        if "event" in data:
            if data["event"]["type"] == "Connected":
                self.connected_signal.emit()
                print("connected")

        if "plugin" in data:
            if data["plugin"]["plugin"] == 'Julia2018FilamentSensor':
                 self.filament_sensor_triggered_signal.emit(data["plugin"]["data"])

            if data["plugin"]["plugin"] == 'JuliaFirmwareUpdater':
                self.firmware_updater_signal.emit(data["plugin"]["data"])

            elif data["plugin"]["plugin"] == 'softwareupdate':
                if data["plugin"]["data"]["type"] == "updating":
                    self.update_started_signal.emit(data["plugin"]["data"]["data"])
                elif data["plugin"]["data"]["type"] == "loglines":
                    self.update_log_signal.emit(data["plugin"]["data"]["data"]["loglines"])
                elif data["plugin"]["data"]["type"] == "restarting":
                    self.update_log_result_signal.emit(data["plugin"]["data"]["data"]["results"])
                elif data["plugin"]["data"]["type"] == "update_failed":
                    self.update_failed_signal.emit(data["plugin"]["data"]["data"])

        if "current" in data:
            if data["current"]["messages"]:
                for item in data["current"]["messages"]:
                    if 'M206' in item: #response to M503, send current Z offset value
                        self.z_home_offset_signal.emit(item[item.index('Z') + 1:].split(' ', 1)[0])
                    # if 'Count' in item:  # gets the current Z value, uses it to set Z offset
                    #     self.emit(QtCore.SIGNAL('SET_Z_HOME_OFFSET'), item[item.index('Z') + 2:].split(' ', 1)[0],
                    #               False)
                    # if 'Count' in item:  # can get thris throught the positionUpdate event
                    #     self.set_z_tool_offset_signal.emit(item[item.index('Z') + 2:].split(' ', 1)[0],
                    #               False)
                    # if 'M218' in item:
                    #     self.tool_offset_signal.emit(item[item.index('M218'):])
                    
                    if 'M851' in item:
                        self.z_probe_offset_signal.emit(item[item.index('Z') + 1:].split(' ', 1)[0])
                    if 'PROBING_FAILED' in item:
                        self.z_probing_failed_signal.emit()

            if data["current"]["state"]["text"]:
                self.status_signal.emit(data["current"]["state"]["text"])

            fileInfo = {"job": data["current"]["job"], "progress": data["current"]["progress"]}
            if fileInfo['job']['file']['name'] is not None:
                self.print_status_signal.emit(fileInfo)
            else:
                self.print_status_signal.emit(None)

            def temp(data, tool, temp):
                try:
                    if tool in data["current"]["temps"][0]:
                        return data["current"]["temps"][0][tool][temp]
                except:
                    pass
                return 0

            if data["current"]["temps"] and len(data["current"]["temps"]) > 0:
                try:
                    temperatures = {'tool0Actual': temp(data, "tool0", "actual"),
                                    'tool0Target': temp(data, "tool0", "target"),
                                    'bedActual': temp(data, "bed", "actual"),
                                    'bedTarget': temp(data, "bed", "target")}
                    self.temperatures_signal.emit(temperatures)
                except KeyError:
                    # temperatures = {'tool0Actual': data["current"]["temps"][0]["tool0"]["actual"],
                    #                 'tool0Target': data["current"]["temps"][0]["tool0"]["target"],
                    #                 'bedActual': data["current"]["temps"][0]["bed"]["actual"],
                    #                 'bedTarget': data["current"]["temps"][0]["bed"]["target"]}
                    pass
                # self.emit(QtCore.SIGNAL('TEMPERATURES'), temperatures)

    def on_open(self,ws):
        self.authenticate()
        self.heartbeat_checker.start()

    def on_close(self, ws):
        pass

    def on_error(self, ws, error):
        print(error)
        pass

    def reconnect(self):
        self.stop_event.set()
        self.ws.close()
        self.start()


class HeartbeatChecker(threading.Thread):
    def __init__(self, ws, stop_event):
        super().__init__()
        self.ws = ws
        self.stop_event = stop_event
        self.last_heartbeat_time = None
        self.start_time = time.time()

    def run(self):
        try:
            while not self.stop_event.is_set():
                if self.last_heartbeat_time is not None:
                    time_since_last_heartbeat = time.time() - self.last_heartbeat_time
                    if time_since_last_heartbeat > 300: #5 Minutes
                        print("No heartbeat received for 60 seconds. Reestablishing connection.")
                        self.ws.reconnect()
                    
                time.sleep(5)  # Check every 5 seconds
        except Exception as e:
            error_message = f"Error in Heart beat checker: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def update_heartbeat_time(self):
        self.last_heartbeat_time = time.time()


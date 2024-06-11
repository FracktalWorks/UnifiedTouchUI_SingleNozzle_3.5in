 Julia TouchUI
==================
Touch UI for Julia 2022 based on `Python3` and  `PyQt5`

## Development Requiements:
see https://github.com/FracktalWorks/Julia-Touch-UI-Documentation

[ A simple getting started guide](https://nikolak.com/pyqt-qt-designer-getting-started/)


1. PyQt5 
2. Qt Designer 5 with pyuic5 ( requred to edit .ui file and generate .py file)
3. Websocket client ( pip install websocket-client )
4. other dependencies that "Main.py" needs (see it's headers)


## Running/Executing:

**Octoprint needs to be running in order for the Touch UI to work, since it uses octoprint's api functionality**

1. point the "ip"  and "apiKey" to where Octoprint is living. Point it to the local host in case it is running on the same system
2. in case of running it on anything other than a raspberry pi, disable the raspberry pi option


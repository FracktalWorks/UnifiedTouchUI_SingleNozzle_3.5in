from PyQt5 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

textedit = _fromUtf8("""
    background-color: rgb(255, 255, 255);
""")

printer_status_green = _fromUtf8("""
    border: 1px solid rgb(87, 87, 87);
    border-radius: 10px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:0, y2:0.534,
                                      stop:0 rgba(130, 203, 117, 255),
                                      stop:1 rgba(66, 191, 85, 255));
""")

printer_status_red = _fromUtf8("""
    border: 1px solid rgb(87, 87, 87);
    border-radius: 10px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0.517, x2:0, y2:0.512, 
                                      stop:0 rgba(255, 28, 35, 255),
                                      stop:1 rgba(255, 68, 74, 255));
""")

printer_status_amber = _fromUtf8("""
    border: 1px solid rgb(87, 87, 87);
    border-radius: 10px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:0, y2:0.54, 
                                      stop:0 rgba(255, 211, 78, 255),
                                      stop:1 rgba(219, 183, 74, 255));
""")

printer_status_blue = _fromUtf8("""
    border: 1px solid rgb(87, 87, 87);
    border-radius: 10px;
    background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:0, y2:0.54,
                                      stop:0 rgba(74, 183, 255, 255),
                                      stop:1 rgba(53, 173, 242, 255));
""")

bar_heater_cold = _fromUtf8("""
    QProgressBar::chunk {
        border-radius: 5px;
        background-color: qlineargradient(spread:pad, x1:0.517, y1:0, x2:0.522, y2:0,
                                          stop:0.0336134 rgba(74, 183, 255, 255),
                                          stop:1 rgba(53, 173, 242, 255));
    }

    QProgressBar {
        border: 1px solid white;
        border-radius: 5px;
    }
""")

bar_heater_heating = _fromUtf8("""
    QProgressBar::chunk {
        background-color: qlineargradient(spread:pad, x1:0.492, y1:0, x2:0.487, y2:0,
                                          stop:0 rgba(255, 28, 35, 255),
                                          stop:1 rgba(255, 68, 74, 255));
        border-radius: 5px;
    }

    QProgressBar {
        border: 1px solid white;
        border-radius: 5px;
    }
""")

msgbox = _fromUtf8("""
    QPushButton {
        border: 1px solid rgb(87, 87, 87);
        background-color: qlineargradient(spread: pad, x1: 0, y1: 1, x2: 0, y2: 0.188, stop: 0 rgba(180, 180, 180, 255), stop: 1 rgba(255, 255, 255, 255));
        height: 50px;
        width: 100px;
        border-radius: 5px;
        font: 14pt "Gotham";
    }

    QPushButton: pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,	stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QPushButton: focus {
        outline: none;
    }

    QLabel {
        margin-top: 20px;
        margin-bottom: 20px;
    }
""")

msgbox_icon = _fromUtf8("""
    margin-top: 15px;
    margin-bottom: 5px;
    margin-left: 10px;
""")

msgbox_label = _fromUtf8("""
    margin-top: 5px;
    margin-bottom: 5px;
    margin-right: 10px;
""")

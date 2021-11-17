import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton
from PySide2 import QtCore


UI_FILE_PATH = "pyaacrl-gui-main.ui"


class Window:
    def __init__(self):
        file = QtCore.QFile(UI_FILE_PATH)
        file.open(QtCore.QFile.ReadOnly)

        self.window = QUiLoader().load(file)


        file.close()

        self.connect_signals()

    def connect_signals(self):
        self.window.button_pick_library.clicked.connect(self.pick_library)

    def pick_library(self):
        path_to_file, _ = QFileDialog.getOpenFileName(
            self.window,
            filter="Music files (*.mp3 *.wav)"
        )
        
        a = self.window.label_library_path
        a.setText(f'<b>Loaded:</b> {path_to_file}')
        a.setEnabled(True)



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    
    app = QApplication()

    w = Window()
    w.window.show()
    sys.exit(app.exec_())
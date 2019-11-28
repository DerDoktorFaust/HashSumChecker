from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import *
import sys
import hashlib
from gui.main_window import Ui_MainWindow

FILE_TO_HASH = '' #global variable containing absolute path of file hash-check

class MainWindow(QMainWindow, Ui_MainWindow):
    """Initializes GUI and provides main functionality"""

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Two Line Edit widgets added here instead of main_window to enable drag and drop
        self.input_file_line = LineEditDragWidget(self.centralwidget)
        self.input_file_line.setGeometry(QtCore.QRect(280, 60, 471, 21))
        self.input_file_line.setObjectName("input_file_line")
        self.provided_hash_line = LineEditDragWidget(self.centralwidget)
        self.provided_hash_line.setGeometry(QtCore.QRect(280, 160, 471, 21))
        self.provided_hash_line.setObjectName("provided_hash_line")

        self.line_edit_fields = [self.results_line, self.computed_hash_line, self.input_file_line, self.provided_hash_line]
        self.radio_button_fields = [self.sha1_radio_button, self.sha256_radio_button, self.md5_radio_button]

        self.browse_file_button.clicked.connect(self.browse_files)
        self.compare_hashes_button.clicked.connect(self.compare_hashes)
        self.reset_button.clicked.connect(self.reset)
        self.exit_button.clicked.connect(self.exit_app)



    @pyqtSlot()
    def browse_files(self):
        global FILE_TO_HASH
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        # file dialogue is "getOpenFileName" not "getOpenFileNames" ===> only one file allowed
        new_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select File to Compare", "", "All Files(*)",
                                                              options=options)
        if new_file:  # check to make sure file was selected
            FILE_TO_HASH = new_file
            self.input_file_line.setText(FILE_TO_HASH)

    @pyqtSlot()
    def compare_hashes(self):
        comparison = self.provided_hash_line.text().strip()

        try:

            if self.md5_radio_button.isChecked():
                original_file_hash = hashlib.md5(open(FILE_TO_HASH,'rb').read()).hexdigest()
                self.computed_hash_line.setText(original_file_hash)
            elif self.sha1_radio_button.isChecked():
                original_file_hash = hashlib.sha1(open(FILE_TO_HASH, 'rb').read()).hexdigest()
                self.computed_hash_line.setText(original_file_hash)
            elif self.sha256_radio_button.isChecked():
                original_file_hash = hashlib.sha256(open(FILE_TO_HASH, 'rb').read()).hexdigest()
                self.computed_hash_line.setText(original_file_hash)
            else:
                failure_message = QtWidgets.QMessageBox.warning(
                    None, "Error", f"Please select a hash type!")
                return #return so rest of function does not cause crash

            if original_file_hash == comparison:
                self.results_line.setText("Success: The hashes match and the file is safe!")
            else:
                self.results_line.setText("Warning: Files do not match!!!")

        except FileNotFoundError: #will also catch a blank field for the input file
            failure_message = QtWidgets.QMessageBox.warning(
                None, "Error", f"Please provide all information!")
            return

    @pyqtSlot()
    def reset(self):
        for field in self.line_edit_fields:
            field.clear()
        for button in self.radio_button_fields:
            self.md5_radio_button.setChecked(False)
            button.setChecked(False)

    @pyqtSlot()
    def exit_app(self):
        QtCore.QCoreApplication.instance().quit()


class LineEditDragWidget(QtWidgets.QLineEdit):
    """Creates a line edit widget that allows user to drag and drop a
    file into the widget area to add a file."""
    def __init__(self, parent):
        super(LineEditDragWidget, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(LineEditDragWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(LineEditDragWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        global FILE_TO_HASH
        test_list = [] #used to ensure that only one file is added
        if event.mimeData().hasUrls():
            for file in event.mimeData().urls():
                test_list.append(file)
            if len(test_list) == 1: #ensure only one file is added
                FILE_TO_HASH = event.mimeData().urls()[0].path()
                self.setText(FILE_TO_HASH)
        else:
            super(LineEditDragWidget, self).dropEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

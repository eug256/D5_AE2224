import sys
import vallenae as vae
import os
import pyqtgraph as pg
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import *
import yaml

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        try:
            with open('settings.yml', 'r') as file:
                results = yaml.safe_load(file)
            self._tradb_file_location = results['tradb']
            self._pridb_file_location = results['pridb']
        except FileNotFoundError:
            with open('settings.yml', 'w') as file:
                databases = {
                    'tradb': None,
                    'pridb': None
                }
                yaml.dump(databases, file, sort_keys=False)


        # Create widgets
        self._open_files_path = ''
        frame_style = QFrame.Sunken | QFrame.Panel

        self.edit = QLineEdit()
        self.button = QPushButton("Show TRAI")
        self.table = QTableWidget()
        self.graph = pg.PlotWidget()
        self._open_file_name_label = QLabel()
        self._open_file_name_label.setText(self._tradb_file_location)
        self._open_file_name_label.setFrameStyle(frame_style)
        self._open_file_name_button = QPushButton("Select tradb file")
        self.style_graph()
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self._open_file_name_button)
        layout.addWidget(self._open_file_name_label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        layout.addWidget(self.graph)
        self.create_empty_table()
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.calculate_trai)
        self._open_file_name_button.clicked.connect(self.set_open_file_name)

    def create_empty_table(self):
        data = ["time", "channel", "param_id", "amplitude", "duration", "energy", "rms", "set_id", "threshold", "rise_time", "signal_strength", "counts"]
        self.table.setRowCount(12)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Data", "Value", "Unit"])
        for (i, name) in enumerate(data):
            data_str = QTableWidgetItem(name)
            self.table.setItem(i, 0, data_str)

    def style_graph(self):
        self.graph.setBackground('w')
        self.pen_main = pg.mkPen(color=(0, 0, 255))
        self.pen_treshold = pg.mkPen(color=(255,0,0), style=Qt.DashLine)
        self.graph.setTitle(f"Amplitude VS Time", color=(0,0,0), size="20px")
        styles = {'color':(0,0,0), 'font-size':'20px'}
        self.graph.setLabel('left', "Amplitude (Unit?)", **styles)
        self.graph.setLabel('bottom', "Time (Unit?)", **styles)
        self.graph.showGrid(x=True, y=True)

    # Calculates parameters
    @Slot()
    def calculate_trai(self):
        HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
        PRIDB = os.path.join(HERE, "databases", "1p12_Ft_25000.pridb")
        TRADB = os.path.join(HERE, "databases", "1p12_Ft_25000.tradb")
        with vae.io.TraDatabase(TRADB) as tradb:
            y, t = tradb.read_wave(self.edit.text())

        self.graph.clear()  
        self.graph.setTitle(f"Amplitude VS Time, TRAI={self.edit.text()}", color=(0,0,0), size="20px")

        pridb = vae.io.PriDatabase(PRIDB)
        df_hits = pridb.iread_hits(query_filter=f"TRAI = {self.edit.text()}")

        for i in df_hits:
            for (index, data_value) in enumerate(i[0:12]):
                data_value_widget = QTableWidgetItem()
                data_value_widget.setData(Qt.DisplayRole, data_value)
                self.table.setItem(index, 1, data_value_widget)
                if index == 8: 
                    self.graph.addLegend()
                    self.graph.plot(t, y, pen=self.pen_main, name="data")
                    self.graph.plot(t, len(t)*[data_value], pen=self.pen_treshold, name="treshold")
                    self.graph.plot(t, len(t)*[-data_value], pen=self.pen_treshold)

    @Slot()
    def set_open_file_name(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select tradb file",
                                                  self._open_file_name_label.text(),
                                                  "Tradb (*.tradb)", "")
        if fileName:
            self._open_file_name_label.setText(fileName)
        self._tradb_file_location = fileName
        with open('settings.yml', 'w') as file:
            databases = {
                'tradb': self._tradb_file_location,
                'pridb': self._pridb_file_location
            }
            yaml.dump(databases, file, sort_keys=False)

if __name__ == '__main__':

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    
    # Run the main Qt loop
    sys.exit(app.exec())
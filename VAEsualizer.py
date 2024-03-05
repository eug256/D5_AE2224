import sys
import vallenae as vae
import os
import math
import pyqtgraph as pg
from PySide6.QtGui import QColor
from PySide6.QtCore import *
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
                self._tradb_file_location = None
                self._pridb_file_location = None


        # Create widgets
        self.create_bunch_of_stuff()
        self.create_empty_table()
        self.create_db_selector()      
        self.create_enter_trai()
        self.create_left_side()
        self.style_graph()
        # Create layout and add widgets
        main_layout = QGridLayout()
        main_layout.addWidget(self._database_select, 0, 0, 1, 4)
        main_layout.addWidget(self.graph, 1, 1)
        main_layout.addWidget(self._left_side, 1, 0)
        main_layout.setColumnStretch(0, 0)
        main_layout.setColumnStretch(1, 20)

        # Set dialog layout
        self.setLayout(main_layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.calculate_trai)
        self._open_tradb_button.clicked.connect(self.set_open_tradb)
        self._open_pridb_button.clicked.connect(self.set_open_pridb)

    def create_bunch_of_stuff(self):
        frame_style = QFrame.Sunken | QFrame.Panel
        self.edit = QLineEdit()
        self.button = QPushButton("Show TRAI")
        self.table = QTableWidget()
        self.graph = pg.PlotWidget()
        self._open_tradb_label = QLabel()
        self._open_tradb_label.setText(self._tradb_file_location)
        self._open_tradb_label.setFrameStyle(frame_style)
        self._open_tradb_button = QPushButton("Select tradb file")
        self._open_pridb_label = QLabel()
        self._open_pridb_label.setText(self._pridb_file_location)
        self._open_pridb_label.setFrameStyle(frame_style)
        self._open_pridb_button = QPushButton("Select pridb file")

    def create_empty_table(self):
        data = ["time", "channel", "param_id", "amplitude", "duration", "energy", "rms", "set_id", "threshold", "rise_time", "signal_strength", "counts"]
        unit = ["s", "-", "-", "µV", "µs", "eu", "µV", "-", "µV", "µs", "nVs", "-"]
        self.table.setRowCount(12)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Data", "Value", "Unit"])
        self.table.setFixedWidth(350)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        for (i, name) in enumerate(data):
            data_str = QTableWidgetItem(name)
            self.table.setItem(i, 0, data_str)
        for (i, unit) in enumerate(unit):
            unit_str = QTableWidgetItem(unit)
            self.table.setItem(i, 2, unit_str)

    def create_db_selector(self):
        self.create_pridb_box()
        self.create_tradb_box()
        self._database_select = QGroupBox("Select database files")
        layout = QHBoxLayout()
        layout.addWidget(self._pridb_box)
        #layout.addWidget(self._open_pridb_label)
        layout.addWidget(self._tradb_box)
        #layout.addWidget(self._open_tradb_label)
        self._database_select.setLayout(layout)

    def create_pridb_box(self):
        self._pridb_box = QGroupBox("")
        layout = QVBoxLayout()
        layout.addWidget(self._open_pridb_button)
        layout.addWidget(self._open_pridb_label)
        self._pridb_box.setLayout(layout)

    def create_tradb_box(self):
        self._tradb_box = QGroupBox("")
        layout = QVBoxLayout()
        layout.addWidget(self._open_tradb_button)
        layout.addWidget(self._open_tradb_label)
        self._tradb_box.setLayout(layout)

    def create_db_label(self):
        self._database_label = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(self._open_pridb_label)
        layout.addWidget(self._open_tradb_label)
        self._database_label.setLayout(layout)

    def create_enter_trai(self):
        self._enter_trai = QGroupBox("Enter TRAI")
        layout = QHBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self._enter_trai.setLayout(layout)
        self._enter_trai.setFixedWidth(350)

    def create_left_side(self):
        self._left_side = QGroupBox()
        layout = QVBoxLayout()
        layout.addWidget(self._enter_trai)
        layout.addWidget(self.table)
        self._left_side.setLayout(layout)

    def style_graph(self):
        self.graph.setBackground('w')
        self.pen_main = pg.mkPen(color=(0, 0, 255))
        self.pen_treshold = pg.mkPen(color=(255,0,0), style=Qt.DashLine)
        self.graph.setTitle("Amplitude VS Time", color=(255,0,0), size="20px")
        self.graph.setLabel('left', "<font color='blue'>Amplitude", "V")
        self.graph.setLabel('bottom', "<font color='blue'>Time", "s")
        self.graph.showGrid(x=True, y=True)
        
    def convert_to_db(self, x):
        self.graph.setLabel('left', "<font color='blue'>Amplitude", "dBV")
        for i in range(len(x)):
            try:
                x[i] = 20*math.log(x[i]/1e-6, 10)
            except ValueError:
                x[i] = -100
        return x

    # Calculates parameters
    @Slot()
    def calculate_trai(self):
        PRIDB = self._pridb_file_location
        TRADB = self._tradb_file_location
        trai = int(self.edit.text())
        with vae.io.TraDatabase(TRADB) as tradb:
            y, t = tradb.read_wave(trai)
            print(tradb.columns())

        '''
        temp = []
        for amplitude in y:
            if vae.features.amplitude_to_db(amplitude) != 0:
                temp.append(vae.features.amplitude_to_db(amplitude))
            else:
                temp.append(-1)
        y = temp
        '''
        y = self.convert_to_db(y)
        
        

        self.graph.clear()  
        self.graph.setTitle(f"Amplitude VS Time, TRAI={trai}", color=(255,0,0), size="20px")

        pridb = vae.io.PriDatabase(PRIDB)
        df_hits = pridb.iread_hits(query_filter=f"TRAI = {trai}")
        print(pridb.columns())
        print(pridb.fieldinfo())
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
    def set_open_tradb(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select tradb file",
                                                  self._open_tradb_label.text(),
                                                  "Tradb (*.tradb)", "")
        if fileName:
            self._open_tradb_label.setText(fileName)
        self._tradb_file_location = fileName
        with open('settings.yml', 'w') as file:
            databases = {
                'tradb': self._tradb_file_location,
                'pridb': self._pridb_file_location
            }
            yaml.dump(databases, file, sort_keys=False)

    @Slot()
    def set_open_pridb(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select pridb file",
                                                  self._open_tradb_label.text(),
                                                  "Pridb (*.pridb)", "")
        if fileName:
            self._open_pridb_label.setText(fileName)
        self._pridb_file_location = fileName
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
    form.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
    form.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
    form.setWindowTitle("VAEsualizer")
    form.show()
    
    # Run the main Qt loop
    sys.exit(app.exec())
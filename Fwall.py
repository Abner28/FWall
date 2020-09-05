# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import Galerkin_GUI
import Esteira_GUI

# Design das janelas:

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_simulation = QtWidgets.QAction(MainWindow)
        self.actionNew_simulation.setObjectName("actionNew_simulation")
        self.actionNew_comparison = QtWidgets.QAction(MainWindow)
        self.actionNew_comparison.setObjectName("actionNew_comparison")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setMenuRole(QtWidgets.QAction.NoRole)
        self.actionExit.setObjectName("actionExit")
        self.actionMaximize = QtWidgets.QAction(MainWindow)
        self.actionMaximize.setObjectName("actionMaximize")
        self.actionUnmaximize = QtWidgets.QAction(MainWindow)
        self.actionUnmaximize.setObjectName("actionUnmaximize")
        self.actionMinimize = QtWidgets.QAction(MainWindow)
        self.actionMinimize.setObjectName("actionMinimize")
        self.menuFile.addAction(self.actionNew_simulation)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew_comparison)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionMaximize)
        self.menuView.addAction(self.actionUnmaximize)
        self.menuView.addAction(self.actionMinimize)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.simulationWindow = start_simulation()
        self.comparisonWindow = comparison_wing()

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionMaximize.triggered.connect(MainWindow.showMaximized)
        self.actionUnmaximize.triggered.connect(MainWindow.showNormal)
        self.actionMinimize.triggered.connect(MainWindow.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.actionNew_simulation.triggered.connect(self.new_sim_clicked)
        self.actionNew_comparison.triggered.connect(self.new_com_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FWall"))
        self.menuFile.setTitle(_translate("MainWindow", "FWall"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionNew_simulation.setText(_translate("MainWindow", "New simulation"))
        self.actionNew_simulation.setStatusTip(_translate("MainWindow", "Create a new simulation"))
        self.actionNew_simulation.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save simulation"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save current simulation"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit program"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionMaximize.setText(_translate("MainWindow", "Maximize"))
        self.actionMaximize.setStatusTip(_translate("MainWindow", "Maximize window"))
        self.actionMaximize.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.actionUnmaximize.setText(_translate("MainWindow", "Unmaximize"))
        self.actionUnmaximize.setStatusTip(_translate("MainWindow", "Unmaximize window"))
        self.actionUnmaximize.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.actionMinimize.setText(_translate("MainWindow", "Minimize"))
        self.actionMinimize.setStatusTip(_translate("MainWindow", "Minimize window"))
        self.actionMinimize.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.actionNew_comparison.setText(_translate("MainWindow", "New comparison"))
        self.actionNew_comparison.setStatusTip(_translate("MainWindow", "Create a new comparison"))
        self.actionNew_comparison.setShortcut(_translate("MainWindow", "Ctrl+K"))

    def new_sim_clicked(self):
        self.simulationWindow.show()

    def new_com_clicked(self):
        self.comparisonWindow.show()

# Tela de simulações:

class start_simulation(QtWidgets.QMainWindow):
    def __init__(self):
        super(start_simulation,self).__init__()
        self.resize(720, 670)
        self.setWindowTitle("Simulation Window")
        
        self.label_1 = QtWidgets.QLabel(self)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_4 = QtWidgets.QLabel(self)
        self.label_5 = QtWidgets.QLabel(self)
        self.label_6 = QtWidgets.QLabel(self)
        self.label_7 = QtWidgets.QLabel(self)
        self.label_8 = QtWidgets.QLabel(self)
        self.label_9 = QtWidgets.QLabel(self)
        self.label_10 = QtWidgets.QLabel(self)
        self.label_11 = QtWidgets.QLabel(self)
        self.label_12 = QtWidgets.QLabel(self)
        self.label_13 = QtWidgets.QLabel(self)
        self.runButton = QPushButton("Run",self)
        self.run2Button = QPushButton("Vortex sheet",self)


        self.runButton.move(435,400)
        self.runButton.resize(200,80)
        self.run2Button.move(435,500)
        self.run2Button.resize(200,80)
        

        self.label_1.setText("Parameters")
        self.label_1.move(300,30)
        self.label_1.setFont(QtGui.QFont("times",18))
        self.label_1.adjustSize()

        self.label_2.setText("Number of wings:")
        self.label_2.move(50,105)
        self.label_2.setFont(QtGui.QFont("Arial",12))
        self.label_2.adjustSize()

        self.textbox2 = QLineEdit(self)
        self.textbox2.setFont(QtGui.QFont("times",14))
        self.textbox2.move(200,100)
           
        self.label_3.setText("Wing span [m]:")
        self.label_3.move(50,155)
        self.label_3.setFont(QtGui.QFont("Arial",12))
        self.label_3.adjustSize()

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(200,150)
        self.textbox3.setFont(QtGui.QFont("times",14))
        

        self.label_4.setText("AoA [°]:")
        self.label_4.move(50,210)
        self.label_4.setFont(QtGui.QFont("Arial",12))
        self.label_4.adjustSize()

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(200,205)
        self.textbox4.setFont(QtGui.QFont("times",14))
        

        self.label_5.setText("y-offset [m]:")
        self.label_5.move(50,270)
        self.label_5.setFont(QtGui.QFont("Arial",12))
        self.label_5.adjustSize()

        self.textbox5 = QLineEdit(self)
        self.textbox5.move(200,265)
        self.textbox5.setFont(QtGui.QFont("times",14))
        

        self.label_6.setText("z-offset [m]:")
        self.label_6.move(50,325)
        self.label_6.setFont(QtGui.QFont("Arial",12))
        self.label_6.adjustSize()

        self.textbox6 = QLineEdit(self)
        self.textbox6.move(200,320)
        self.textbox6.setFont(QtGui.QFont("times",14))
        

        self.label_7.setText("Element type:")
        self.label_7.move(50,375)
        self.label_7.setFont(QtGui.QFont("Arial",12))
        self.label_7.adjustSize()

        self.textbox7 = QLineEdit(self)
        self.textbox7.move(200,370)
        self.textbox7.setFont(QtGui.QFont("times",14))
        
        
        self.label_8.setText("Mesh type:")
        self.label_8.move(50,430)
        self.label_8.setFont(QtGui.QFont("Arial",12))
        self.label_8.adjustSize()

        self.textbox8 = QLineEdit(self)
        self.textbox8.move(200,430)
        self.textbox8.setFont(QtGui.QFont("times",14))
        
        
        self.label_9.setText("Want to plot figures together?\n(True/False)")
        self.label_9.move(50,485)
        self.label_9.setFont(QtGui.QFont("Arial",12))
        self.label_9.adjustSize()

        self.textbox9 = QLineEdit(self)
        self.textbox9.move(280,485)
        self.textbox9.resize(60,30)
        self.textbox9.setFont(QtGui.QFont("times",14))
        

        self.label_10.setText("Wing type\n(Planar or Flexibe):")
        self.label_10.move(380,90)
        self.label_10.setFont(QtGui.QFont("Arial",12))
        self.label_10.adjustSize()

        self.textbox10 = QLineEdit(self)
        self.textbox10.move(535,100)
        self.textbox10.setFont(QtGui.QFont("times",14))
        

        self.label_11.setText("Number of elements:")
        self.label_11.move(370,155)
        self.label_11.setFont(QtGui.QFont("Arial",12))
        self.label_11.adjustSize()

        self.textbox11 = QLineEdit(self)
        self.textbox11.move(535,150)
        self.textbox11.setFont(QtGui.QFont("times",14))
        

        self.label_12.setText("r:")
        self.label_12.move(505,210)
        self.label_12.setFont(QtGui.QFont("Arial",12))
        self.label_12.adjustSize()

        self.textbox12 = QLineEdit(self)
        self.textbox12.move(535,205)
        self.textbox12.setFont(QtGui.QFont("times",14))
        
     

        self.label_13.setText("Uinf [m/s]:")
        self.label_13.move(450,260)
        self.label_13.setFont(QtGui.QFont("Arial", 12))

        self.textbox13 = QLineEdit(self)
        self.textbox13.move(535,265)
        self.textbox13.setFont(QtGui.QFont("times",14))
        


        self.runButton.clicked.connect(self.on_click)
        self.runButton.clicked.connect(self.call_Galerkin_def)

        #self.run2Button.clicked.connect(self.on_click)
        self.run2Button.clicked.connect(self.call_Vortex_sheet)



    def on_click(self):

        self.Nwings = int(self.textbox2.text())
        self.span = float(self.textbox3.text())
        self.AoA_user = float(self.textbox4.text())
        self.y_offset_user = float(self.textbox5.text())
        self.z_offset_user = float(self.textbox6.text())
        self.elem_type= self.textbox7.text()
        self.mesh_type = self.textbox8.text()
        self.plot_together= self.textbox9.text()
        self.wing_type = self.textbox10.text()
        self.Nelem = int(self.textbox11.text())
        self.r = float(self.textbox12.text())
        self.Uinf = float(self.textbox13.text())
        return #self.Nwings, self.span, self.AoA_user, self.y_offset_user, self.z_offset_user, self.elem_type, self.mesh_type, self.plot_together, self.wing_type, self.Nelem, self.r, self.Uinf
    
    def call_Galerkin_def(self):
        Galerkin_GUI.call_Galerkin(self.Nwings, self.span, self.AoA_user, self.y_offset_user,
         self.z_offset_user, self.elem_type, self.mesh_type, self.plot_together, self.wing_type, self.Nelem, self.r,self.Uinf)    

    def call_Vortex_sheet(self):
        Esteira_GUI.call_Vortex_sheet(self.Nelem, self.wing_type,self.Nwings)


# Tela de comparações:

class comparison_wing(QtWidgets.QMainWindow):
    """docstring for comparison_wing"""
    def __init__(self):
        super(comparison_wing, self).__init__()
        self.resize(720, 540)
        self.setWindowTitle("Comparison Window")   



            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Aparência:

    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    # RUN:

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sim = start_simulation()
    sys.exit(app.exec_())
    
    




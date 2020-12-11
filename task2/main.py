import life
import sys
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QCheckBox, QApplication, QPushButton, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QColorDialog, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIntValidator

alivecolor = QColor(0, 255, 0)
deadcolor = QColor(255, 255, 255)
framecolor = QColor(255, 255, 255)
cellwidth = 10
colors = {'Dead Cell Color': QColor(255, 255, 255), 'Living Cell Color': QColor(0, 255, 0), 'Frame Color': QColor(255, 255, 255)}

class Cell(QWidget):

    cellToggled = pyqtSignal()

    def __init__(self, x, y):
        
        super().__init__()
        
        self.alive = 0
        self.coordinates = [x, y]

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawCell(qp)
        qp.end()

    def ToggleStatus(self, alive):
        self.alive = alive

    def mousePressEvent(self, event):
        self.cellToggled.emit()
    
    def drawCell(self, qp):

        qp.setPen(colors['Frame Color'])
        qp.setBrush(colors['Living Cell Color'] if self.alive else colors['Dead Cell Color'])
        qp.drawRect(0, 0, cellwidth, cellwidth)

    

class Field(QWidget):

    def __init__(self, x, y, l):
        super().__init__()
        self.game = life.Life(x, y, l) #start up with the 10x10 field, no looping screen
        self.drawCells()
        grid = QGridLayout()
        for i in range(self.game.length()):
            for j in range(self.game.width()):
                grid.addWidget(self.cellmatrix[i][j], i, j)

        self.setLayout(grid)

    def return_length(self):
        return self.game.length()
    def return_width(self):
        return self.game.width()
    
    def paintEvent(self, event):
        grid = QGridLayout()
        for i in range(self.game.length()):
            for j in range(self.game.width()):
                grid.addWidget(self.cellmatrix[i][j], i, j)
        self.setLayout(grid)

    def drawCells(self):
        self.cellmatrix = []
        for i in range(self.game.length()):
            self.cellmatrix.append([])
            for j in range(self.game.width()):
                current_cell = Cell(i, j)
                current_cell.ToggleStatus(self.game.cell_is_alive(i, j))
                current_cell.cellToggled.connect(self.toggle)
                self.cellmatrix[i].append(current_cell)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    
    def checkCells(self):
        for i in range(self.game.length()):
            for j in range(self.game.width()):
                self.cellmatrix[i][j].ToggleStatus(self.game.cell_is_alive(i, j))
    
    def toggle(self):
        sender = self.sender()
        x = sender.coordinates[0]
        y = sender.coordinates[1]
        if self.game.cell_is_alive(x, y):
            self.game.kill_cell(x, y)
        else:
            self.game.enliven_cell(x, y)
        sender.ToggleStatus(not sender.alive)
        self.update()

    def step(self):
        a = self.game.step()
        self.checkCells()
        self.update()
        return a

    def clear(self):
        self.game.clear_field()
        self.checkCells()
        self.update()

class SettingsDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.invitex = "Please write the length of the field here"
        self.invitey = "Please write the width of the field here"
        
        self.intlimiter = QIntValidator()
        self.editx = QLineEdit(self.invitex)
        self.editx.setValidator(self.intlimiter)
        self.edity = QLineEdit(self.invitey)
        self.edity.setValidator(self.intlimiter)
        self.submitbutton = QPushButton("Submit")
        self.submitbutton.clicked.connect(self.submit)
        self.settings = {'field_length': -1, 'field_width': -1}
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.editx)
        layout.addWidget(self.edity)
        layout.addWidget(self.submitbutton)
        
        self.setLayout(layout)
        self.setGeometry(500, 500, 300, 300)
        self.setWindowTitle("Field Size Choice")

    def GetResults(self):
        return self.settings
    
    def submit(self):
        if self.editx.text() != self.invitex:
            self.settings['field_length'] = int(self.editx.text())
        if self.edity.text() != self.invitey:
            self.settings['field_width'] = int(self.edity.text())
        self.done(1)
        

class UserInterface(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.mainfield = Field(10, 10, False)

        self.timer = QBasicTimer()
        self.speed = 100
        self.isRunning = False
        
        self.box1 = QHBoxLayout()
        self.box1.addWidget(self.mainfield)

        self.box2 = QHBoxLayout()
        startbutton = QPushButton("Start")
        pausebutton = QPushButton("Pause")
        stepbutton = QPushButton("One step")
        startbutton.clicked.connect(self.start)
        pausebutton.clicked.connect(self.pause)
        stepbutton.clicked.connect(self.step)
        clearbutton = QPushButton("Clear field")
        clearbutton.clicked.connect(self.clear)
        self.box2.addWidget(clearbutton)
        self.box2.addWidget(startbutton)
        self.box2.addWidget(pausebutton)
        self.box2.addWidget(stepbutton)

        self.settingsbox = QHBoxLayout()
        deadcolorbutton = QPushButton("Dead Cell Color")
        alivecolorbutton = QPushButton("Living Cell Color")
        framecolorbutton = QPushButton("Frame Color")
        deadcolorbutton.clicked.connect(self.color)
        alivecolorbutton.clicked.connect(self.color)
        framecolorbutton.clicked.connect(self.color)
        settingsbutton = QPushButton("Settings")
        settingsbutton.clicked.connect(self.set)
        
        self.settingsbox.addWidget(deadcolorbutton)
        self.settingsbox.addWidget(alivecolorbutton)
        self.settingsbox.addWidget(framecolorbutton)
        self.settingsbox.addWidget(settingsbutton)
        

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.box1)
        self.vbox.addLayout(self.box2)
        self.vbox.addLayout(self.settingsbox)

        self.setLayout(self.vbox)

    def start(self):
        self.isRunning = True
        self.timer.start(self.speed, self)

    def pause(self):
        self.timer.stop()
        self.isRunning = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if not self.step():
                self.pause()
    
    def step(self):
        return self.mainfield.step()

    def clear(self):
        self.mainfield.clear()

    def color(self):
        col = QColorDialog.getColor()
        sender = self.sender()
        global colors
        if col.isValid():
            colors[sender.text()] = col

    def set(self):
        s = SettingsDialog()
        if s.exec_():
            a = s.GetResults()
            x = a['field_length'] if a['field_length'] > 0 else self.mainfield.return_length()
            y = a['field_width'] if a['field_width'] > 0 else self.mainfield.return_width()
            self.mainfield.replaceCells(x, y)
            a = Field(x, y, False)
            self.mainfield.deleteLater()
            self.mainfield = a
            self.box1.addWidget(self.mainfield)
            self.update()
            

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.UI = UserInterface(self)
        self.setCentralWidget(self.UI)
        
        self.setGeometry(0, 0, 1000, 1000)
        self.setWindowTitle('Game of Life')
        
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

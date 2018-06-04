from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap,QColor,QPalette
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import vlc
import sys

RESDIR = "../resources"

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 850, 550)
        self.setWindowTitle('Subeeper')
        self.setWindowIcon(QIcon(RESDIR+"/icon3.png"))
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.stack.addWidget(self.buildLogoPage())
        self.stack.addWidget(self.buildMainPage())
        self.stack.setCurrentIndex(1)
        self.showMaximized()

    def buildLogoPage(self):
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(RESDIR+"/logo.png"))
        self.logo.setAlignment(Qt.AlignCenter)
        return self.logo

    def buildMainPage(self):
        self.main = QWidget()
        mainLayout = QVBoxLayout()
        self.main.setLayout(mainLayout)
        mainLayout.addWidget(self.buildMaintop())
        self.subeditor = QPlainTextEdit()
        self.subeditor.setMaximumHeight(100)
        mainLayout.addWidget(self.subeditor)
        return self.main

    def buildMaintop(self):
        self.maintop = QWidget()
        maintopLayout = QHBoxLayout()
        self.maintop.setLayout(maintopLayout)
        maintopLayout.addWidget(self.buildVideoPlayer())
        maintopLayout.addWidget(self.buildSidePannel())
        return self.maintop

    def buildVideoPlayer(self):
        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            from PyQt5.QtWidgets import QMacCocoaViewContainer
            self.videoframe = QMacCocoaViewContainer(0)
        else:
            self.videoframe = QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QPalette.Window,
                               QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        return self.videoframe


    def buildSidePannel(self):
        self.sidepannel = QWidget()
        self.sidepannel.setMaximumWidth(400)
        lay1 = QHBoxLayout()
        widget2 = QWidget()
        lay2 = QVBoxLayout()
        lay2.setAlignment(Qt.AlignBottom)
        widget2.setLayout(lay2)
        self.slider = QSlider(Qt.Vertical)
        lay1.addWidget(self.slider)
        lay1.addWidget(widget2)
        self.sidepannel.setLayout(lay1)
        self.startTimer = self.buildTimer()
        self.startTimer.display("00:00:32.123")
        self.endTimer = self.buildTimer()
        self.endTimer.display("00:01:02.102")
        lay2.addWidget(self.startTimer)
        lay2.addWidget(self.endTimer)
        lay2.addWidget(self.buildButtons())
        return self.sidepannel

    def buildTimer(self):
        timer = QLCDNumber()
        timer.setSegmentStyle(QLCDNumber.Filled)
        timer.setDigitCount(12)
        timer.setMinimumHeight(40)
        return timer

    def buildButtons(self):
        w = QWidget()
        lay = QHBoxLayout()
        w.setLayout(lay)
        self.playbutton = QPushButton("Play")
        self.nextbutton = QPushButton(">>")
        self.prewbutton = QPushButton("<<")
        lay.addWidget(self.prewbutton)
        lay.addWidget(self.playbutton)
        lay.addWidget(self.nextbutton)
        return w


    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

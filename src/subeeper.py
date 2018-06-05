#####################################################
#                   [subeeper.py]                   #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap,QColor,QPalette
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import controller as cnt
import time
import vlc
import sys

# path to resources folder
RESDIR = "../resources"

# path to a file with IBM Watson Speech-to-Text API
# credentials (separated by lines)
IBMCRED = "~/IBMSTT.cred"

# path to a file with Microsoft Speech-to-Text API
# credentials (separated by lines)
MICROSOFTCRED = "~/MICROSOFTSTT.cred"

# the frame which contains GUI
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
        self.preprocessPage = PreprocessPage(self)
        self.loadPage = LoadPage(self)
        self.editPage = EditPage(self)
        self.stack.addWidget(self.loadPage)
        self.stack.addWidget(self.preprocessPage)
        self.stack.addWidget(self.editPage)
        self.stack.setCurrentIndex(0)
        # self.showMaximized()
        self.show()



class LoadPage(QWidget):
    trigger = pyqtSignal(['QString'])
    def __init__(self,parent):
        super(LoadPage,self).__init__()
        self.parent = parent
        self.initUI()
        self.trigger.connect(parent.preprocessPage.setVideo)

    def initUI(self):
        lay = QVBoxLayout()
        self.setLayout(lay)
        logo = QLabel()
        logo.setPixmap(QPixmap(RESDIR+"/logo.png"))
        logo.setAlignment(Qt.AlignCenter)
        lay.addStretch(1)
        lay.addWidget(logo)
        lay.addStretch(1)
        buttons_menu = QWidget()
        btnlay = QHBoxLayout()
        buttons_menu.setLayout(btnlay)
        lay.addWidget(buttons_menu)
        btn_video = QPushButton("Load Video")
        btn_project = QPushButton("Load Project")
        btn_exit = QPushButton("Exit")
        btn_video.clicked.connect(self.load_video)
        btn_project.clicked.connect(self.load_project)
        btn_exit.clicked.connect(QCoreApplication.quit)
        btnlay.addStretch(1)
        btnlay.addWidget(btn_video)
        btnlay.addWidget(btn_project)
        btnlay.addWidget(btn_exit)
        btnlay.addStretch(1)

    def load_video(self):
        self.parent.stack.setCurrentIndex(1)
        video = "/home/d33pblue/Documenti/uni/CSproject/300/300.mp4"
        self.trigger.emit(video)

    def load_project(self):
        self.parent.stack.setCurrentIndex(2)



class PreprocessPage(QWidget):
    def __init__(self,parent):
        super(PreprocessPage,self).__init__()
        self.parent = parent
        self.initUI()
        self.ppunit = cnt.PreprocessUnit(self)

    def initUI(self):
        lay = QVBoxLayout()
        self.setLayout(lay)
        title = QLabel("Preprocess video")
        font = title.font()
        font.setPointSize(30)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        self.progbar = QProgressBar()
        self.progbar.setMaximum(100)
        self.progbar.setMinimum(0)
        self.progbar.setValue(0)
        self.videoname = QLabel("video..")
        self.videoname.setAlignment(Qt.AlignCenter)
        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.startTask)
        lay.addStretch(1)
        lay.addWidget(title)
        lay.addWidget(self.videoname)
        lay.addWidget(self.btn_start)
        lay.addWidget(self.progbar)
        self.ck_audioext = self.addTaskLabel(lay,"Audio Extraction____")
        self.ck_ibm = self.addTaskLabel(lay,"IBM API_____________")
        self.ck_chunks = self.addTaskLabel(lay,"Making chunks______")
        self.ck_microsoft = self.addTaskLabel(lay,"Microsoft API________")
        lay.addStretch(1)

    def setVideo(self,video):
        self.video = video
        self.processed = False
        self.videoname.setText("Video: "+video)

    def startTask(self,video):
        if not self.processed:
            self.btn_start.setEnabled(False)
            self.ppunit.preprocess(self.video)


    def addTaskLabel(self,layout,text):
        w = QWidget()
        lay = QHBoxLayout()
        w.setLayout(lay)
        checkbox = QCheckBox()
        checkbox.setEnabled(False)
        lay.addStretch(1)
        lay.addWidget(checkbox)
        lay.addWidget(QLabel(text))
        lay.addStretch(1)
        layout.addWidget(w)
        return checkbox



class EditPage(QWidget):
    def __init__(self,parent):
        super(EditPage,self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.buildMaintop())
        self.subeditor = QPlainTextEdit()
        self.subeditor.setMaximumHeight(100)
        mainLayout.addWidget(self.subeditor)

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

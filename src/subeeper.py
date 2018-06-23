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
import configparser
import time
import vlc
import sys
import pickle

# the frame which contains GUI
class MainWindow(QMainWindow):
    def __init__(self,config):
        super(MainWindow,self).__init__()
        self.config = config
        self.RESDIR = self.config["DEFAULT"]["resdir"]
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 850, 550)
        self.setWindowTitle('Subeeper')
        self.setWindowIcon(QIcon(self.RESDIR+"/icon3.png"))
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
        self.trigger.connect(parent.preprocessPage.startTask)

    def initUI(self):
        lay = QVBoxLayout()
        self.setLayout(lay)
        logo = QLabel()
        logo.setPixmap(QPixmap(self.parent.RESDIR+"/logo.png"))
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
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose Video",
                QDir.homePath(),filter="Video Files (*.mp4 *.avi)")
        if fileName != None and fileName != "":
            self.trigger.emit(fileName)
        else:
            self.parent.stack.setCurrentIndex(0)

    def load_project(self):
        self.parent.stack.setCurrentIndex(2)



class PreprocessPage(QWidget):
    def __init__(self,parent):
        super(PreprocessPage,self).__init__()
        self.parent = parent
        self.video = ""
        self.initUI()
        self.ppunit = cnt.PreprocessUnit(self,self.parent.config)

    def initUI(self):
        lay = QVBoxLayout()
        self.setLayout(lay)
        title = QLabel("Preprocess video")
        font = title.font()
        font.setPointSize(30)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        barwidg = QWidget()
        lb = QHBoxLayout()
        barwidg.setLayout(lb)
        self.progbar = QProgressBar()
        self.progbar.setMaximum(100)
        self.progbar.setMinimum(0)
        self.progbar.setValue(0)
        self.progbar.setMaximumWidth(500)
        self.progbar.setMinimumWidth(500)
        lb.addStretch(1)
        lb.addWidget(self.progbar)
        lb.addStretch(1)
        self.videoname = QLabel("Choose video..")
        self.videoname.setAlignment(Qt.AlignCenter)
        lay.addStretch(1)
        lay.addWidget(title)
        lay.addWidget(self.videoname)
        lay.addWidget(barwidg)
        self.ck_audioext = self.addTaskLabel(lay,"Audio Extraction____")
        self.ck_ibm = self.addTaskLabel(lay,"IBM API_____________")
        self.ck_chunks = self.addTaskLabel(lay,"Making chunks______")
        self.ck_microsoft = self.addTaskLabel(lay,"Microsoft API________")
        lay.addStretch(1)

    def startTask(self,video):
        self.video = video
        self.videoname.setText("Video: "+video)
        self.ppunit.preprocess(video)


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
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.updateUI)
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
        self.slider.setMaximum(1000)
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
        saveButton = QPushButton("Save project")
        saveButton.clicked.connect(self.save_project)
        lay2.addWidget(saveButton)
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
        self.playbutton.clicked.connect(self.PlayPause)
        self.nextbutton = QPushButton(">>")
        self.nextbutton.clicked.connect(self.nextChunk)
        self.prewbutton = QPushButton("<<")
        lay.addWidget(self.prewbutton)
        lay.addWidget(self.playbutton)
        lay.addWidget(self.nextbutton)
        return w

    def setVideo(self,video):
        self.video = video
        filename = video.getName()
        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)
        # parse the metadata of the file
        self.media.parse()
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
        self.chunkManager = cnt.ChunkManager(self,self.mediaplayer,video)
        self.PlayPause()

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                # self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def updateUI(self):
        # setting the slider to the desired position
        self.slider.setValue(self.mediaplayer.get_position() * 1000)
        self.chunkManager.limitVideo()
        self.chunkManager.updateSubtitles()
        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Play")
        self.chunkManager.setCurrent(0)

    def nextChunk(self):
        self.chunkManager.nextChunk()

    def save_project(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Video",
                QDir.homePath(),filter="Subeeper File (*.subeeper)")
        if fileName == None or fileName == "":
            fileName = "Untitled.subeeper"
        if not fileName.endswith(".subeeper"):
            fileName = fileName+".subeeper"
        with open(fileName,"wb") as f:
            pickle.dump(self.video,f)
        print "FILENAME",fileName
        print "SAVED!"




if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    app = QApplication(sys.argv)
    mw = MainWindow(config)
    sys.exit(app.exec_())

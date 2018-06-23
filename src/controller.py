#####################################################
#                   [controller.py]                 #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
from PyQt5.QtCore import *
import model as mdl
import threading
import json


class PreprocessThread(QThread):
    videodone = pyqtSignal(object)
    def __init__(self,parent,video,ibmUtils,microUtils,audioExtractor,chunkMaker):
        QThread.__init__(self)
        self.parent = parent
        self.videodone.connect(parent.parent.editPage.setVideo)
        self.video = video
        self.ibmUtils = ibmUtils
        self.microUtils = microUtils
        self.audioExtractor = audioExtractor
        self.chunkMaker = chunkMaker

    def __del__(self):
        self.wait()

    def getFakeTranscription(self):
        with open("tmp.json","r") as f:
            return json.load(f)

    def refine(self):
        chunks = self.videochunks.getChunks()
        nc = float(len(chunks))
        videopath = self.videochunks.getName()
        for i,chunk in enumerate(chunks):
            interval = chunk.getInterval()
            start = interval.getBegin().replace(",",".")
            duration = interval.getDurationTimestamp().replace(",",".")
            audiowav = self.audioExtractor.getWav(videopath,start,duration)
            result = self.microUtils.getTranscription(audiowav)
            chunk.setMicrosoftResult(result)
            self.parent.progbar.setValue(75+(i+1)*(25.0/nc))


    def run(self):
        self.parent.progbar.setValue(5)
        audiomp3 = self.audioExtractor.getMp3(self.video)
        self.parent.ck_audioext.setChecked(True)
        self.parent.progbar.setValue(25)
        # transcription = self.ibmUtils.getTranscription(audiomp3)
        transcription = self.getFakeTranscription()
        self.parent.ck_ibm.setChecked(True)
        self.parent.progbar.setValue(50)
        self.videochunks = self.chunkMaker.makeChunks2(self.video,transcription)
        self.parent.ck_chunks.setChecked(True)
        self.parent.progbar.setValue(75)
        self.refine()
        self.goToEdit()

    def goToEdit(self):
        self.parent.parent.stack.setCurrentIndex(2)
        self.videodone.emit(self.videochunks)

class PreprocessUnit:
    def __init__(self,parent,config):
        self.parent = parent
        self.config = config
        self.ibmUtils = mdl.IBMUtils(self.config["DEFAULT"]["ibmcred"])
        self.microUtils = mdl.MicrosoftUtils(self.config["DEFAULT"]["microsoftcred"])
        self.audioExtractor = mdl.AudioExtractor()
        self.chunkMaker = mdl.ChunkMaker(self.config["DEFAULT"]["maxchunksize"])


    def preprocess(self,video):
        t = PreprocessThread(
            self.parent,
            video,
            self.ibmUtils,
            self.microUtils,
            self.audioExtractor,
            self.chunkMaker)
        # t.start()
        t.run()
        print "started preprocess thread"




class ChunkManager:
    def __init__(self,parent,mediaplayer,video):
        self.parent = parent
        self.mediaplayer = mediaplayer
        self.video = video
        self.currentChunk = 0
        self.showedSubs = False

    def limitVideo(self):
        chunk = self.video.getChunk(self.currentChunk)
        t1,t2 = chunk.getTime()
        t = self.mediaplayer.get_time()/1000.0
        if t<t1 or t>t2:
            print t1,t2,t
            if self.mediaplayer.is_playing():
                self.parent.PlayPause()
            self.mediaplayer.set_position(float(t1)/float(self.video.getDuration()))

    def setCurrent(self,i):
        self.currentChunk = i
        self.showedSubs = False

    def updateSubtitles(self):
        subs = self.video.getChunk(self.currentChunk).getSubtitles()
        # print subs
        # self.parent.subeditor.setPlainText(subs)
        if not self.showedSubs:
            self.showedSubs = True
            self.parent.subeditor.setPlainText(subs)


    def nextChunk(self):
        self.currentChunk += 1
        if self.currentChunk >= self.video.getChunksNum():
            self.currentChunk = 0
        self.showedSubs = False
        self.limitVideo()
        self.parent.PlayPause()

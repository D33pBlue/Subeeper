#####################################################
#                   [controller.py]                 #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
from PyQt5.QtCore import QThread
import model as mdl
import threading
import json


class PreprocessThread(QThread):
    def __init__(self,parent,video,ibmUtils,audioExtractor,chunkMaker):
        QThread.__init__(self)
        self.parent = parent
        self.video = video
        self.ibmUtils = ibmUtils
        self.audioExtractor = audioExtractor
        self.chunkMaker = chunkMaker

    def __del__(self):
        self.wait()

    def getFakeTranscription(self):
        with open("tmp.json","r") as f:
            return json.load(f)

    def run(self):
        self.parent.progbar.setValue(5)
        audiomp3 = self.audioExtractor.getMp3(self.video)
        self.parent.ck_audioext.setChecked(True)
        self.parent.progbar.setValue(25)
        transcription = self.ibmUtils.getTranscription(audiomp3)
        # transcription = self.getFakeTranscription()
        self.parent.ck_ibm.setChecked(True)
        self.parent.progbar.setValue(50)
        chunks = self.chunkMaker.makeChunks(self.video,transcription)
        self.parent.ck_chunks.setChecked(True)
        self.parent.progbar.setValue(75)

class PreprocessUnit:
    def __init__(self,parent,config):
        self.parent = parent
        self.config = config
        self.ibmUtils = mdl.IBMUtils(self.config["DEFAULT"]["ibmcred"])
        self.audioExtractor = mdl.AudioExtractor()
        self.chunkMaker = mdl.ChunkMaker(self.config["DEFAULT"]["maxchunksize"])


    def preprocess(self,video):
        t = PreprocessThread(
            self.parent,
            video,
            self.ibmUtils,
            self.audioExtractor,
            self.chunkMaker)
        # t.start()
        t.run()
        print "started preprocess thread"



class ChunkManager:
    def __init__(self):
        pass

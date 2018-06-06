#####################################################
#                   [model.py]                      #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
import ffmpy
import requests

class AudioExtractor:

    def getMp3(self,video):
        outputpath = 'tmpvideo.mp3'
        ff=ffmpy.FFmpeg(
            inputs={video:"-y"},
            outputs={outputpath:None}
        )
        ff.run()
        return outputpath

    def getWav(self,video):
        pass


class Video:
    def __init__(self,name):
        self.chunks = []
        self.name = name

    def addChunk(self,chunk):
        self.chunks.append(chunk)

class Chunk:
    def __init__(self,interval,videoseq):
        self.interval = interval
        self.videoseq = videoseq
        self.text = ""

    def split(self,maxDuration=15):
        pass

class Interval:
    def __init__(self,mill1,mill2):
        if mill2<mill1:
            z = mill1
            mill1 = mill2
            mill2 = z
        self.__mill1 = mill1
        self.__mill2 = mill2

    def getDuration(self):
        return self.__mill2-self.__mill1

    def getBegin(self):
        return "00:..."

    def getEnd(self):
        return "00:..."


class ChunkMaker:
    def __init__(self,maxChunkSize):
        self.maxChunkSize = maxChunkSize

    def makeChunks(self,transcription):
        print transcription


class IBMUtils:
    def __init__(self,credentials):
        with open(credentials,"r") as f:
            self.credentials = f.readlines()

    def getTranscription(self,audiomp3):
        user = self.credentials[0].strip()
        pswd = self.credentials[1].strip()
        urlbase = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
        myurl = urlbase+"?timestamps=true&max_alternatives=3"
        r = requests.post(myurl,
            auth=(user, pswd),
            headers={"Content-Type":"audio/mp3"},
            data=file(audiomp3,'rb').read())
        return r.json()

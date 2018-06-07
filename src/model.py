#####################################################
#                   [model.py]                      #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
import ffmpy
import requests
import vlc

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

    def getName(self):
        return self.name

    def getChunks(self):
        return self.chunks

    def getChunksNum(self):
        return len(self.chunks)

class Chunk:
    def __init__(self,interval,videoseq):
        self.interval = interval
        self.videoseq = videoseq
        self.timestamps = []
        self.text = ""
        self.ibmtext = ""
        self.silent = True

    def getDuration(self):
        return self.interval.getDuration()

    def isSilent(self):
        return self.silent

    def getIbmText(self):
        return self.ibmtext

    def extendEnd(self,t):
        self.interval.extendEnd(t)

    def extendBegin(self,t):
        self.interval.extendBegin(t)

    def getTimestamps(self):
        return self.timestamps

    def getTime(self):
        return self.interval.getBeginTime(),self.interval.getEndTime()

    def setIbmText(self,text,timestamps):
        self.silent = False
        self.ibmtext = text
        self.timestamps = timestamps

    def getCopyWithSeq(self,seq):
        c = Chunk(self.interval,seq)
        c.silent = self.silent
        c.text = self.text
        c.ibmtext = self.ibmtext
        c.timestamps = self.timestamps
        return c

class Interval:
    def __init__(self,mill1,mill2):
        mill1 = float(mill1)
        mill2 = float(mill2)
        if mill2<mill1:
            z = mill1
            mill1 = mill2
            mill2 = z
        self.__mill1 = mill1
        self.__mill2 = mill2

    def __getTimestamp(secs):
        millis = str(int((secs-int(secs))*100))
        if len(millis)<2:
            millis = millis+"0"
        secs = int(secs)
        h = secs/3600
        m = (secs%3600)/60
        s = (secs%3600)%60
        h = str(h)
        m = str(m)
        s = str(s)
        if len(h)<2:
            h = "0"+h
        if len(m)<2:
            m = "0"+m
        if len(s)<2:
            s = "0"+s
        return h+":"+m+":"+s+","+millis

    def extendEnd(self,t):
        t = float(t)
        if t>self.__mill2:
            self.__mill2 = t

    def extendBegin(self,t):
        t = float(t)
        if t<self.__mill1:
            self.__mill1 = t

    def getDuration(self):
        return self.__mill2-self.__mill1

    def getBegin(self):
        return self.__getTimestamp(self.__mill1)

    def getEnd(self):
        return self.__getTimestamp(self.__mill2)

    def getBeginTime(self):
        return self.__mill1

    def getEndTime(self):
        return self.__mill2



class ChunkMaker:
    def __init__(self,maxChunkSize):
        self.maxChunkSize = maxChunkSize

    def makeChunks(self,name,transcription):
        video = Video(name)
        instance = vlc.Instance()
        media = instance.media_new(name)
        media.parse()
        totalDuration = media.get_duration()/1000.0
        sentences = transcription["results"]
        for i,sentence in enumerate(sentences):
            text = sentence["alternatives"][0]["transcript"]
            timestamps = sentence["alternatives"][0]["timestamps"]
            tbegin = timestamps[0][1]
            k = len(timestamps)
            tend = timestamps[k-1][2]
            interval = Interval(tbegin,tend)
            chunk = Chunk(interval,i)
            chunk.setIbmText(text,timestamps)
            video.addChunk(chunk)
        return self.__adjustChunks(video,totalDuration)

    def __fillChunkSpaces(self,chunks,duration):
        t1 = 0
        t2 = 0
        ci = 0
        while t2<duration and ci<len(chunks):
            ct1,ct2 = chunks[ci].getTime()
            if t1<ct1:
                chunk = Chunk(Interval(t1,ct1),ci)
                chunks.insert(ci,chunk)
                ct1,ct2 = t1,ct1
            t1 = ct2
            t2 = t1
            ci += 1
        return chunks

    def __joinSmallSpaces(self,chunks):
        i = 0
        while i<len(chunks):
            chunk = chunks[i]
            if i>0 and i<(len(chunks)-1) and chunk.getDuration()<1.0 and chunk.isSilent():
                t1,t2 = chunk.getTime()
                t = (t1+t2)/2.0
                chunks[i-1].extendEnd(t)
                chunks[i+1].extendBegin(t)
                del chunks[i]
            else:
                i += 1
        return chunks

    def __splitChunk(self,chunk,i):
        duration = chunk.getDuration()
        if float(duration)<float(self.maxChunkSize):
            return [chunk.getCopyWithSeq(i+1)]
        t1,t2 = chunk.getTime()
        if chunk.isSilent():
            chunks = []
            while t1<t2:
                tsep = t1+float(self.maxChunkSize)-0.01
                if tsep>t2:
                    tsep = t2
                interval = Interval(t1,tsep)
                c = Chunk(interval,i)
                chunks.append(c)
                i += 1
                t1 = tsep
            return chunks
        timestamps = chunk.getTimestamps()
        mid = len(timestamps)/2
        text = chunk.getIbmText()
        tmst1 = [timestamps[x] for x in range(mid)]
        tmst2 = [timestamps[x] for x in range(mid,len(timestamps))]
        text1 = " ".join([x[0] for x in tmst1])
        text2 = " ".join([x[0] for x in tmst2])
        intv1 = Interval(tmst1[0][1],tmst1[len(tmst1)-1][2])
        intv2 = Interval(tmst2[0][1],tmst2[len(tmst2)-1][2])
        c1 = Chunk(intv1,i+1)
        c1.setIbmText(text1,tmst1)
        chunks1 = self.__splitChunk(c1,i)
        i = i+len(chunks1)
        c2 = Chunk(intv2,i+1)
        c2.setIbmText(text2,tmst2)
        chunks2 = self.__splitChunk(c2,i)
        return chunks1+chunks2

    def __adjustChunks(self,video,duration):
        finalvideo = Video(video.name)
        chunks = self.__fillChunkSpaces(video.getChunks(),duration)
        chunks = self.__joinSmallSpaces(chunks)
        i = 0
        for chunk in chunks:
            for c in self.__splitChunk(chunk,i):
                finalvideo.addChunk(c)
                i = finalvideo.getChunksNum()
        return finalvideo



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

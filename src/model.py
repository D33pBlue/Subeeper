#####################################################
#                   [model.py]                      #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
import ffmpy

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

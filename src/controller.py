#####################################################
#                   [controller.py]                 #
#   Subeeper                                        #
#   version: 1.0                                    #
#   author: D33pBlue (B.F.)                         #
#   Didactical project for Cognitive Services       #
#####################################################
import model as mdl


class ChunkManager:
    def __init__(self):
        pass

class PreprocessUnit:
    def __init__(self,parent):
        self.parent = parent
        self.audioExtractor = mdl.AudioExtractor()

    def preprocess(self,video):
        self.parent.progbar.setValue(5)
        audiomp3 = self.audioExtractor.getMp3(video)
        self.parent.ck_audioext.setChecked(True)
        self.parent.progbar.setValue(25)

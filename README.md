# Subeeper
Semi-automatic subtitle editor (didactical project for Cognitive Services course)
![alt text](resources/logo.png?raw=true "")

## Abstract
The aim of this project is to implement a
smart subtitle editor for english-language
videos.
Writing subtitles from scratch can be a very
boring activity, because the writer has to
split all speeches into sentences and, for
each of these, he has to identify the time
position inside the video and the text said.
Instead with this project (from now on called
Subeeper), all these operations are done by
the program automatically and the user has
only to check and edit the text suggested for
each sentence, which is (as well as the text)
identified and time located by using audio
captioning and cognitive services APIs.



The program interface need to be very
simple to use. It must give the possibility to
view the video under processing, to have
information about the current time position
and to edit the text which will be shown as
subtitle. A mockup is reported here:
![alt text](resources/mockup2.png?raw=true "")

## Dependencies
- PyQt5 (http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
- VLC media player (https://www.videolan.org/vlc/index.it.html)

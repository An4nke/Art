# importing libraries
import sys
import re

from krita import *
from textblob import TextBlob
from textblob_de import TextBlobDE


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .classes import *
from .svg_vorlagen import *


class DockerLinkGrepper(DockWidget):
    global link
    global html
    global linkdata
    global content
		     
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Url to Art")
        mainWidget = QWidget(self)        
        self.setWidget(mainWidget)        
        
        # add button and layout for button
        layoutForButtons = QHBoxLayout()
        newButton = QPushButton("load text", mainWidget) 
        newButton.move(100, 700) 
        layoutForButtons.addWidget(newButton)

        # label
        nameLabel = QLabel()
        nameLabel.setText('Please input a link:')       
        
        #layoutForButtons.addWidget(nameLabel)

        #input field
        line = QLineEdit()
        line.setPlaceholderText("URL")
        line.setMinimumWidth(300)
        line.setFont(QFont("console",8)) # change font
        layoutForButtons.addWidget(line)
        

        # write some actions
        clicked = 'Button clicked'
        parser = MyHTMLParser()
        content = line.text()
 
        #add a checkbox
        newCheckbox = QCheckBox()
        newCheckbox.setText('realise input')
        layoutForButtons.addWidget(newCheckbox)
        mainWidget.setLayout(layoutForButtons)
        mainWidget.layout().addWidget(newButton)
               
        newButton.clicked.connect(lambda: newCheckbox.setCheckState(2))
        newCheckbox.clicked.connect(lambda: parser.feed(urllib.request.urlopen(content).read().decode()))
        #parser.feed(urllib.request.urlopen(content).read().decode())
        #link = urllib.request.urlopen(content).read().decode()
        linkdata = parser.data

        # language
        language = ''

        # filtering parsed text
        text = ""
        for phrases in linkdata:
            #print (phrases)
            #print('pre: '  + phrases)
            phrases = phrases.rstrip("\n\r+0-9[]()+")
            #print('after: ' + phrases)   
            # skip unwanted characters         
            text = text + phrases
            #print('get: ' + phrases) 
         
        #print(text)
        # create textblob
        blob = TextBlob(text)
        #print(blob.tags)

        for w in blob.words:
            if re.match(r"and", w):
                language = 'en'
            elif re.match(r"und", w):
                language = 'de'

        #print(language)
        if language == 'de':
            blob = TextBlobDE(text)

        sentence_lens = []
        commas = []
        polarity = []

        # print polarity of sentences
        for sentence in blob.sentences:
    
            # length of sentences
            sentence_lens.append(len(sentence))    
  
            # number of commas
            commas.append(len(re.findall(',', str(sentence))))    
    
            # polarity
            polarity.append(sentence.sentiment.polarity)
  
        # init new textforart object
        #art = textforart(self, language, sentence_lens, blob.sentences, commas, polarity)   
   
        # make art out of object

        # width: 0 - 700
        # height: 0 - 700
        # fill color:#000000 # stroke color:#000000
        #stroke = "rgb(" + str(round(125*(1/art.mean_number_commas))) + ", " + str(round(125 - art.min_sentences_polarity)) + ", " + str(round(125 - art.max_sentences_polarity)) + ")"
        #fill = "rgb(" + str(round(125*(1/art.mean_number_commas))) + ", " + str(round(125 - art.min_sentences_polarity)) + ", " + str(round(125 - art.max_sentences_polarity)) + ")"
        #ImageColor.getcolor("#23a9dd", "RGB")

        stroke = "rgb(255, 255, 255)"
        stroke = "rgb(255, 254, 94.)"
        #fill = "rgb(255, 255, 255)"

        # define with of svg
        #heigh = 700- (10000*art.mean_sentences_polarity)
        #width = 700*art.mean_number_commas

        #svg = design_svg(stroke, fill, 700, 700)
        #create_svg(svg)


    def canvasChanged(self, canvas):
       pass
 

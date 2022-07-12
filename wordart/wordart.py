# importing libraries
import sys
import re
import sqlite3
from krita import *
from textblob import TextBlob
from textblob_de import TextBlobDE
from html.parser import HTMLParser
import urllib.request

from PIL import ImageColor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# define class HTML-Parser
class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = []
        self.capture = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'h1'):
            self.capture = True

    def handle_endtag(self, tag):
        if tag in ('p', 'h1'):
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.data.append(data)


# define object/class for analysis
class textforart:
    
    def __init__(self, language = 'en', sentences_lens = [], sentences = [], commas = [], polarity = []):    
       # Sprache
       self.language = language

       # Satz
       self.senctences = sentences
       
       # Sentence lengthes
       self.sentences_lens = sentence_lens       
       
       # Commas
       self.commas = commas
            
       # Bewertung
       self.polarity = polarity
       
       # Komplezität
       self.complexity = ''

       
       # Satzlänge
       self.sentence_number = len(sentences)      
       self.min_sentence_length = min(sentences_lens)
       self.max_sentence_length = max(sentences_lens)
       self.mean_sentence_length = sum(sentences_lens) / len(sentences)  
       
       # Kommas
       self.number_commas = len(commas)
       self.min_number_commas = min(commas)
       self.max_number_commas = max(commas)
       self.mean_number_commas = len(commas)/ len(sentences)   
        
       # Bewertung
       self.sum_sentences_polarity = sum(polarity)
       self.min_sentences_polarity = min(polarity)
       self.max_sentences_polarity = max(polarity)
       self.mean_sentences_polarity = sum(polarity) / len(sentences)
        
       # Schätzer für Komplexität  
       self.max_complexity = 0
       self.min_complexity = 0
       self.mean_complexity = 0   
       
       # signatur Word -> mean purpose
       self.signatur_word = ''   


class DockerLinkGrepper(DockWidget):
    global link
    global html
    global linkdata
    global content
	
	     
    # svg
    def design_svg(strokecolor, fillcolor, width, height):
        trans = str(((800 - height)/2) - 80)   
        print (trans)
        #print(f'''stroke="{strokecolor}" fill="{fillcolor}"''')
        svg = f'''<?xml version="1.0" encoding="iso-8859-1"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg version="1.1" id="Capa_1" x="0px" y="0px"
        	 width="{width}" height="{height}" viewBox="0 0 302.623 302.623" stroke="{strokecolor}" fill="{fillcolor}" style="enable-background:new 0 0 302.623 302.623;"
        	 xml:space="preserve">
      
        <g>
        	<g>
        		<path transform="translate(20, {trans})" d="M148.185,78.801c-88.048,0-144.647,69.607-147.013,72.579c-1.682,2.114-1.54,5.14,0.334,7.076
        			c41.827,43.37,89.258,65.365,140.992,65.365c87.583,0,155.568-62.5,158.423-65.167c1.083-1.013,1.691-2.415,1.701-3.895
        			c0.011-1.486-0.576-2.896-1.648-3.92C251.237,103.045,199.829,78.801,148.185,78.801z M142.487,213.081
        			c-47.292,0-90.941-19.706-129.805-58.573c12.746-14.097,63.71-64.948,135.503-64.948c47.312,0,94.753,21.862,141.068,65.002
        			C273.106,168.02,213.777,213.081,142.487,213.081z"/>
        		<path transform="translate(20, {trans})" d="M110.218,152.691c0,22.656,18.434,41.094,41.095,41.094c22.658,0,41.088-18.438,41.088-41.094
        			s-18.431-41.095-41.088-41.095C128.658,111.602,110.218,130.035,110.218,152.691z"/>
        	</g>
        </g>
        </svg>'''.encode('utf-8')
        return(svg)

    def add_svg(svg):
        clipboard = QGuiApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setData('image/svg+xml', svg)
        clipboard.setMimeData(mime_data)
        Application.action('edit_paste').trigger()
    
    def create_svg(svg):
        app = Krita.instance()
        # Document open?
        #if app.activeDocument():
          #print("aktive document")
          #doc = app.activeDocument() 
        #else:
            #print("create document")
            #doc = app.createDocument(800, 600, 'SVGA Test', 'RGBA', 'U8', '', 120.0)
            #app.activeWindow().addView(doc)
        
        doc = app.createDocument(800, 600, 'SVGA Test', 'RGBA', 'U8', '', 120.0)
        app.activeWindow().addView(doc) 
        layer = doc.createVectorLayer('ColorSVG')
        layer.setName('ColorSVG')
        add_svg(svg)


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
        art = textforart(language, sentence_lens, blob.sentences, commas, polarity)   

        # make art out of object

        # width: 0 - 700
        # height: 0 - 700
        # fill color:#000000 # stroke color:#000000
        stroke = "rgb(" + str(round(125*(1/art.mean_number_commas))) + ", " + str(round(125 - art.min_sentences_polarity)) + ", " + str(round(125 - art.max_sentences_polarity)) + ")"
        fill = "rgb(" + str(round(125*(1/art.mean_number_commas))) + ", " + str(round(125 - art.min_sentences_polarity)) + ", " + str(round(125 - art.max_sentences_polarity)) + ")"
        #ImageColor.getcolor("#23a9dd", "RGB")

        #stroke = "rgb(255, 255, 255)"
        #stroke = "rgb(255, 254, 94.)"
        #fill = "rgb(255, 255, 255)"

        # define with of svg
        heigh = 700- (10000*art.mean_sentences_polarity)
        width = 700*art.mean_number_commas

        svg = design_svg(stroke, fill, 700, 700)
        create_svg(svg)

    def canvasChanged(self, canvas):
       pass
 

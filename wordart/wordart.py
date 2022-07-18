# importing libraries
import sys
import re

from krita import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from html.parser import HTMLParser
import urllib.request
from wordart.classes import *
from wordart.svg_vorlagen import *

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
 
        #add a checkbox
        newCheckbox = QCheckBox()
        newCheckbox.setText('realise input')
        layoutForButtons.addWidget(newCheckbox)
        mainWidget.setLayout(layoutForButtons)
        mainWidget.layout().addWidget(newButton)
            
        #newButton.clicked.connect(lambda: newCheckbox.setCheckState(2))
        newButton.clicked.connect(lambda: newButtonIsClicked())
        #newButton.clicked.connect(lambda: makeart(content, parser))
        
        #newCheckbox.clicked.connect(lambda: parser.feed(urllib.request.urlopen(content).read().decode()))
        #newButton.clicked.connect(self.newButtonIsClicked(content))
        
        #global parser         
        #parser = MyHTMLParser()
        #if line.text():
            #makeart(line.text(), parser)
        #newCheckbox.clicked.connect(makeart(content, parser)) 
        
        def newButtonIsClicked():
            # text = 'Welcome fellow human beeing ^.^        
            # aktivate Checkbox if input is done
            newCheckbox.setCheckState(2)
            if line.text():   
                parser = MyHTMLParser()
                makeart(line.text(), parser)
                
            else: 
                newCheckbox.setCheckState(1)
                

    def canvasChanged(self, canvas):
        pass

from krita import *
from textblob import TextBlob
from textblob_de import TextBlobDE
import re
from html.parser import HTMLParser
import urllib.request
from nrclex import NRCLex
import numpy as np
import math
from PIL import Image


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
            
            
def add_svg(svg):
	
    clipboard = QGuiApplication.clipboard()
    mime_data = QMimeData()
    mime_data.setData('image/svg+xml', svg)
    clipboard.setMimeData(mime_data)
    Application.action('edit_paste').trigger()
    
def create_svg(svg, width, heigth):
    app = Krita.instance()
    # Document open?
    if app.activeDocument():
        doc = app.activeDocument() 
    else:
        doc = app.createDocument(width, heigth, 'SVGA Test', 'RGBA', 'U8', '', 120.0)
        
    app.activeWindow().addView(doc) 
    layer = doc.createVectorLayer('ColorSVG')
    layer.setName('ColorSVG')
    add_svg(svg)

def design_svg(width, height, x, y):
	svg = f'''<?xml version="1.0" encoding="iso-8859-1"?>
		<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
		<svg>'''
	return(svg)

def design_svg2(fillcolor, width, height, x, y):
    svg = f'''<rect x="{x}" y="{y}" width="{width}" height="{height}" fill = "{fillcolor}"/>'''
    return(svg)



## make art from emotions
def makeart(content, parser):

	parser = MyHTMLParser()            
	parser.feed(urllib.request.urlopen(content).read().decode())
	linkdata = parser.data

	# language
	language = ''

	# number of sentences
	sentencenr = 0

	# filtering parsed text
	text = ""	

	for phrases in linkdata:
		phrases = phrases.rstrip("\n\r+0-9[]()+")
		# skip unwanted characters         
		text = text + phrases


	# create textblob
	blob = TextBlob(text)
	
	# language?
	for w in blob.words:
		sentencenr = sentencenr + 1
		if re.match(r"and", w):
			language = 'en'
		elif re.match(r"und", w):
			language = 'de'

	if language == 'de':
		blob = TextBlobDE(text)
	else:
		blob = TextBlob(text)

	polarity = []
	
	for sentence in blob.sentences:    
		# polarity
		polarity.append(sentence.sentiment.polarity)
	
	text_object = NRCLex('nrc_en.json')
	size = round(math.sqrt(len(linkdata)))
	i = 0 # counter for all tuples
	j = 0 # counter for resize	

	lim = 0.2
	
	for sentence in blob.sentences:     
		# polarity
		polarity.append(sentence.sentiment.polarity)
	
    # define svg as string variable
	#svg = bytes()
	svg = design_svg(size, size, 0, 0)
	
	if linkdata is not None:
		# filtering parsed text
		text = ""
		for x in range(size):
			for y in range(size):
				phrase = linkdata[j].rstrip("\n\r+0-9[]()+")
				
				# skip unwanted characters     
				text = text + phrase
				
				# let's show the emotions
				emotion = NRCLex(phrase)

				red = 0
				green = 0
				blue = 0

				## calculate value for red:
				# positive-low arousal: trust, positive, surprise, joy		
				if emotion.raw_emotion_scores.get('trust'):
					red = red + (100*3.137*emotion.raw_emotion_scores['trust'])			
				if emotion.raw_emotion_scores.get('joy'):			
					red = red + (100*3.137*emotion.raw_emotion_scores['joy'])						
				if emotion.raw_emotion_scores.get('surprise'):						
					red = red + (100*3.137*emotion.raw_emotion_scores['surprise'])
												
				## calculate value for blue:
				# negative-high arousal: fear, anger, sadness
				if emotion.raw_emotion_scores.get('fear'):
					blue = blue + (100*1.961*emotion.raw_emotion_scores['fear'])			
				if emotion.raw_emotion_scores.get('anger'):
					blue = blue + (100*1.961*emotion.raw_emotion_scores['anger'])							
				if emotion.raw_emotion_scores.get('sadness'):
					blue = blue + (100*1.961*emotion.raw_emotion_scores['sadness'])					

				## calculate value for green: anticip, disgust, negative
				if emotion.raw_emotion_scores.get('anticip'):
					green = green + (100*1.176*emotion.raw_emotion_scores['anticip'])					
				if emotion.raw_emotion_scores.get('disgust'):
					green = green + (100*1.176*emotion.raw_emotion_scores['disgust'])								
				if emotion.raw_emotion_scores.get('negative'):
					green = green + (10*1.176*emotion.raw_emotion_scores['negative'])

				## now adding the polarity
				if polarity[j] < -1*float(lim):
					red = red + (100*3.137*polarity[j]) 
				elif polarity[j] > float(lim):
					blue = blue + (100*1.961*polarity[j])
				else:
					green = green + (100*1.176*polarity[j])

				## make sure every color is max 250
				if red > 255:
					red = 255
					
				if green > 255:
					green = 255				
					
				if blue > 255:
					blue = 255	
				
				## calculate Color
				rgbcolor = "rgb(" + str(round(red)) + ", " + str(round(green)) + ", " + str(round(blue)) + ")"
	
                # create svg
				svg_part = design_svg2(rgbcolor, 10, 10, x, y)
				svg = svg + svg_part

				# reset counter
				try:
					polarity[j + 1]
					j = j + 1
				except IndexError:
					j = 0 
																	

	svg_end = f'''</svg>'''
	svg = svg + svg_end
					 
	create_svg(svg.encode('utf-8'), size, size)
	#f = open("/tmp/test.svg", "w")
	#f.write(str(svg.encode('utf-8')))
	#f.write(svg)

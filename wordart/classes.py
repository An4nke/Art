from html.parser import HTMLParser
import urllib.request

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
    
    def __init__(self, language, sentences_lens, sentences, commas, polarity):    
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

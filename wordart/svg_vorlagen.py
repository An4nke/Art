from PIL import ImageColor
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import sys
import re
from krita import *
import sip

# svg
def design_svg(strokecolor, fillcolor, width, height):
    trans = str(((800 - height)/2) - 80)   
    #print (trans)
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
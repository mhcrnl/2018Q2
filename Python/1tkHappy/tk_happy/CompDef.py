#!/usr/bin/env python

class TextWidthComp(object):
    
    def __init__(self, name='Button1', compType='button', optionD=None, tkOptionD=None):
        
        self.name = name
        self.compType = compType
        self.helpD = compHelpDictionaries[compType]
        
        # separate options into legal Tk options and Other options
        self.optionD = {'name':name+' text'}  # place the name in the option Dictionary
            
        # ONLY legal Tk options go in tkOptionD
        self.tkOptionD = {'text':name} # make sure there is a "text" value in tkOptionD
            
        if compType in ['text', 'listbox','canvas']: # some widgets don't like text option
            del self.tkOptionD['text']
            
            # these widgets also can have scrollbars
            if not self.optionD.has_key('scrolly'):
                self.optionD['scrolly'] = 'yes'
            
        if compType == 'listbox': # default listbox to extended
            self.tkOptionD['selectmode'] = 'extended'
            
        if not self.tkOptionD.has_key('width') and compType!='message':
            if compType == 'text':
                self.tkOptionD['width'] = 40
                self.tkOptionD['height'] = 12
            else:
                self.tkOptionD['width'] = 15

        # put general options (e.g. name, x, y ) in optionD
        if type(optionD ) == type({}):
            for opt,val in optionD.items():
                self.optionD[opt] = val
                
        if compType=='radiobutton':
            if not self.optionD.has_key('radioGroup'):
                self.optionD['radioGroup'] = 1
                self.tkOptionD['value'] = str(name) + ' value'
            
        # put legal Tk options into tkOptionD
        if type(tkOptionD ) == type({}):
            for opt,val in tkOptionD.items():
                if self.helpD.has_key(opt) :
                    self.tkOptionD[opt] = val
                else:
                    self.optionD[opt] = val
                    
    def setPixelWidth(self, w):
        self.optionD['pixelWidth']=w
                    
    def setPixelHeight(self, h):
        self.optionD['pixelHeight']=h

class PixelWidthComp(TextWidthComp):
    
    def __init__(self, name='LabelFrame1', compType='labelframe', optionD=None, tkOptionD=None):
        
        setWidth = not tkOptionD.has_key('width')
        
        TextWidthComp.__init__(self, name, compType, optionD, tkOptionD)
        
        if setWidth:
            self.tkOptionD['width'] = 60
        if not self.tkOptionD.has_key('height'):
            self.tkOptionD['height'] = 50
                    
    def setPixelWidth(self, w):
        self.tkOptionD['width']=w
        print 'setting pixel width=',w
                    
    def setPixelHeight(self, h):
        self.tkOptionD['height']=h
        print 'setting pixel height=',h

#padx #horizontal padding between the text or image and the border
#pady #vertical padding between the text or image and the border
#height #height, text units or pixels
#width #width, text units or pixels
smallOptionD = {}
smallOptionStr = '''anchor  # N, NE, E, SE, S, SW, W, NW, or CENTER. Default is CENTER
background #The background color
font #font to use
foreground #color to use for text and bitmap content
image #image to display
justify #align multiple lines of text. LEFT, RIGHT, or CENTER
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
text #text to display. The text can contain newlines. '''

strL = smallOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        smallOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#height #height, text units or pixels
#width #width, text units or pixels

canvasOptionD = {}
canvasOptionStr = '''background #The background color
height #height, text units or pixels
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
width #width, text units or pixels'''

strL = canvasOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        canvasOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#padx #horizontal padding between the text or image and the border
#pady #vertical padding between the text or image and the border
#height #height, text units or pixels
#width #width, text units or pixels

textOptionD = {}
textOptionStr = '''background #The background color
font #font to use
foreground #color to use for text and bitmap content
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT'''

strL = textOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        textOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#padx #horizontal padding between the text or image and the border
#pady #vertical padding between the text or image and the border
#height #height, text units or pixels
#width #width, text units or pixels

radioOptionD = {}
radioOptionStr = '''background #The background color
font #font to use
foreground #color to use for text and bitmap content
image #image to display
justify #align multiple lines of text. LEFT, RIGHT, or CENTER
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
text #text to display. The text can contain newlines.
value #value of the radio button
indicatoron#true=standard radio button. false=SUNKEN. Default is true'''

strL = radioOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        radioOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#height #height, text units or pixels
#width #width, text units or pixels

listboxOptionD = {}
listboxOptionStr = '''background #The background color
font #font to use
foreground #color to use for text and bitmap content
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
selectmode # single, browse, multiple, extended
setgrid # 0 or 1'''

strL = listboxOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        listboxOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#labelanchor # N, NE, E, SE, S, SW, W, NW, or CENTER. Default is NW
#padx #horizontal padding between the text or image and the border
#pady #vertical padding between the text or image and the border
#height #height, text units or pixels
#width #width, text units or pixels

labelFrameOptionD = {}
labelFrameOptionStr = '''background #The background color
font #font to use
foreground #color to use for text and bitmap content
height #height, text units or pixels
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
text #text to display as label.  
width #width, text units or pixels'''

strL = labelFrameOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        labelFrameOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#width #width, text units or pixels

entryOptionD = {}
entryOptionStr = '''background #The background color
font #font to use
foreground #color to use for text and bitmap content
justify #align multiple lines of text. LEFT, RIGHT, or CENTER
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
text #text to display. The text can contain newlines.'''

strL = entryOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        entryOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#width #width, text units or pixels

messageOptionD = {}
messageOptionStr = '''aspect # Aspect ratio of text (default=150, w=50% larger than h)
background #The background color
font #font to use
foreground #color to use for text and bitmap content
justify #align multiple lines of text. LEFT, RIGHT, or CENTER
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
text #text to display. The text can contain newlines.'''

strL = messageOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        messageOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#anchor  # N, NE, E, SE, S, SW, W, NW, or CENTER. Default is CENTER
#command #function or method that is called when the button is pressed
#textvariable #Tkinter variable (usually a StringVar) if changed, the button text is updated
#padx #horizontal padding between the text or image and the border
#pady #vertical padding between the text or image and the border
#height #height, text units or pixels
#width #width, text units or pixels

buttonOptionD = {}
buttonOptionStr = '''background #The background color
borderwidth # is usually 1 or 2 pixels
compound #BOTTOM, LEFT, RIGHT, or TOP, image relative to text Default is NONE
font #font to use in the button
foreground #color to use for text and bitmap content
highlightbackground #color to use for the highlight border when the button does not have focus
highlightcolor #color to use for the highlight border when the button has focus
highlightthickness #width of the highlight border
image #image to display
justify #align multiple lines of text. LEFT, RIGHT, or CENTER
overrelief #relief to use when the mouse is moved over the widget
relief #Border decoration. SUNKEN RAISED GROOVE RIDGE FLAT
state # NORMAL, ACTIVE or DISABLED
takefocus #can use the Tab key to move to this button
text #text to display in the button. The text can contain newlines. 
wraplength #when text should be wrapped into multiple lines in screen units (0=no wrapping)'''

strL = buttonOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        buttonOptionD[sL[0].strip()] = sL[1].strip()
# --------------------------------------------------------------------------------------------------
#anchor# N, NE, E, SE, S, SW, W, NW, or CENTER
#textvariable# Associates a Tkinter variable (usually a StringVar)
#padx# Extra horizontal padding
#pady# Extra vertical padding
#height #height, text units or pixels
#width #width, text units or pixels

labelOptionD = {}
labelOptionStr = '''activebackground# background color when the label is active
activeforeground# foreground color when the label is active
background# The background color
borderwidth# width of the border
compound# image relative to text CENTER BOTTOM LEFT RIGHT TOP NONE
cursor# cursor to show when mouse moves over
disabledforeground# foreground color when disabled
font# font
foreground# color
highlightbackground# color when not focus
highlightcolor# color when focused
highlightthickness# width of the highlight border
image# image to display(PhotoImage, BitmapImage, or a compatible object)
justify# align multiple lines LEFT, RIGHT, or CENTER
relief# Border decoration FLAT SUNKEN, RAISED, GROOVE RIDGE
state# Label state. NORMAL ACTIVE DISABLED
takefocus# If true, accepts input focus
text# text to display (can contain newlines)
underline# character to be underlined (e.g. for keyboard shortcuts)
wraplength# when a label's text should be wrapped into multiple lines'''

strL = labelOptionStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        labelOptionD[sL[0].strip()] = sL[1].strip()

#compHelpDictionaries = {'button':buttonOptionD, 'label':labelOptionD}
compHelpDictionaries = {'button':smallOptionD, 'canvas':canvasOptionD,
    'label':smallOptionD, 'entry':entryOptionD,
    'labelframe':labelFrameOptionD, 'checkbutton':smallOptionD, 'message':messageOptionD,
    'radiobutton':radioOptionD, 'listbox':listboxOptionD, 'text':textOptionD}

if __name__ == "__main__":
    

    testBtn2 = TextWidthComp( name='Button2', compType='button',  
        optionD=None, tkOptionD=None)
        
    for opt,val in testBtn2.optionD.items():
        print opt,val
        
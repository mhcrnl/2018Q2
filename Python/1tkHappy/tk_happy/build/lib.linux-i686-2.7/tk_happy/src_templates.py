#!/usr/bin/env python
from string import maketrans, printable, digits, letters
import copy

# change all non-legal letters to underscore
goodset = letters+digits+'_'
nonlegal = ''.join([c for c in printable if c not in goodset])
legalTranTab = maketrans( nonlegal,"_"*len(nonlegal) )


def legalPythonIdentifier( name ):
    legalName = name.translate(legalTranTab) 
    if legalName[0] in digits:
        legalName = 'x'+legalName

    return legalName

def legalQuotedString( s ): # precede any quotes with backslash
    val = str(s)
    val = val.replace("'","\\'")
    val = val.replace('"','\\"')
    return val

def legalWidgetName(name, ctype):
    lcname = name.lower()
    lctype = ctype.lower()
    
    if lcname.find( lctype ) > -1:
        legalName = lcname.title()
    else:
        legalName = '%s_%s'%(lcname.title(), lctype.title())

    legalName = legalPythonIdentifier(legalName)

    return legalName
    
def makeOptionString( opDict, startComma=1 ):
    if opDict:
        sL = []
        for k,v in opDict.items():
            # precede any quotes in the value with a backslash
            val = legalQuotedString(v)
            sL.append( '%s="%s"'%(k,val) )
        s = ', '.join(sL)
        if len(s)>0 and startComma:
            s = ', ' + s
    else:
        s = ''
    
    return s


sInit = '''

class %s:
    def __init__(self, master):
        self.initComplete = 0
        frame = Frame(master, width=%i, height=%i%s)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        # bind master to <Configure> in order to handle any resizing, etc.
        # postpone self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        
'''
def beginSourceFile(className, width=300, height=300, opDict=None):
    return sInit%(className.title(), width, height, makeOptionString( opDict ))

#-------------------------------------------------------------
sHideOkBtn = '''
    def buttonbox(self):
        pass
        # this dummy routine overrides the standard "OK" and "Cancel" buttons
        # REMEMBER!!! to call self.ok() and self.cancel() in User Code
'''

sInitDialog = '''
from tkSimpleDialog import Dialog

class _Dialog(Dialog):
    # use dialogOptions dictionary to set any values in the dialog
    def __init__(self, parent, title = None, dialogOptions=None):
        self.initComplete = 0
        self.dialogOptions = dialogOptions
        Dialog.__init__(self, parent, title)

class %s(_Dialog):
%s
    def body(self, master):
        dialogframe = Frame(master, width=%i, height=%i%s)
        dialogframe.pack()
'''
def beginDialogSourceFile(className, hideOkBtn, width=300, height=300, opDict=None):
    if hideOkBtn:
        s = sHideOkBtn
    else:
        s = ''
    return sInitDialog%(className.title(),s, width, height, makeOptionString( opDict ))

#-------------------------------------------------------------
sDialogValidate = '''    def validate(self):
        self.result = {} # return a dictionary of results
    '''
def getDialogValidate():
    return sDialogValidate
#-------------------------------------------------------------
sEnd = '''
def main():
    root = Tk()
    app = %s(root)
    root.mainloop()

if __name__ == '__main__':
    main()
'''
def endSourceFile(className):
    return sEnd%(className.title(),)

#-------------------------------------------------------------
sEndDialog = '''

    def apply(self):
        print 'apply called'

class _Testdialog:
    def __init__(self, master):
        frame = Frame(master, width=300, height=300)
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        self.Button_1 = Button(text="Test Dialog", relief="raised", width="15")
        self.Button_1.place(x=84, y=36)
        self.Button_1.bind("<ButtonRelease-1>", self.Button_1_Click)

    def Button_1_Click(self, event): #click method for component ID=1
        dialog = %s(self.master, "Test Dialog")
        print '===============Result from Dialog===================='
        print dialog.result
        print '====================================================='

def main():
    root = Tk()
    app = _Testdialog(root)
    root.mainloop()

if __name__ == '__main__':
    main()
'''
def endDialogSourceFile(className):
    return sEndDialog%(className.title(),)


#----------------------------------------------------------------
# create list box... needs special treatment for y scroller
sCreateWidgetWScroll='''
        lbframe = Frame( %s )
        self.%s_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.%s = %s(lbframe, %s, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.%s.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.%s.pack(side=LEFT, fill=BOTH, expand=1)
'''
sCreateWidgetWOScroll='''
        self.%s = %s(%s, %s)
'''
def createWidgetwName(wName, wCall, guiType, opDict=None, specOpDict=None):
    opStr = makeOptionString( opDict, startComma=0 )
    
    if guiType=='dialog':
        master = 'dialogframe'
    else:
        master = 'self.master'

    doscroll = 0
    if type(specOpDict)==type({}):
        if specOpDict.has_key('scrolly'):
            if specOpDict['scrolly'].lower()=='yes':
                doscroll = 1
    if doscroll:
        return sCreateWidgetWScroll%(master,wName, wName, wCall.title(), opStr, wName, wName)
    else:
        return sCreateWidgetWOScroll%( wName, wCall.title(), master, opStr)
#----------------------------------------------------------------

# create widget
#        self.<name> = <widget>( <options> )
sCreateWidget = '        self.%s = %s(%s,%s)\n'
def createWidget(wName, wCall, guiType, opDict=None, specOpDict=None):
    
    if wCall.lower()=='entry':
        myOpDict = copy.deepcopy( opDict )
        if myOpDict.has_key('text'):
            del(myOpDict['text'])
    else:
        myOpDict = opDict
    
    if wCall.lower()=='labelframe':
        Constructor = 'LabelFrame'
    else:
        Constructor = wCall.title()

    doscroll = 0
    if type(specOpDict)==type({}):
        if specOpDict.has_key('scrolly'):
            if specOpDict['scrolly'].lower()=='yes':
                doscroll = 1
    if doscroll:
        return createWidgetwName(wName, wCall, guiType, myOpDict, specOpDict)
    else:
        if guiType=='dialog':
            return sCreateWidget%(wName, Constructor,'dialogframe', makeOptionString( myOpDict, startComma=0 ))
        else:
            return sCreateWidget%(wName, Constructor,'self.master', makeOptionString( myOpDict, startComma=0 ))
    
#----------------------------------------------------------------

# place widget
#        self.<name>.place( x=<x>, y=<y> )
sPlaceWidget = '        self.%s.place(x=%i, y=%i)\n'
sPlaceWidgetFrame = '        self.%s_frame.place(x=%i, y=%i)\n'
def placeWidget(wName, ctype, x, y, placeWidgetFrame):
    if placeWidgetFrame:
        return sPlaceWidgetFrame%(wName, int(x), int(y))
    else:
        return sPlaceWidget%(wName, int(x), int(y))
#----------------------------------------------------------------

# place widget Full (including width and height)

sPlaceWidgetFull = '        self.%s.place(x=%i, y=%i, width=%i, height=%i)\n'
sPlaceWidgetFrameFull = '        self.%s_frame.place(x=%i, y=%i, width=%i, height=%i)\n'
def placeWidgetFull(wName, ctype, x, y, w, h, placeWidgetFrame):
    if placeWidgetFrame:
        return sPlaceWidgetFrameFull%(wName, int(x), int(y), int(w), int(h))
    else:
        return sPlaceWidgetFull%(wName, int(x), int(y), int(w), int(h))
#----------------------------------------------------------------
# bind widget
#        self.<name>.bind("<event>", self.<callback>)
sBindWidget = '        self.%s.bind("<%s>", self.%s)\n'
def bindWidget(wName, eventName, callBack):
    return sBindWidget%( wName, eventName, callBack)
#----------------------------------------------------------------
# make string variable
#        self.<name>_StringVar = StringVar()
sMakeStringVar = '        self.%s_StringVar = StringVar()\n'
def makeStringVar( wName ):
    return sMakeStringVar%wName

#----------------------------------------------------------------
# connect string variable to widget
#        self.<name>.configure(variable=self.<name>_StringVar, <options>)
sConnectStringVar = '        self.%s.configure(variable=self.%s_StringVar%s)\n'
def connectStringVar(wName, opDict=None):
    return sConnectStringVar%(wName, wName, makeOptionString( opDict ))

# special for Entry widget
sConnectEntryStringVar = '        self.%s.configure(textvariable=self.%s_StringVar%s)\n'
def connectEntryStringVar(wName, opDict=None):
    return sConnectEntryStringVar%(wName, wName, makeOptionString( opDict ))
#----------------------------------------------------------------
# turn on trace for string variable
#        self.<name>_StringVar_traceName = self.<name>_StringVar.trace_variable("w", self.<name>_StringVar_Callback)
sTraceStringVar = '        self.%s_StringVar_traceName = self.%s_StringVar.trace_variable("w", self.%s_StringVar_Callback)\n'
def traceStringVar(wName):
    return sTraceStringVar%(wName, wName, wName)
#----------------------------------------------------------------
# statusbar
sStatusBar = '''        
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
'''
def getStatusBarSource():
    return sStatusBar
#----------------------------------------------------------------
# standard message dialogs
sMessageDialogs = '''
    # standard message dialogs... showinfo, showwarning, showerror
    def ShowInfo(self, title='Title', message='your message here.'):
        tkMessageBox.showinfo( title, message )
        return
    def ShowWarning(self, title='Title', message='your message here.'):
        tkMessageBox.showwarning( title, message )
        return
    def ShowError(self, title='Title', message='your message here.'):
        tkMessageBox.showerror( title, message )
        return
        
    # standard question dialogs... askquestion, askokcancel, askyesno, or askretrycancel
    # return True for OK, Yes, Retry, False for Cancel or No
    def AskYesNo(self, title='Title', message='your question here.'):
        return tkMessageBox.askyesno( title, message )
    def AskOK_Cancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askokcancel( title, message )
    def AskRetryCancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askretrycancel( title, message )
        
    # return "yes" for Yes, "no" for No
    def AskQuestion(self, title='Title', message='your question here.'):
        return tkMessageBox.askquestion( title, message )
    # END of standard message dialogs
'''
def getStandardMessageDialogs():
    return sMessageDialogs
#----------------------------------------------------------------
sFileDialogs = '''    # standard file dialogs... askdirectory, askopenfile, asksaveasfilename

    # return a string containing directory name
    def AskDirectory(self, title='Choose Directory', initialdir="."):
        dirname = tkFileDialog.askdirectory(parent=%s,initialdir=initialdir,title=title)
        return dirname # <-- string
        
    # return an OPEN file type object OR None (opened using mode, 'r','rb','w','wb')
    # WARNING... opening file with mode 'w' or 'wb' will erase contents
    def AskOpenFile(self, title='Choose File', mode='rb', initialdir='.', filetypes=None):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]
        fileobj = tkFileDialog.askopenfile(parent=%s,mode=mode,title=title,
            initialdir=initialdir, filetypes=filetypes)
        
        # if opened, then fileobj.name contains the name string
        return fileobj # <-- an opened file, or the value None
        
    # return a string containing file name (the calling routine will need to open the file)
    def AskSaveasFilename(self, title='Save File', filetypes=None, initialfile=''):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]

        fileName = tkFileDialog.asksaveasfilename(parent=%s,filetypes=filetypes, initialfile=initialfile ,title=title)
        return fileName # <-- string
        
    # END of standard file dialogs
'''
def getStandardFileDialogs(guiType='main'):
    if guiType=='dialog':
        master = 'self'
    else:
        master = 'self.master'
        
    return sFileDialogs%(master, master, master)
#----------------------------------------------------------------
sColorDialog='''
    # returns a color tuple and a string representation of the selected color
    def AskForColor(self,title='Pick Color'): 
        ctuple,cstr = tkColorChooser.askcolor(title=title)
        return ctuple,cstr
'''
def getStandardColorDialog():
    return sColorDialog
#----------------------------------------------------------------
#----------------------------------------------------------------
sAlarmDialog='''
    # alarm function is called after specified number of milliseconds
    def SetAlarm(self, milliseconds=1000):
        self.master.after( milliseconds, self.Alarm )
    def Alarm(self): 
        pass
'''
def getStandardAlarmDialog():
    return sAlarmDialog
#----------------------------------------------------------------
#----------------------------------------------------------------

if __name__ == '__main__':
    if 1:
        print beginSourceFile("TestForm1")
        print beginSourceFile("TestForm2",opDict={'background':'yellow'})
            
        print
        print endSourceFile("TestForm1")
        
        print
        print createWidget('Bang_Checkbutton', 'Checkbutton', {'bg':'red', 'ddd':'aaa'})
            
        print
        print placeWidget('Bang_Checkbutton','Checkbutton', '22', '55', 0)
        
        print
        print bindWidget('Bang_Button', 'ButtonRelease-1', 'Bang_Button_Click')
        
        print
        print makeStringVar( 'Bang_Checkbutton' )
        
        print
        print connectStringVar('Bang_Checkbutton', opDict={'onvalue':"yes", 'offvalue':"no"})
            
        print
        print traceStringVar('Bang_Checkbutton')
        print
        print createWidget('myList', 'Listbox', {'bg':'red', 'ddd':'aaa'})
            
        print
        print placeWidget('myList','Listbox', '22', '55', 1)
        

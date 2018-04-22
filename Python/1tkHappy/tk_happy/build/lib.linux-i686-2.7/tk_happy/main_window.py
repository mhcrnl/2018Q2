#!/usr/bin/env python
from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkColorChooser
import FormWindow
import EditWindow
import FormDef
import os.path
import webbrowser
import sys
from make_py_src import FormSource
import make_menu_src
from MenuMaker_Dialog import Menumaker
from NoSaveWarn_Dialog import Nosavewarn
# see book examples in C:\Python23\Doc\TK_Examples


class TK_Happy( object ):
    def __init__(self, MainWin):
        
        self.MainWin = MainWin
        self.myForm = None

        MainWin.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        MainWin.allow_subWindows_to_close = 0
        
        self.root = MainWin
        # make menus
        self.menuBar = Menu(MainWin, relief = 'raised', bd=2)

        # create file pulldown menu
        fileMenu = Menu(self.menuBar, tearoff=0)
        fileMenu.add('command', label = 'New', command = self.newForm)
        fileMenu.add('command', label = 'Open', command = self.openFile)
        fileMenu.add('command', label = 'Save', command = self.saveasFile)
        fileMenu.add('command', label = 'SaveAs', command = self.saveasFile)
        fileMenu.add('command', label = 'Refresh', command = self.refresh)
        fileMenu.add('command', label = 'Exit', command = self.cleanupOnQuit)
        self.menuBar.add('cascade', label="File", menu=fileMenu)

        # create options pulldown menu
        optMenu = Menu(self.menuBar, tearoff=0)
        optMenu.add('command', label = 'Font', command =self.TBD)
        optMenu.add('command', label = 'Color', command = self.ColorPickButton_Select)
        self.menuBar.add('cascade', label="Options", menu=optMenu)

        # create help pulldown menu
        optMenu = Menu(self.menuBar, tearoff=0)
        optMenu.add('command', label = 'tk_happy - Overview', command =self.browser_tk_happy)
        optMenu.add('command', label = 'effbot.org - INTRODUCTION', command =self.browserEffbot)
        optMenu.add('command', label = 'pythonware.com - LIBRARY', command =self.browserPythonware)
        optMenu.add('command', label = 'infohost.nmt.edu - TK REFERENCE', command = self.browserInfohost)
        optMenu.add('command', label = 'astro.washington.edu - SUMMARY', command = self.browserTkinterSummary)
        optMenu.add('command', label = 'ferg.org - THINKING IN TK', command = self.browserThinkingInTK)
        self.menuBar.add('cascade', label="Help", menu=optMenu)

        # create About menu
        self.menuBar.add('command', label="About", command = self.About)

        self.root.config(menu=self.menuBar)

        superFrame = Frame( MainWin ) # frame for controls
        topFrame = Frame( superFrame ) # frame for controls

        # make StringVar to hold type of widget to place on form when clicked
        # frame1 is the frame for column #1 of controls
        
        #frame1 = Frame( topFrame ) # frame for radio buttons
        frame1 = LabelFrame(topFrame, text="Widgets")
        MainWin.placementWidgetType=StringVar()
        MainWin.placementWidgetType.set('none')
        CONTROLS = [
            ("None", "none"),
            ("Button", "button"),
            ("Canvas", "canvas"),
            ("Checkbutton", "checkbutton"),
            ("Entry", "entry"),
            ("Label", "label"),
            ("LabelFrame", "labelframe"),
            ("Listbox", "listbox"),
            ("Message", "message"),
            ("Radiobutton", "radiobutton"),
            ("Text", "text"),
            ]


        self.Listbox_1 = Listbox(frame1,width="15",height=str(len(CONTROLS)))#, selectmode="extended")
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)


        for text, cont in CONTROLS:
            #b = Radiobutton(frame1, text=text, value=cont, variable=MainWin.placementWidgetType)
            #b.pack(anchor=W)
            self.Listbox_1.insert(END, text)
        
        self.Listbox_1.pack(anchor=W)
        self.Listbox_1.select_set(0) # make None highlighted
        
        # show checkbox for multiple vs. single component placements
        MainWin.multiPlacements = Checkbutton(frame1, text="multi-placement", width="15")
        MainWin.multiPlacements.pack(anchor=W)
        MainWin.multiPlacements_StringVar = StringVar()
        MainWin.multiPlacements_StringVar.set("no")
        MainWin.multiPlacements.configure(variable=MainWin.multiPlacements_StringVar, onvalue="yes", offvalue="no")
        
        frame1.pack(anchor=NW, side=LEFT)

        # make frame for column 2 of controls
        frame2 = Frame( topFrame ) # frame for radio buttons
        
        # show option for Main Window or Dialog
        MainWin.mainOrDialog=StringVar()
        MainWin.mainOrDialog.set('main')
        lbframe = LabelFrame(frame2, text="GUI Type")
        lbframe.pack(anchor=W)

        b = Radiobutton(lbframe, text="Main Window", value='main', variable=MainWin.mainOrDialog)
        b.pack(anchor=W)
        b = Radiobutton(lbframe, text="Dialog", value='dialog', variable=MainWin.mainOrDialog)
        b.pack(anchor=W)
        
        MainWin.hideOkChkBox = Checkbutton(lbframe, text="Hide OK Btn", width="15", anchor=E)
        MainWin.hideOkChkBox.pack(anchor=E, side=TOP)
        MainWin.hideOkChkBox_StringVar = StringVar()
        MainWin.hideOkChkBox_StringVar.set("no")
        MainWin.hideOkChkBox.configure(variable=MainWin.hideOkChkBox_StringVar, onvalue="yes", offvalue="no")
        self.hideOkChkBox_traceName = MainWin.hideOkChkBox_StringVar.trace_variable("w", self.hideOkChkBox_Callback)
        
        # show checkbox for menu and status bar
        lbframe = LabelFrame(frame2, text="Window Options")
        lbframe.pack(anchor=W)
        
        MainWin.menuChkBox = Checkbutton(lbframe, text="Main Menu", width="15", anchor=W)
        MainWin.menuChkBox.pack(anchor=W, side=TOP)
        MainWin.menuChkBox_StringVar = StringVar()
        MainWin.menuChkBox_StringVar.set("no")
        MainWin.menuChkBox.configure(variable=MainWin.menuChkBox_StringVar, onvalue="yes", offvalue="no")
        self.menuChkBox_traceName = MainWin.menuChkBox_StringVar.trace_variable("w", self.menuChkBox_Callback)
        
        MainWin.statusBarChkBox = Checkbutton(lbframe, text="Status Bar", width="15", anchor=W)
        MainWin.statusBarChkBox.pack(anchor=W, side=TOP)
        MainWin.statusBarChkBox_StringVar = StringVar()
        MainWin.statusBarChkBox_StringVar.set("no")
        MainWin.statusBarChkBox.configure(variable=MainWin.statusBarChkBox_StringVar, onvalue="yes", offvalue="no")
        self.statusBarChkBox_traceName = MainWin.statusBarChkBox_StringVar.trace_variable("w", self.statusBarChkBox_Callback)
        
        MainWin.resizableChkBox = Checkbutton(lbframe, text="Resizable", width="15", anchor=W)
        MainWin.resizableChkBox.pack(anchor=W, side=TOP)
        MainWin.resizableChkBox_StringVar = StringVar()
        MainWin.resizableChkBox_StringVar.set("no")
        MainWin.resizableChkBox.configure(variable=MainWin.resizableChkBox_StringVar, onvalue="yes", offvalue="no")
        self.resizableChkBox_traceName = MainWin.resizableChkBox_StringVar.trace_variable("w", self.resizableChkBox_Callback)
        
        # set snap value
        snapFrame = Frame( lbframe )
        label = Label(snapFrame, text="Snap Size")
        MainWin.snapValue=IntVar()
        MainWin.snapSpinbox = Spinbox(snapFrame, values=(1,6,12,18,24,30,36,42,48), \
            textvariable=MainWin.snapValue, width=2)
        MainWin.snapValue.set(12)
        
        self.snapValue_traceName = MainWin.snapValue.trace_variable("w", self.snapValue_Callback)
        
        label.pack(side=LEFT, anchor=W)
        MainWin.snapSpinbox.pack( side=LEFT, anchor=W)
        snapFrame.pack(anchor=W, side=TOP)
        
        # show choices for standard dialogs
        lbframe = LabelFrame(frame2, text="Standard Dialogs")
        lbframe.pack(anchor=W)

        MainWin.stdDialMessChkBox = Checkbutton(lbframe, text="Messages", width="15", anchor=W)
        MainWin.stdDialMessChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialMessChkBox_StringVar = StringVar()
        MainWin.stdDialMessChkBox_StringVar.set("no")
        MainWin.stdDialMessChkBox.configure(variable=MainWin.stdDialMessChkBox_StringVar, onvalue="yes", offvalue="no")
        

        MainWin.stdDialColorChkBox = Checkbutton(lbframe, text="Color Choose", width="15", anchor=W)
        MainWin.stdDialColorChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialColorChkBox_StringVar = StringVar()
        MainWin.stdDialColorChkBox_StringVar.set("no")
        MainWin.stdDialColorChkBox.configure(variable=MainWin.stdDialColorChkBox_StringVar, onvalue="yes", offvalue="no")

        MainWin.stdDialFileChkBox = Checkbutton(lbframe, text="File Open/Save", width="15", anchor=W)
        MainWin.stdDialFileChkBox.pack(anchor=E, side=TOP)
        MainWin.stdDialFileChkBox_StringVar = StringVar()
        MainWin.stdDialFileChkBox_StringVar.set("no")
        MainWin.stdDialFileChkBox.configure(variable=MainWin.stdDialFileChkBox_StringVar, onvalue="yes", offvalue="no")

        MainWin.stdAlarmChkBox = Checkbutton(lbframe, text="Alarm Handler", width="15", anchor=W)
        MainWin.stdAlarmChkBox.pack(anchor=E, side=TOP)
        MainWin.stdAlarmChkBox_StringVar = StringVar()
        MainWin.stdAlarmChkBox_StringVar.set("no")
        MainWin.stdAlarmChkBox.configure(variable=MainWin.stdAlarmChkBox_StringVar, onvalue="yes", offvalue="no")
        
        # put color picker button
        self.ColorPickButton = Button(frame1, text="Put Color on Clipboard")
        self.ColorPickButton.pack(anchor=W, side=TOP)
        self.ColorPickButton.bind("<ButtonRelease-1>", self.ColorPickButton_Click)
        
        # pack column 2 of controls
        frame2.pack(anchor=W, side=TOP)


        topFrame.pack(fill=BOTH, expand=Y)
        
        # make a Status Bar
        statframe = Frame(MainWin)
        MainWin.statusMessage = StringVar()
        MainWin.statusMessage.set('Welcome to tk_happy')
        self.statusbar = Label(statframe, textvariable=MainWin.statusMessage, 
            bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        statframe.pack(anchor=SW, fill=X, side=BOTTOM)
        
        superFrame.pack(fill=BOTH, expand=Y)
        
        
        if len( sys.argv ) == 2:
            fName = sys.argv[1]
            if fName.find('.')<0:
                fName += '.def'
            self.pathopen = os.path.abspath(fName)
            if os.path.isfile( self.pathopen ): # if file exists, read it as a definition file
                self.readFormDefinitionFile()
            else:
                MainWin.statusMessage.set('file "%s" does not exist'%fName)
        #else:
        #    self.newForm()
        
        #MainWin.geometry('320x400+10+10')
        #print 'MainWin.geometry()=',MainWin.geometry()
        #print 'self.ColorPickButton.bbox()=',self.ColorPickButton.bbox()
    
    def clearPlacementWidgetType(self):
        self.MainWin.placementWidgetType.set('none')
        
        for i in self.Listbox_1.curselection():
            self.Listbox_1.selection_clear(i)
        self.Listbox_1.select_set(0)
        
    def Listbox_1_Click(self, event): #click method for component ID=1
        labelL = []
        val = 'none'
        for i in self.Listbox_1.curselection():
            labelL.append( self.Listbox_1.get(i))
            val = self.Listbox_1.get(i).lower()
        
        self.MainWin.placementWidgetType.set(val)
                
    def ColorPickButton_Click(self, event): #put selected color on clipboard
        self.ColorPickButton_Select()
        
    def ColorPickButton_Select(self): #put selected color on clipboard
        self.MainWin.statusMessage.set('Place Selected Color on Clipboard')
        ctup,cstr = tkColorChooser.askcolor(title='Place Selected Color on Clipboard')
        if cstr != None:
            self.MainWin.statusMessage.set('%s is on Clipboard'%cstr)
            self.ColorPickButton.clipboard_clear()
            self.ColorPickButton.clipboard_append(cstr)
            
            print 'color chosen=',cstr
        

    def resizableChkBox_Callback(self, varName, index, mode):
        print 'Status Bar =',self.MainWin.resizableChkBox_StringVar.get()
        
        try:
            self.myForm.setSpecialOption('resizable', self.MainWin.resizableChkBox_StringVar.get())
        except:
            pass
                    
        self.refresh() # redraw the form window showing menu state.
        
    def statusBarChkBox_Callback(self, varName, index, mode):
        print 'Status Bar =',self.MainWin.statusBarChkBox_StringVar.get()
        
        try:
            self.myForm.setSpecialOption('hasstatusbar', self.MainWin.statusBarChkBox_StringVar.get())
        except:
            pass
                    
        self.refresh() # redraw the form window showing menu state.

    def menuChkBox_Callback(self, varName, index, mode):
        print 'make menu =',self.MainWin.menuChkBox_StringVar.get()
        
        try:
            self.myForm.setSpecialOption('hasmenu', self.MainWin.menuChkBox_StringVar.get())
        except:
            pass
        
        if self.MainWin.menuChkBox_StringVar.get()=='yes' and self.myForm:
            dialog = Menumaker(self.MainWin, "Define Menu Structure",
                self.myForm.getSpecialOption('menu'))
            print dialog.result
            
            if type(dialog.result) == type({}):
                
                menuStr = dialog.result.get('menu','').strip()
                if len( menuStr ) > 0:
                    self.myForm.setSpecialOption('menu',menuStr)
                    print 'Recording new Menu Definition'
                    
        self.refresh() # redraw the form window showing menu state.


    def hideOkChkBox_Callback(self, varName, index, mode):
        print 'Hide OK Button in Dialog =',self.MainWin.hideOkChkBox_StringVar.get()

    def snapValue_Callback(self, varName, index, mode):
        #print 'snap variable name=',self.MainWin.snapValue
        #print "snapValue_Callback varName, index, mode",varName, index, mode
        #print "    new IntVar value =",self.MainWin.snapValue.get()
        
        try:
            self.FormWin.showSnapGrid()
        except:
            pass
        
    def cleanupOnQuit(self):
        print 'Doing final cleanup before quitting'
        self.MainWin.allow_subWindows_to_close = 1
        self.MainWin.destroy()

    def saveasFile(self):
        if self.myForm:
            name = self.myForm.optionD['name'] + '.def'
        else:
            name = '*.def'
        self.saveFile(name)
    
    def refresh(self):
        try:
            if self.FormWin and self.myForm:
                self.FormWin.changeFormDef( self.myForm )
        except:
            pass
        
    def saveFile(self, fileDesc='*.def'):
        print 'Save File'
        self.fsave = tkFileDialog.asksaveasfilename(parent=self.root, title='Saving tk_happy file', 
            initialfile=fileDesc)
        
        if self.fsave:
            spL = self.fsave.split('.')
            #print spL
            if len(spL) == 1:
                self.fsave = self.fsave + '.def'
            elif len(spL) == 2:
                if spL[-1].lower() != 'def':
                    self.fsave = spL[0] + '.def'
                    print 'WARNING... added "def" to file name'
            elif len(spL) > 2: # take extra dots out of name
                if spL[-1].lower() != 'def':
                    self.fsave = '_'.join(spL) + '.def'
                else:
                    self.fsave = '_'.join(spL[:-1]) + '.def'
            else:
                self.fsave = '' # abort
                
            
            print 'saving to file',self.fsave
            
            if self.myForm:
                
                # set any form options prior to save
                self.myForm.setSpecialOption('guitype', self.MainWin.mainOrDialog.get())
                self.myForm.setSpecialOption('hideOkBtn', self.MainWin.hideOkChkBox_StringVar.get())
                self.myForm.setSpecialOption('hasmenu', self.MainWin.menuChkBox_StringVar.get())
                self.myForm.setSpecialOption('hasstatusbar', self.MainWin.statusBarChkBox_StringVar.get())
                self.myForm.setSpecialOption('resizable', self.MainWin.resizableChkBox_StringVar.get())
                
                
                self.myForm.setSpecialOption('hasstddialmess', self.MainWin.stdDialMessChkBox_StringVar.get())
                self.myForm.setSpecialOption('hasstddialfile', self.MainWin.stdDialFileChkBox_StringVar.get())
                self.myForm.setSpecialOption('hasstddialcolor', self.MainWin.stdDialColorChkBox_StringVar.get())
                self.myForm.setSpecialOption('hasstdalarm', self.MainWin.stdAlarmChkBox_StringVar.get())
                
                
                if self.myForm.savePickleFile(self.fsave):
                    self.MainWin.title(self.myForm.optionD['name'])
                    self.MainWin.statusMessage.set('saved file:'+self.fsave)
                    
                    # save to py file
                    sf = FormSource(self.myForm, self.MainWin)
                    sf.saveToFile()

                else:
                    self.MainWin.statusMessage.set('ERROR... did NOT save file:'+self.fsave)
                    dialog = Nosavewarn(self.MainWin, "File Save Error")
                    #self.MainWin.title(self.myForm.optionD['name'])

        else:
            self.MainWin.statusMessage.set('WARNING... did NOT save file:'+self.fsave)
            tkMessageBox.showwarning( 'File NOT Saved', 'No file was saved' )
                
    
    def TBD(self):
        print 'Not yet implemented'
        tkMessageBox.showwarning( 'Feature NOT Implemented', 'This Feature is NOT yet Implemented' )

    def About(self):
        tkMessageBox.showinfo(
            "About tk_happy",
            "tk_happy is:\n\n"+\
            "A quick approach to\n"+\
            "building Tkinter applications.\n"+\
            "Written by Charlie Taylor\n"
        )

    def browser_tk_happy(self):
        try:
            webbrowser.open_new('http://tk-happy.sourceforge.net/overview.html')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
    def browserEffbot(self):
        try:
            webbrowser.open_new('http://effbot.org/tkinterbook/')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
    def browserPythonware(self):
        try:
            webbrowser.open_new('http://www.pythonware.com/library/tkinter/introduction/index.htm')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
    def browserInfohost(self):
        try:
            webbrowser.open_new('http://infohost.nmt.edu/tcc/help/pubs/tkinter/')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
    def browserTkinterSummary(self):
        try:
            webbrowser.open_new('http://www.astro.washington.edu/owen/TkinterSummary.html')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
    def browserThinkingInTK(self):
        try:
            webbrowser.open_new('http://www.ferg.org/thinking_in_tkinter/index.html')
            self.MainWin.statusMessage.set('Launching Browser...')
        except:
            print 'ERROR launching browser'
            self.MainWin.statusMessage.set('ERROR.. Launching Browser')
            

        
    def showAllForms(self):
        # only called from readFormDefinitionFile (fprefix and dirname initialized there)
        try:
            x = self.EditWin.winfo_x()
            self.EditWin.clearAll()
        except:
            self.EditWin = EditWindow.EditWindow(self.MainWin)
            self.EditWin.transient(self.MainWin)
            print 'created EditWin'
    
        self.myForm = FormDef.FormDef(self.fprefix,self.dirname)
        if self.myForm.readFileOK:
            self.MainWin.statusMessage.set('read file:'+self.fopen)
            self.MainWin.title( self.fprefix )
            
            # set guitype string variable from FormDef object
            if self.myForm.getSpecialOption('guitype')=='dialog':
                self.MainWin.mainOrDialog.set('dialog')
            else:
                self.MainWin.mainOrDialog.set('main')
            
            # set hideOkBtn string variable from FormDef object
            if self.myForm.getSpecialOption('hideOkBtn')=='yes':
                self.MainWin.hideOkChkBox_StringVar.set("yes")
            else:
                self.MainWin.hideOkChkBox_StringVar.set("no")
            
            # set hasmenu string variable from FormDef object
            if self.myForm.getSpecialOption('hasmenu')=='yes':
                # inhibit dialog pop-up when reading file
                self.MainWin.menuChkBox_StringVar.trace_vdelete("w", self.menuChkBox_traceName)
                self.MainWin.menuChkBox_StringVar.set("yes")
                self.menuChkBox_traceName = self.MainWin.menuChkBox_StringVar.trace_variable("w", self.menuChkBox_Callback)

            else:
                self.MainWin.menuChkBox_StringVar.set("no")
            
            
            # set resizable string variable from FormDef object
            if self.myForm.getSpecialOption('resizable')=='yes':
                # inhibit dialog pop-up when reading file
                self.MainWin.resizableChkBox_StringVar.trace_vdelete("w", self.resizableChkBox_traceName)
                self.MainWin.resizableChkBox_StringVar.set("yes")
                self.resizableChkBox_traceName = self.MainWin.resizableChkBox_StringVar.trace_variable("w", self.resizableChkBox_Callback)
            else:
                self.MainWin.resizableChkBox_StringVar.set("no")
            
            # set hasstatusbar string variable from FormDef object
            if self.myForm.getSpecialOption('hasstatusbar')=='yes':
                # inhibit dialog pop-up when reading file
                self.MainWin.statusBarChkBox_StringVar.trace_vdelete("w", self.statusBarChkBox_traceName)
                self.MainWin.statusBarChkBox_StringVar.set("yes")
                self.statusBarChkBox_traceName = self.MainWin.statusBarChkBox_StringVar.trace_variable("w", self.statusBarChkBox_Callback)
            else:
                self.MainWin.statusBarChkBox_StringVar.set("no")
                
            # set standard dialog string variables from FormDef object
            if self.myForm.getSpecialOption('hasstddialmess')=='yes':
                self.MainWin.stdDialMessChkBox_StringVar.set("yes")
            else:
                self.MainWin.stdDialMessChkBox_StringVar.set("no")
                
            if self.myForm.getSpecialOption('hasstddialfile')=='yes':
                self.MainWin.stdDialFileChkBox_StringVar.set("yes")
            else:
                self.MainWin.stdDialFileChkBox_StringVar.set("no")
                
                
            if self.myForm.getSpecialOption('hasstddialcolor')=='yes':
                self.MainWin.stdDialColorChkBox_StringVar.set("yes")
            else:
                self.MainWin.stdDialColorChkBox_StringVar.set("no")
                
            if self.myForm.getSpecialOption('hasstdalarm')=='yes':
                self.MainWin.stdAlarmChkBox_StringVar.set("yes")
            else:
                self.MainWin.stdAlarmChkBox_StringVar.set("no")
                
        else:
            self.MainWin.statusMessage.set('ERROR... reading file:'+self.fopen)
            self.MainWin.title( 'tk_happy' )
            
        try:
            x = self.FormWin.winfo_x()
            self.refresh()
        except:
            
            self.FormWin = FormWindow.FormWindow(self, self.MainWin, self.EditWin, self.myForm) 
            self.FormWin.transient(self.MainWin)
            print 'created FormWin'
            
        
    def newForm(self):
        print "New Form"
        
        try:
            self.EditWin.destroy()
        except:
            pass
        try:
            self.FormWin.destroy()
        except:
            pass
        self.EditWin = None
        self.FormWin = None
        
        self.pathopen = 'NewForm.def'
        self.fopen = 'NewForm.def'
        self.fprefix = 'NewForm'
        self.dirname = os.path.dirname( self.pathopen )
        self.showAllForms()
        
    def openFile(self):
        print 'Open File'
        filetypes = [
            ('tk_happy definition','*.def'),
            ('Any File','*.*')]
        self.pathopen = tkFileDialog.askopenfilename(parent=self.root,title='Open tk_happy file', 
            filetypes=filetypes)
        
        if self.pathopen:
            self.readFormDefinitionFile()
            
    def readFormDefinitionFile(self):
        self.fopen = os.path.basename( self.pathopen )
        self.fprefix = self.fopen.split('.')[0]
        print 'getting file:',self.fopen
            
        self.dirname = os.path.dirname( self.pathopen )
        print 'directory:',self.dirname
            
        self.showAllForms()
        
if __name__=="__main__":
    root = Tk()
    MainWin = root
    MainWin.title('Main Window')
    #MainWin.geometry('320x320+10+10')
    MainWin.config(background='#FFFACD')#'lemonchiffon': '#FFFACD'

    tk_happy = TK_Happy( MainWin )
    # must start mainloop for the following auto load to work properly
    MainWin.mainloop()

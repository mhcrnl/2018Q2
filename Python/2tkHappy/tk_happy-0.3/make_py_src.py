#!/usr/bin/env python
from src_templates import *
import SourceCode
import make_menu_src
#from src_templates import legalPythonIdentifier

class FormSource( object ):
    
    def __init__(self, formObj, MainWin):
        self.formObj = formObj
        self.MainWin = MainWin
        if self.MainWin.mainOrDialog.get() == "dialog":
            self.pyFile = formObj.fName[:-4] + '_Dialog.py'
            self.imADialog = 1
        else:
            self.pyFile = formObj.fName[:-3] + 'py'
            self.imADialog = 0
        self.sourceFile = SourceCode.SourceFile( self.pyFile )
        self.getClassAndInit()
    
    def saveToFile(self):
        self.sourceFile.saveToFile()
    
    def getClassAndInit(self):
    
        # make class statement and top of __init__
        w = self.formObj.optionD['width']
        h = self.formObj.optionD['height']
        name = '_'+self.formObj.optionD['name'] # add underscore to beginning (preclude name collision)
        
        self.importSectionL = ['from Tkinter import *\n']
        
        self.classInitUserSectionL = []

        if self.imADialog:
            if self.MainWin.hideOkChkBox_StringVar.get()=="yes":
                self.classInitL = [beginDialogSourceFile(name, 1, w, h, self.formObj.tkOptionD)]
            else:
                self.classInitL = [beginDialogSourceFile(name, 0, w, h, self.formObj.tkOptionD)]
        else:
            self.classInitL = [beginSourceFile(name, w, h, self.formObj.tkOptionD)]
            
            self.classInitL.append('        self.master.title("%s")\n'%(self.formObj.optionD['name'],))
        
        # check for standard dialog includes
        if self.MainWin.stdDialMessChkBox_StringVar.get()=='yes':
            self.importSectionL.append('import tkMessageBox\n')
        if self.MainWin.stdDialFileChkBox_StringVar.get()=='yes':
            self.importSectionL.append('import tkFileDialog\n')
        if self.MainWin.stdDialFileChkBox_StringVar.get()=='yes':
            self.importSectionL.append('import tkColorChooser\n')
            
        # make end code while name is right
        if self.MainWin.mainOrDialog.get() == "dialog":
            self.endCode = endDialogSourceFile(name)
        else:
            self.endCode = endSourceFile(name)
        
        # sort widgets into alphabetical order
        sortL = []
        for comp in self.formObj.compObjL:
            sortL.append( [comp.compType, comp.name, comp] )
        sortL.sort()
        
        # flag to make traceback for variables (StringVar, etc.)
        needVarTraceback = 0
        traceNameL = [] # will be names of form "PY_VAR1"
        
        # dictionary of radio groups
        radioGroupD = {}
    
        # loop through the components to make their widget creation statements
        temp = '''\n        self.%s = %s(%s)\n'''
        bindMethodL = []
        for ctype, name, comp in sortL:
            x = comp.optionD['x']
            y = comp.optionD['y']
            
            wName = legalWidgetName(name, ctype)
            
            self.classInitL.append('\n')
            self.classInitL.append( createWidget(wName, ctype, self.MainWin.mainOrDialog.get(), 
                comp.tkOptionD, comp.optionD) )
            
            placeWidgetFrame = comp.optionD.get('scrolly','').lower()=='yes'
            try:
                w = comp.optionD['pixelWidth']
                h = comp.optionD['pixelHeight']
                self.classInitL.append(placeWidgetFull(wName, ctype, x, y, w, h, placeWidgetFrame))
            except:
                self.classInitL.append(placeWidget(wName, ctype, x, y, placeWidgetFrame))
            
            # make any checkbutton StringVar variables
            if ctype in ['checkbutton']:
                svname = '%s_StringVar'%wName
                self.classInitL.append( makeStringVar( wName ) )
                opDict = {'onvalue':"yes", 'offvalue':"no"}
                self.classInitL.append(connectStringVar(wName, opDict))
                traceNameL.append('%s_StringVar_Callback'%wName)
                self.classInitL.append( traceStringVar(wName) )
                needVarTraceback = 1
            
            # make any entry StringVar variables
            if ctype in ['entry']:
                svname = '%s_StringVar'%wName
                self.classInitL.append( makeStringVar( wName ) )
                opDict = {}
                self.classInitL.append(connectEntryStringVar(wName, opDict))
                self.classInitL.append( '        self.%s.set("%s")\n'%(svname,legalQuotedString(comp.tkOptionD['text'])))
                traceNameL.append('%s_StringVar_Callback'%wName)
                self.classInitL.append( traceStringVar(wName) )
                needVarTraceback = 1
            
            
            # make any radiobutton StringVar variables
            if ctype in ['radiobutton']:
                radioGroup = int(comp.optionD['radioGroup'])
                svname = 'RadioGroup%i_StringVar'%radioGroup
                gName = 'RadioGroup%i'%radioGroup
                
                # only create one callback routine for all of the radio buttons in the group
                if not radioGroupD.has_key( radioGroup ):
                    radioGroupD[ radioGroup ] = [comp] # start list of radio components in each radio group
                
                    self.classInitL.append( makeStringVar( gName ) )
                    self.classInitL.append( '        self.%s.set("%s")\n'%(svname,legalQuotedString(comp.tkOptionD['value'])))
                    traceNameL.append('%s_StringVar_Callback'%gName)
                    needVarTraceback = 1
                    self.classInitL.append( traceStringVar(gName) )

                self.classInitL.append( '        self.%s.configure(variable=self.%s )\n'%(wName, svname))
            
            
            #create any bind statements for components
            if ctype=='button':
                methodName = '%s_Click'%(wName,)
                id = comp.optionD['compID']
                self.classInitL.append(bindWidget(wName, 'ButtonRelease-1', methodName))
                bindMethodL.append( (methodName,id,'click','') )
                
            if ctype=='listbox':
                methodName = '%s_Click'%(wName,)
                id = comp.optionD['compID']
                self.classInitL.append(bindWidget(wName, 'ButtonRelease-1', methodName))
                userLines =     ['        print "current selection(s) =",self.%s.curselection()\n'%wName]
                userLines.append('        labelL = []\n' )
                userLines.append('        for i in self.%s.curselection():\n'%wName )
                userLines.append('            labelL.append( self.%s.get(i))\n'%wName )
                userLines.append('        print "current label(s) =",labelL\n')
                userLines.append('        # use self.%s.insert(0, "item zero")\n'%wName)
                userLines.append('        #     self.%s.insert(index, "item i")\n'%wName)
                userLines.append('        #            OR\n')
                userLines.append('        #     self.%s.insert(END, "item end")\n'%wName)
                userLines.append('        #   to insert items into the list box\n')

                bindMethodL.append( (methodName,id,'click',userLines) )

                
            if ctype=='canvas':
                methodName = '%s_Click'%(wName,)
                id = comp.optionD['compID']
                self.classInitL.append(bindWidget(wName, 'ButtonRelease-1', methodName))
                userLines =     ['        print "clicked in canvas at x,y =",event.x,event.y\n']
                userLines.append('        w = int(self.%s.cget("width"))\n'%(wName,))
                userLines.append('        h = int(self.%s.cget("height"))\n'%(wName,))
                userLines.append('        self.%s.create_rectangle((2, 2, w+1, h+1), outline="blue")\n'%(wName,))
                userLines.append('        self.%s.create_line(0, 0, w+2, h+2, fill="red")\n'%(wName,))
                userLines.append('        x = int(event.x)\n')
                userLines.append('        y = int(event.y)\n')
                userLines.append('        print "event x,y=",x,y\n')
                userLines.append('        self.%s.create_text(x,y, text="NE", fill="green", anchor=NE)\n'%(wName,))
                userLines.append('        self.%s.create_text(x,y, text="SW", fill="magenta", anchor=SW)\n'%(wName,))
                
                bindMethodL.append( (methodName,id,'click',userLines) )
        
        
        # if not resizable, set resizable to NO
        if self.MainWin.statusBarChkBox_StringVar.get()=='no':
            if self.imADialog:
                self.classInitL.append('        self.resizable(0,0) # Linux may not respect this\n')
            else:
                self.classInitL.append('        self.master.resizable(0,0) # Linux may not respect this\n')
        
        # add a status bar if desired
        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
            self.classInitL.append(getStatusBarSource())
            self.classInitL.append('\n')
            appName = self.formObj.optionD['name']
            self.classInitUserSectionL.append('        self.statusMessage.set("Welcome to %s")\n'%appName)

        # import section is placed 1st
        self.sourceFile.addSection('imports', self.importSectionL, defaultUserCodeL='# Place any user import statements here\n\n')
        # place top_of_init sections of code
        self.sourceFile.addSection('top_of_init', self.classInitL, defaultUserCodeL=self.classInitUserSectionL)
            
        if self.MainWin.menuChkBox_StringVar.get()=='yes':
            menuL = make_menu_src.buildMenuSource( self.formObj.getSpecialOption('menu') )
            menuSrcL = make_menu_src.getMenuSource( menuL, rootName='master'  )
            genCodeL = menuSrcL
            defaultUserCodeL = []
            self.sourceFile.addSection('menuStructure', genCodeL, defaultUserCodeL=defaultUserCodeL)
            
            def addMenuToSource( mItem ):
                for s in mItem.subLabelL:
                    genCodeL = []
                    defaultUserCodeL = []
                    if s.lenSubmenu()==0:
                        name = legalPythonIdentifier('menu_%s_%s'%(mItem.label, s.label))
                        genCodeL.append('    def %s(self):\n'%name)
                        genCodeL.append('        pass\n')
                        defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
                        
                        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                            defaultUserCodeL.append('        self.statusMessage.set("called %s")\n'%name)
                            
                        defaultUserCodeL.append('        print "called %s"\n\n'%name)
                        self.sourceFile.addSection(name, genCodeL, defaultUserCodeL=defaultUserCodeL)
                    else:
                        addMenuToSource( s )
                        
            for mItem in menuL:
                addMenuToSource( mItem )
                
                if mItem.lenSubmenu()==0:
                        genCodeL = []
                        defaultUserCodeL = []
                        name = legalPythonIdentifier('menu_%s'%(mItem.label))
                        genCodeL.append('    def %s(self):\n'%name)
                        genCodeL.append('        pass\n')
                        defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
                        
                        if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                            defaultUserCodeL.append('        self.statusMessage.set("called %s")\n'%name)
                        defaultUserCodeL.append('        print "called %s"\n\n'%name)
                        
                        self.sourceFile.addSection(name, genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        # bind master to <Configure> to handle any resizing, etc.
        if not self.imADialog: # Main Window
            genCodeL = []
            defaultUserCodeL = []
            sectName = 'Master_Configure'
            
        
            genCodeL.append('    def bindConfigure(self, event):\n')
            genCodeL.append('        if not self.initComplete:\n')
            genCodeL.append('            self.master.bind("<Configure>", self.Master_Configure)\n')
            genCodeL.append('            self.initComplete = 1\n\n')
            
            
            genCodeL.append('    def Master_Configure(self, event):\n')
            genCodeL.append('        pass\n')
            defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
            defaultUserCodeL.append('        if event.widget != self.master:\n')
            defaultUserCodeL.append('            if self.w != -1:\n')
            defaultUserCodeL.append('                return\n')
        
            defaultUserCodeL.append('        x = int(self.master.winfo_x())\n')
            defaultUserCodeL.append('        y = int(self.master.winfo_y())\n')
            defaultUserCodeL.append('        w = int(self.master.winfo_width())\n')
            defaultUserCodeL.append('        h = int(self.master.winfo_height())\n')
            defaultUserCodeL.append('        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):\n')
            defaultUserCodeL.append('            self.x, self.y, self.w, self.h = x,y,w,h\n\n')
            defaultUserCodeL.append('        if self.w!=w or self.h!=h:\n')
            defaultUserCodeL.append('            print "Master reconfigured... make resize adjustments"\n')
            defaultUserCodeL.append('            self.w=w\n')
            defaultUserCodeL.append('            self.h=h\n')
            
            #defaultUserCodeL.append('        print "executed method Master_Configure"\n\n')
            self.sourceFile.addSection(sectName, genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        
        # make any bind method statements
        for bm,id,btype,userLines in bindMethodL:
            genCodeL = []
            defaultUserCodeL = []
            sectName = 'compID=%i'%id
            genCodeL.append('    def %s(self, event): #%s method for component ID=%i\n'%(bm,btype,id))
            genCodeL.append('        pass\n')
            defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
            defaultUserCodeL.append('        print "executed method %s"\n'%bm)
            
            if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                defaultUserCodeL.append('        self.statusMessage.set("executed method %s")\n'%bm)
            
            for line in userLines:
                defaultUserCodeL.append(line)
            defaultUserCodeL.append('\n')
            self.sourceFile.addSection(sectName, genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        
        if needVarTraceback:
            for tn in traceNameL:
                genCodeL = []
                defaultUserCodeL = []
                sectName = tn
                genCodeL.append('    def %s(self, varName, index, mode):\n'%tn)
                genCodeL.append('        pass\n')
                defaultUserCodeL.append('        # replace, delete, or comment-out the following\n')
                defaultUserCodeL.append('        print "%s varName, index, mode",varName, index, mode\n'%tn)
            
                if self.MainWin.statusBarChkBox_StringVar.get()=='yes':
                    defaultUserCodeL.append('        self.statusMessage.set("    %s = "+self.%s.get())\n'%(tn[:-9],tn[:-9]))
                defaultUserCodeL.append('        print "    new StringVar value =",self.%s.get()\n\n'%(tn[:-9],) )
                #defaultUserCodeL.append('        if varName == str(self.%s):\n'%tn)
                #defaultUserCodeL.append('            print "    %s changed to",self.%s.get()\n'%(tn,tn))
                self.sourceFile.addSection(sectName, genCodeL, defaultUserCodeL=defaultUserCodeL)
            
        # standard message dialogs
        if self.MainWin.stdDialMessChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardMessageDialogs()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_message_dialogs', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # standard file dialogs
        if self.MainWin.stdDialFileChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardFileDialogs()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_file_dialogs', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # color dialog
        if self.MainWin.stdDialColorChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardColorDialog()]
            defaultUserCodeL = []
            self.sourceFile.addSection('standard_color_dialog', genCodeL, defaultUserCodeL=defaultUserCodeL)
        # alarm logic
        if self.MainWin.stdAlarmChkBox_StringVar.get()=='yes':
            genCodeL = [getStandardAlarmDialog()]
            defaultUserCodeL = ['        print "Alarm called"\n']
            self.sourceFile.addSection('standard_alarm', genCodeL, defaultUserCodeL=defaultUserCodeL)
        
            
        # if making a dialog, need to put in user-editable validate function
        if self.MainWin.mainOrDialog.get() == "dialog":
            genCodeL = [getDialogValidate()]
            defaultUserCodeL = ['        # set values in "self.result" dictionary for return\n',
                '        # for example...\n',
                '        # self.result["age"] = self.Entry_2_StringVar.get() \n\n',
                '        self.result["test"] = "test message" \n',
                '        return 1\n']
            self.sourceFile.addSection('dialog_validate', genCodeL, defaultUserCodeL=defaultUserCodeL)
        
        #self.topCode = ''.join(self.classInitL)
        self.sourceFile.addSection('end',self.endCode, allowUserCode=0)


if __name__ == '__main__':
    import FormDef
    fd = FormDef.FormDef( 'myTestApp' )
    sf = FormSource(fd)
    sf.saveToFile()
    #print 'curdir=',fd.curdir
    #print 'fName=',fd.fName
    
    print
    #print sf.topCode
    #print sf.endCode
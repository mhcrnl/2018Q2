#!/usr/bin/env python
from Tkinter import *
import CompDef
from SelectWidget import GrabHandles
from src_templates import legalPythonIdentifier, getStatusBarSource
import make_menu_src
from MenuMaker_Dialog import Menumaker
import traceback
DEBUG_PRINT = 0

# see book examples in C:\Python23\Doc\TK_Examples

tkWidgetsD = {'button':Button, 'canvas':Canvas, 'checkbutton':Checkbutton, 'entry':Entry, 
    'label':Label, 'labelframe':LabelFrame,'listbox':Listbox, 'message':Message, 
    'radiobutton':Radiobutton, 'text':Text    }

import re
def parsegeometry(geometry):
    m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", geometry)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())
    
def makeDummyWidget( parent, compType, tkOptionD, optionD ):    
    # generalized version of:
    #   return Label( parent, tkOptionD )
    # or
    #   return Button( parent, tkOptionD )
    
    # returns a Label widget if not in tkWidgetsD
    W = tkWidgetsD.get(compType.lower(), Label)(parent, tkOptionD)
    
    if compType.lower()=='canvas':
        #print 'Canvas bg=',W.cget('bg')
        W.configure({'bg':'pink'})
        W.create_text(2,2, text=optionD['name'], fill="black", anchor=NW)
    
    if compType.lower()=='entry':
        W.insert(0, tkOptionD['text'])
    return W
    
class FormWindow( Toplevel ):
        
    def cleanupOnQuit(self):
        if self.MainWin.allow_subWindows_to_close:
            # I'm not sure that transient windows need this, but I'm trying to be careful
            self.parent.focus_set()
            self.destroy()
        
        print '"No Kill I", H.'
        self.MainWin.statusMessage.set('To Exit Applicaton, Use Main Window.')
    
    def changeFormDef(self, myFormDef):
        #self.unbindFormWindow() # unbind all statements
        self.unbindFormWindow()
        allWidgets = self.myCanvas.find_all()
        
        for w in allWidgets:
            self.myCanvas.delete(w)
        
        self.myFormDef = myFormDef
        
        self.showSnapGrid()
        self.showFormWidgets()
        #print '  ---> this lower statement seems like hooey'
        self.lower( self.myCanvas )
        
        #self.bindFormWindow() # issue all bind statements
        try:
            self.refreshEditWindow()
        except:
            pass
            
        if self.initComplete:
            self.bindFormWindow()
        
    def resizeMyForm(self, optD=None):
        if not optD:
            print 'Bailing on resizeMyForm'
            return
            
            
        #print 'resizeMyForm',optD
        w0,h0,x0,y0 = parsegeometry(self.wm_geometry())
        if DEBUG_PRINT: print '=========> In resizeMyForm w0,h0=',w0,h0,'x0,y0=',x0,y0
        
        newVal = 0
        self.myFormDef.optionD['width'] = w0
        self.myFormDef.optionD['height'] = h0
        self.myFormDef.optionD['x'] = x0
        self.myFormDef.optionD['y'] = y0
            
        # holdingResidualReinit can only be set to 1 here
        # the call must come from onConfigureForm
        if optD.get('calledBy','')=='onConfigureForm':
            if self.enterOrLeaveForm:
                self.holdingResidualReinit = 0
            else:
                #print '  calledBy onConfigureForm --> self.holdingResidualReinit = 1'
                self.holdingResidualReinit = 1
                # residual reinit, cleans up after a resize(snap grid, etc.)
            
        
        if optD.has_key('width'):
            w = int(optD['width'])
            if w != w0:
                newVal=1
                w0 = w
                self.myFormDef.optionD['width']=w
        
        if optD.has_key('height'):
            h = int(optD['height'])
            if h != h0:
                newVal=1
                h0 = h
                self.myFormDef.optionD['height']=h
        
        if optD.has_key('x'):
            x = int(optD['x'])
            if x != x0:
                newVal=1
                x0 = x
                self.myFormDef.optionD['x']=x
        
        if optD.has_key('y'):
            y = int(optD['y'])
            if y != y0:
                newVal=1
                y0 = y
                self.myFormDef.optionD['y']=y
                
        if newVal:
            self.unbindFormWindow()
            self.geometry( '%ix%i+%i+%i'%(w0,h0,x0,y0))
            self.bindFormWindow()
            print ' ....... (RESIZED) .........',w0,h0,x0,y0

    
    def snapXY(self, x, y ):
        '''Calculate x and y snap values from raw x and y'''
        snap = int(self.MainWin.snapValue.get())
        snapx = ((x + snap/2)/snap) * snap
        snapy = ((y + snap/2)/snap) * snap
        return snapx, snapy

    def __init__(self, happyObj, MainWin, EditWin, myFormDef):
        self.initComplete = 0
        self.holdingResidualReinit = 0 # can only be set to 1 in resizeMyForm
        
        Toplevel.__init__(self, MainWin, bg='#ADD8E6') #'lightblue': '#ADD8E6',
        self.title('Form Window')
        self.happyObj = happyObj
        self.MainWin = MainWin
        self.EditWin = EditWin
        self.myFormDef = myFormDef
        
        #self.bindsEnabled = 1
        
        x = MainWin.winfo_x() + MainWin.winfo_width() + 10
        y = MainWin.winfo_y() 
        if x<340: x=340
        if y<10: y=10
        # position over to the upper right
        try:
            w,h = int(myFormDef.optionD['width']), int(myFormDef.optionD['height'])
        except:
            w,h = 200, 200
        if DEBUG_PRINT: print '=========>  Initializing FormWindow to w,h=',w,h

        self.menuBar = None # used for dummy menuBar
        self.statusBar = None # used for dummy statusBar
        self.myCanvas = Canvas(self)#,width=w, height=h)
        self.myCanvas.pack(fill=BOTH, expand=True)
        
        self.canvasKeys = self.myCanvas.configure().keys()
        
        #self.geometry( '+%i+%i'%(x,y))
        self.geometry( '%ix%i+%i+%i'%(w,h,x,y))
        
        myFormDef.optionD['width'] = w
        myFormDef.optionD['height'] = h
            
        # show snap grid on form
        self.snapGridObjects = []  # reinitialized in showSnapGrid
        #self.showSnapGrid()  <--- moved to changeFormDef
        #self.showFormWidgets()
        self.changeFormDef( self.myFormDef )
        
        self.activeDummyWidget = None
        self.activeFormDefObj = None
        self.grabHandles = None
        
        # only main window can close this window
        self.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
        
        #self.bind('<Enter>', self.fireUpBindings)
        self.enterOrLeaveForm = 0 # kludgy logic to get Linux to stop resizing
        self.after(1000, self.fireUpBindings)# wait for tk config messages to finish
        
        #self.after_idle(self.fireUpBindings)# wait for tk config messages to finish
        
    def fireUpBindings(self):    #, event):
        if not self.initComplete:
            if DEBUG_PRINT: print "...in fireUpBindings"
            self.bindFormWindow() # issue all bind statements
            self.initComplete = 1 # this is the ONLY place initComplete is assigned True
        
    def showSnapGrid(self):
        for obj in self.snapGridObjects:
            self.myCanvas.delete(obj)
        self.snapGridObjects = []
        
        snap = int(self.MainWin.snapValue.get())
        w,h = int(self.myFormDef.optionD['width']), int(self.myFormDef.optionD['height'])
        if DEBUG_PRINT: print ' in showSnapGrid w,h=',w,h,'  w.cget values=',self.myCanvas.cget('width'),self.myCanvas.cget('height')
        
        if snap>1:
            for i in range(0, w, snap):
                for j in range(0, h, snap):
                    line = self.myCanvas.create_line(i,j,i+1,j+1, fill='red')
                    self.snapGridObjects.append( line )
        
        
    def bindFormWindow(self):
        self.bindsEnabled = 1
        self.bind('<Button>', self.onClickForm)
        #self.bind('<ButtonPress-1>', self.onClickForm)
        self.myCanvas.bind('<Button>', self.onClickForm)
        
        #print '...MAY NOT WANT TO BIND MYCANVAS TO SELF.ONCONFIGUREFORM'
        #self.myCanvas.bind('<Configure>', self.onConfigureForm)
        #self.bind('<Leave>', self.enterOrLeave)
        self.bind('<Enter>', self.enterOrLeave)
        self.bind('<Configure>', self.onConfigureForm)
        
    def enterOrLeave(self, event):
        self.enterOrLeaveForm = 1
        self.maybeReinitForm(event)
        
    def maybeReinitForm(self, event):
        #print 'maybe do reinit/resize'
        if self.holdingResidualReinit: # can only be set to 1 in resizeMyForm
            if DEBUG_PRINT: print 'Performing Residual Reinit/Resize'
            #self.holdingResidualReinit = 0
            
            self.changeFormDef( self.myFormDef )
            self.showWidgetInEditWindow(self, self.myFormDef, event )
            self.holdingResidualReinit = 0
        
    def unbindFormWindow(self):
        self.bindsEnabled = 0
        self.unbind('<Button>')
        self.unbind('<Configure>')
        self.unbind('<Leave>')
        self.unbind('<Enter>')
        self.myCanvas.unbind('<Button>')
        self.myCanvas.unbind('<Configure>')

    def onConfigureForm(self, event):
        if self.initComplete==0:
            return
        # make any changes input on the Edit Window
        
        if event.widget not in [self]: #, self.myCanvas]:
            return
            
            
        #if event.widget == self.myCanvas:
        #    return
            
        # in case the form is being resized, try to resize it
        #print '--------------->  onConfigureForm  event type=',event.type
        
        # Linux does NOT pass accurate x and y event values on resize in some cases
        #optD = {'x':event.x, 'y':event.y, 'width':event.width, 'height':event.height, 
        #    'calledBy':'onConfigureForm'}
                
        optD = {'calledBy':'onConfigureForm','width':event.width, 'height':event.height}
                
        if DEBUG_PRINT: print 'calling resizeMyForm with optD=',optD
        self.resizeMyForm( optD )
        #print event.widget,"config: width",event.width,' height',event.height#,\
        #'x,y=',event.x,event.y,'x_root,y_root=',event.x_root,event.y_root
            
        #if self.activeDummyWidget == self:
        #    self.refreshEditWindow()
        
        
        #print traceback.print_stack()
        self.enterOrLeaveForm = 0 # kludge to stop Linux from resizing
        

    
    def deleteActiveDummyWidget(self): # COMPLETELY REMOVE FROM FORM... WARNING.
        if DEBUG_PRINT: print 'self.activeDummyWidget',self.activeDummyWidget
        if DEBUG_PRINT: print 'self.activeFormDefObj',self.activeFormDefObj,self.activeFormDefObj.name
        if DEBUG_PRINT: 
            for c in self.myFormDef.compObjL:
                print c.name
            print
        self.myFormDef.delComponentByName(self.activeFormDefObj.name)
        self.changeFormDef(self.myFormDef)
    
    def showWidgetInEditWindow(self, dummyWidget, formDefObj, event ):
        self.activeDummyWidget = dummyWidget
        self.activeFormDefObj = formDefObj
        
        if dummyWidget != self:
            self.unbindFormWindow()
            self.grabHandles = GrabHandles(self, self.MainWin, self.myCanvas, dummyWidget, 
                formDefObj, self.myFormDef, self.onClickForm, 
                self.bindFormWindow, event, self.refreshEditWindow)
            #print 'need to MARK the active widget'
        self. refreshEditWindow()
        
    def refreshEditWindow(self):
            
        # remove any widget from EditWin
        for k,i in self.EditWin.children.items():
            i.destroy()
            
        print 'showing in Edit, name=',self.activeFormDefObj.optionD['name']
        self.MainWin.statusMessage.set( self.activeFormDefObj.optionD['name'] + ' selected' )
                    
        # display widget options in EditWin
        Label(self.EditWin, bg='#90EE90', text=self.activeFormDefObj.compType.capitalize()+\
            ' Layout').pack(side=TOP,  fill=X)
                    
        # FIRST show name and placement info
        keys = self.activeFormDefObj.optionD.keys()
        keys.sort()
        for k in keys:
            frame = Frame( self.EditWin )
            lab = Label(frame, text=k, width='15', anchor='e' )
            e = StringVar()
            eb = Entry(frame, textvariable=e )
            e.set(str(self.activeFormDefObj.optionD[k]))
            lab.pack(side=LEFT)
            eb.pack(side=LEFT)
            frame.pack()
                        
            eb.tk_happy_option = str(k)
            eb.bind('<FocusOut>', self.onLeaveEntry)
            eb.bind('<Return>', self.printHitReturn)
                    
        # NEXT show legal Tk options
        Label(self.EditWin, bg='#90EE90', text=self.activeFormDefObj.compType.capitalize()+' Tk Options').pack(side=TOP,  fill=X)
        keys = self.activeFormDefObj.helpD.keys()
        keys.sort()
        for k in keys:
            frame = Frame( self.EditWin )
            lab = Label(frame, text=k, width='15', anchor='w' )
            e = StringVar()
            eb = Entry(frame, textvariable=e )
                        
            #val = self.activeDummyWidget.cget( k )
            val = self.activeFormDefObj.tkOptionD.get(k,'')
            if val=='':
                val=self.activeDummyWidget.cget( k )
            
            #e.set(str(self.activeFormDefObj.tkOptionD[k]))
            e.set(str(val))
                        
            lab.pack(side=LEFT)
            eb.pack(side=LEFT)
            frame.pack()
                        
            eb.tk_happy_option = str(k)
            eb.bind('<FocusOut>', self.onLeaveEntry)
            eb.bind('<Return>', self.printHitReturn)
            
    def printHitReturn(self, event):
        if DEBUG_PRINT: print 'Hit Return... event',event
        self.onLeaveEntry(event)
            
    def onClickForm(self, event):
        
        if self.holdingResidualReinit:
            self.maybeReinitForm(event)
        
        if not self.bindsEnabled:
            return
            
        if DEBUG_PRINT: print 'clicked form'
        
        if DEBUG_PRINT: print 'self.myFormDef.tkOptionD',self.myFormDef.tkOptionD
        #print 'self.winfo_parent=',self.winfo_parent()
        #print 'self.winfo_name=',self.winfo_name()
        #print 'self.winfo_toplevel=',self.winfo_toplevel()
        #print 'self.geometry=',self.geometry()
        #print 'self.aspect=',self.aspect()
        #print 'self.maxsize=',self.maxsize()
        #print 'self.minsize=',self.minsize()
        #print 'self.resizable=',self.resizable()
            
        # remove any widget from EditWin
        for k,i in self.EditWin.children.items():
            i.destroy()
                    
        # ========== CLICKED MAIN FORM WINDOW FRAME ==========
        if DEBUG_PRINT: print 'event.widget',event.widget
        if event.widget == self or event.widget == self.myCanvas\
            or event.widget in self.snapGridObjects:
            
            # see what widget is selected for placement on the main form
            placementWidgetType = self.MainWin.placementWidgetType.get()
            
            # if placement Widget is in tkWidgets Dictionary, place it.
            if placementWidgetType in tkWidgetsD.keys():
                
                if self.MainWin.multiPlacements_StringVar.get()=='no':
                    #self.MainWin.placementWidgetType.set('none')
                    self.happyObj.clearPlacementWidgetType()
                    
                
                self.unbindFormWindow() # up to grab handles to reinstate bind for FormWin
                snapx, snapy = self.snapXY( event.x, event.y )
                name = self.myFormDef.nextComponentName( placementWidgetType )
                self.myFormDef.addComponent( placementWidgetType, {'name':name, 'x':snapx,'y':snapy}, 
                    {'text':name+' text'} ) # text property may be deleted by CompDef class
                obj = self.myFormDef.compObjL[-1]
                comp = makeDummyWidget( self.myCanvas, obj.compType, obj.tkOptionD, obj.optionD )
                
                self.myCanvas.create_window( snapx, snapy, window=comp, tags=comp, anchor='nw')
                
                #comp.place(x=event.x, y=event.y)
                #comp.focus_force()
                #print dir(comp)
                print
                if DEBUG_PRINT: print 'just added',comp.winfo_name()
                obj.dummyWidget = comp
                # self.activeFormDefObj = obj done in showWidgetInEditWindow
                
                #print
                #print 'self children=',self.children
                self.showWidgetInEditWindow(comp, obj, event )
                
            # if not placing a widget, then show toplevel window's properties
            if placementWidgetType == 'none':
                #print self.children
                #self.activeFormDefObj = self.myFormDef  done in showWidgetInEditWindow
                
                # show self NOT self.myCanvas so that x,y,h,and w are all for the frame not myCanvas
                self.showWidgetInEditWindow(self, self.myFormDef, event )
            
        # ==== CLICKED A WIDGET =========
        else: # just clicked a widget
            for obj in self.myFormDef.compObjL:
                if obj.dummyWidget == event.widget:
                    
                    self.showWidgetInEditWindow(event.widget, obj, event )
                    
                    # stop iterating on objects, we just finished showing one on the EditWin
                    break
                    
        # force a repaint of the form
        #print "self.MainWin.event_generate('<Visibility>')???"
        
    def onLeaveEntry(self, event):
        if DEBUG_PRINT: print 'Leave Entry...',event.widget.tk_happy_option, event.widget.get()
        
        if self.activeDummyWidget:
            opt = str(event.widget.tk_happy_option)
            val = str(event.widget.get())
            optD = { opt:val }
            if opt=='name':
                # set new value of property on FormDef object
                legal_val = legalPythonIdentifier( val )
                self.activeFormDefObj.optionD['name'] = legal_val
                self.activeFormDefObj.name = legal_val
                
                self.refreshEditWindow()
                # now set the new value on the dummyWidget in FormWin
                #self.activeDummyWidget.configure( text=val )
            
            # position changes to the Frame
            elif self.activeDummyWidget == self and opt in ['x','y','width','height']:
                
                # apply height and width to toplevel form
                if DEBUG_PRINT: print 'applying change to',self.activeFormDefObj.optionD['name']
                y=int(self.activeFormDefObj.optionD['y'])
                x=int(self.activeFormDefObj.optionD['x'])
                w=int(self.activeFormDefObj.optionD['width'])
                h=int(self.activeFormDefObj.optionD['height'])
                if opt=='x': x=int(val)
                if opt=='y': y=int(val)
                if opt=='width': w=int(val)
                if opt=='height': h=int(val)
                
                self.resizeMyForm( {opt:val} )
                #print 'Set Geometry of TopLevel window to w,h,x,y',w,h,x,y
                
                # set new value of property on FormDef object
                self.activeFormDefObj.optionD['x']=x
                self.activeFormDefObj.optionD['y']=y
                self.activeFormDefObj.optionD['width']=w
                self.activeFormDefObj.optionD['height']=h
                
                
                #try:
                #    self.grabHandles.returnConrolToFormWindow(event)
                #except:
                #    print 'no grab handles to escape'
                    
                self.changeFormDef( self.myFormDef )
            elif opt=='compID':
                print 'can NOT change compID'
            elif opt=='pixelWidth':
                self.activeFormDefObj.optionD[opt] = val
                self.myCanvas.itemconfig(self.activeDummyWidget, width=val)
                
            elif opt =='pixelHeight':
                self.activeFormDefObj.optionD[opt] = val
                self.myCanvas.itemconfig(self.activeDummyWidget, height=val)
                
            elif opt in ['x','y']:
                # set new value of property x or y on FormDef object
                
                # need to use the canvas coords command to change x and y
                xnow,ynow = self.myCanvas.coords(self.activeDummyWidget)
                xnow=int(xnow)
                ynow=int(ynow)
                if opt=='x':
                    xnow=val
                else:
                    ynow=val
                
                self.activeFormDefObj.optionD['x'] = xnow
                self.activeFormDefObj.optionD['y'] = ynow
                self.myCanvas.coords(self.activeDummyWidget, xnow, ynow)
                
                #try:
                #    self.grabHandles.returnConrolToFormWindow(event)
                #except:
                #    print 'no grab handles to escape'
            elif opt in ['scrolly','scrollx']:
                if val in ['no','yes']:
                    self.activeFormDefObj.optionD[opt] = val
                else:
                    print 'ERROR... only "yes" or "no" is allowed'
                    oldval = self.activeFormDefObj.optionD[opt]
                    print 'WARNING... restoring old value=',oldval
                    tv = event.widget.cget('textvariable')
                    #print 'tv=',tv  # tv is a name like PY_VAR7
                    self.setvar(name=tv, value=oldval)
                    self.MainWin.statusMessage.set('Input Error on "%s". Previous value restored.'%opt)
                    
            else: # should be tk options for the widget
                
                # try to set the tk option
                # if it is an error, restore the previous value into Entry
                try:
                    self.activeDummyWidget.configure( optD )
                    # set new value of property on FormDef object
                    self.activeFormDefObj.tkOptionD[opt] = val
                    
                    if opt=='text'  and hasattr(self.activeFormDefObj,'compType'):
                        if self.activeFormDefObj.compType.lower()=='entry':
                            self.activeDummyWidget.delete(0, END)
                            self.activeDummyWidget.insert(0, val)
                    
                    # update myCanvas if required
                    if self.activeDummyWidget == self:
                        if self.myFormDef.tkOptionD.has_key(opt):
                            oldval = self.activeDummyWidget.cget(opt)
                            if DEBUG_PRINT: print 'Configure myCanvas...'
                            if opt in self.canvasKeys:# and oldval != val:
                                self.myCanvas.configure({opt:self.myFormDef.tkOptionD[opt]})
                                if DEBUG_PRINT: print 'Configure myCanvas...',{opt:self.myFormDef.tkOptionD[opt]}
                                #self.focus()
                    
                except:
                    #print traceback.print_stack()
                    print traceback.print_exc()
                    oldval = self.activeDummyWidget.cget(opt)
                    print 'WARNING... restoring old value=',oldval
                    tv = event.widget.cget('textvariable')
                    #print 'tv=',tv  # tv is a name like PY_VAR7
                    self.setvar(name=tv, value=oldval)
                    self.MainWin.statusMessage.set('Input Error on "%s". Previous value restored.'%opt)
                    
    def changeMenuStructure(self):
        
        if self.myFormDef:
            dialog = Menumaker(self.MainWin, "Define Menu Structure",
                self.myFormDef.getSpecialOption('menu'))
            if DEBUG_PRINT: print dialog.result
            
            if type(dialog.result) == type({}):
                
                menuStr = dialog.result.get('menu','').strip()
                if len( menuStr ) > 0:
                    self.myFormDef.setSpecialOption('menu',menuStr)
                    print 'Recording new Menu Definition'
        self.changeFormDef( self.myFormDef )
        
        
    def showFormWidgets(self): 
        # dummy menu logic
        #print 'begin showFormWidgets.  geom=',parsegeometry(self.wm_geometry())
        if self.myFormDef.getSpecialOption('hasmenu')=='yes':
            MainWin = self # needed for source in make_menu_src
            menuL = make_menu_src.buildMenuSource( self.myFormDef.getSpecialOption('menu') )
            if len(menuL)>0:
                menuSrcL = make_menu_src.getMenuSource( menuL, rootName='self'  )
                print "   --- placing dummy menu"
                
                for s in menuSrcL:
                    #print s,
                    i = s.find(', command')
                    if i>-1:
                        s = s[:i] + ', command=self.changeMenuStructure)'
                    s = s.strip()
                    #print s
                    exec(s) # self.menuBar is created by the exec command
                self.config(menu=self.menuBar)
                #print "   ---"
                
                #  width and height apply to CLIENT area
                #self.geometry( '%ix%i'%(int(self.myFormDef.optionD['width']), int(self.myFormDef.optionD['height'])))
                
                
        else:
            if self.menuBar: # might have to remove a menu bar that was previously added
                for k,i in self.menuBar.children.items():
                    i.destroy()
                self.menuBar.destroy()
                if DEBUG_PRINT: print '\N============>>>>> REMOVING DUMMY MENU'
            self.menuBar = None # used for dummy menuBar


        # dummy statusbar logic
        if self.myFormDef.getSpecialOption('hasstatusbar')=='yes':
            if self.statusBar==None:
                self.statusBar = 1
                statusBarSrc = getStatusBarSource()
                statusBarSrc = statusBarSrc.replace('self.master','self')
                sL = statusBarSrc.split('\n')
                for s in sL:
                    s = s.strip()
                    exec(s) # self.statusbar is created by exec command
        else:
            self.statusBar = None
            try: 
                self.statusMessage.destroy()
            except:
                pass
            try:
                self.statusbar.destroy()
            except:
                pass
        


        
        for obj in self.myFormDef.compObjL:
            #print 'showing',obj.compType,obj.name
            comp = makeDummyWidget( self, obj.compType, obj.tkOptionD, obj.optionD )
            
            id = self.myCanvas.create_window( obj.optionD['x'], obj.optionD['y'], 
                window=comp, tags=comp, anchor='nw')
            
            if obj.optionD.has_key('pixelWidth'):
                self.myCanvas.itemconfig(id, width=obj.optionD['pixelWidth'])
            
            if obj.optionD.has_key('pixelHeight'):
                self.myCanvas.itemconfig(id, height=obj.optionD['pixelHeight'])
            
            x1,y1,x2,y2 = self.myCanvas.bbox( id )# requires tags option in create_window
            if DEBUG_PRINT: print 'placing',comp,'with bbox=',x1,y1,x2,y2
            
            #comp.place(x=obj.optionD['x'], y=obj.optionD['y'])
            obj.dummyWidget = comp
            
        for k in self.myFormDef.tkOptionD.keys():
            if k in self.canvasKeys:
                if DEBUG_PRINT: print 'setting myCanvas',k,'to',self.myFormDef.tkOptionD[k]
                self.myCanvas.configure({k:self.myFormDef.tkOptionD[k]})
        #print '  end showFormWidgets.  geom=',parsegeometry(self.wm_geometry())
                    
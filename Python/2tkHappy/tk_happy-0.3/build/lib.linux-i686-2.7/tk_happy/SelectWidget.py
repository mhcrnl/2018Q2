#!/usr/bin/env python
from Tkinter import *
DEBUG_PRINT = 0

class GrabHandles( object ):
    
    def __init__(self, FormWin, MainWin, canvas, widget, formDefObj, formDefTopObj, unhandledClickRoutine, 
        bindCallingFormWindow, event, refreshEditWindow, color='blue', hw=4):
            
        self.FormWin = FormWin
        self.MainWin = MainWin
        self.canvas = canvas
        self.widget = widget # widget is already placed on canvas with create_window
        self.formDefObj = formDefObj # form definition object
        self.formDefTopObj = formDefTopObj # form definition object
        
        self.unhandledClickRoutine = unhandledClickRoutine # if grabbers can't handle click, use this callback
        self.bindCallingFormWindow = bindCallingFormWindow # when returning control back to calling window
        self.refreshEditWindow = refreshEditWindow # when x,y,width, or height change, refresh edit window
        
        # assume that callingForm has unbound all button handlers
        #print '__init__ self.canvas.find_all()',self.canvas.find_all()
        #print 'self.canvas.find_withtag( widget )[0]',self.canvas.find_withtag( widget )[0]
        self.widgetID = self.canvas.find_withtag( widget )[0] # returns a tuple
        
        allWidgets = self.canvas.find_all()
        self.otherWidgetL = []
        self.gridLineL = []
        for w in allWidgets:
            if w != self.widgetID:
                try:
                    owtag = self.canvas.itemcget(w,'window')
                    self.otherWidgetL.append(w)
                except:
                    self.gridLineL.append(w)
                    pass
                
        #print 'allWidgets',allWidgets
        #print 'other widgets',self.otherWidgetL
        
        #print 'unbinding <Button> for widget'
        #self.canvas.tag_unbind( self.widgetID, '<Button>' )
        #self.canvas.unbind('<Button>')
        
        self.hw = hw # height and width of handles
        self.color = color
        
        self.activeGrabberID = self.widgetID # initial select starts here
        self.rubberRect = None
        self.rubberRectL = []
        self.dx = 0
        self.dy = 0
        
        self.showGrabbers()
        #self.grabx,self.graby = None, None # nothing's been grabbed yet
        self.grabx = int(self.canvas.canvasx(event.x))
        self.graby = int(self.canvas.canvasy(event.y))
        
        self.FormWin.bind('<Key>', self.hitKeyOverGrabObject )
        
        #self.FormWinGeometry = self.FormWin.geometry()
        #self.FormWin.bind('<Enter>', self.onEnterFormWin )
        
        # disallow resizing with Grabbers active
        self.FormWin.minsize(self.formDefTopObj.optionD['width'],self.formDefTopObj.optionD['height'])
        self.FormWin.maxsize(self.formDefTopObj.optionD['width'],self.formDefTopObj.optionD['height'])


    #def onEnterFormWin(self, event):
    #    # if the window geometry changes, go back to FormWindow
    #    if self.FormWinGeometry != self.FormWin.geometry():
    #        self.FormWin.holdingResidualReinit = 1
    #        self.returnConrolToFormWindow( event )
        
    def clearAllHandlersAndGrabHandles(self):
        self.FormWin.unbind('<Key>')
        # called from FormWindow when 
        self.widget.config( cursor='arrow' )
        self.widget.unbind( '<ButtonPress-1>')
        self.widget.unbind( '<Button1-Motion>')
        self.widget.unbind( '<ButtonRelease-1>')
        self.widget.unbind( '<Enter>')
        self.widget.unbind( '<Leave>')
        
        try: # self.widgetID might be deleted
            self.canvas.tag_unbind(self.widgetID, '<ButtonPress-1>')
            self.canvas.tag_unbind(self.widgetID, '<Button1-Motion>')
            self.canvas.tag_unbind(self.widgetID, '<ButtonRelease-1>')
            self.canvas.tag_unbind(self.widgetID, '<Enter>')
            self.canvas.tag_unbind(self.widgetID, '<Leave>')
        except:
            pass
        
        try:
            self.canvas.tag_unbind(self.returnRect, '<ButtonPress-1>')
        except:
            pass
            
        
        # other widgets on canvas should indicate a return to FormWin
        for ow in self.otherWidgetL:
            try:
                owtag = self.canvas.itemcget(ow,'window')
                owtag = self.canvas.nametowidget(owtag)
                if DEBUG_PRINT: print 'owtag',owtag
                owtag.unbind('<ButtonPress-1>')
            except:
                pass
            
        
        for ow in self.otherWidgetL:
            try: # might be deleted
                self.canvas.tag_unbind(ow, '<ButtonPress-1>')
            except:
                pass
        
        self.canvas.delete(self.returnRect)
        #self.canvas.unbind( '<ButtonPress-1>')
        
        handL = [ self.ul_id ,self.l_id,self.ll_id ,self.ur_id ,self.r_id ,self.lr_id ,self.top_id,self.bot_id ]
        for hand in handL:
            self.canvas.delete(hand)
            hand = None
        
    def setActiveGrabberID(self, event):
        # the widget will not get selected with find_closest
        if event.widget == self.widget:
            self.activeGrabberID = self.widgetID
            return
        
        # if not widget, then start looking at grab handles
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # make small rectagles to capture grab handles
        eps = self.hw+2
        
        #self.canvas.create_rectangle ( x-eps,y-eps,x+eps,y+eps,
        #         outline='red' )
        
        enclosedL = self.canvas.find_enclosed(x-eps,y-eps,x+eps,y+eps)
        if DEBUG_PRINT: print 'enclosedL',enclosedL
        if len(enclosedL)>0:
            # initialize active grabber id to 1st in list, but then make sure it's not a grid line
            self.activeGrabberID = enclosedL[0]
            for id in enclosedL:
                if id not in self.gridLineL:
                    self.activeGrabberID = id
                    break
        else:
            self.activeGrabberID = self.canvas.find_closest(x,y)[0]
    
    def newBBox(self):
        # based on dx,dy,and activeGrabberID get new bbox
        
        # self.x1,self.y1,self.x2,self.y2 
        
        #[self.widgetID, self.ul_id ,self.l_id,self.ll_id ,self.ur_id ,self.r_id ,self.lr_id ,self.top_id,self.bot_id ]
        
        x1,y1,x2,y2 = self.x1*1,self.y1*1,self.x2*1,self.y2*1 # use *1 to get new number objects

        # do x1
        if self.activeGrabberID in [self.widgetID, self.ul_id ,self.l_id,self.ll_id  ]:
            x1 = int(x1 + self.dx)
            
        # do y1
        if self.activeGrabberID in [self.widgetID, self.ul_id ,self.ur_id ,self.top_id ]:
            y1 = int(y1 + self.dy)
            
        # do x2
        if self.activeGrabberID in [self.widgetID, self.ur_id ,self.r_id ,self.lr_id  ]:
            x2 = int(x2 + self.dx)
            
        # do y2
        if self.activeGrabberID in [self.widgetID, self.ll_id ,self.lr_id ,self.bot_id  ]:
            y2 = int(y2 + self.dy)
            
        return x1,y1,x2,y2
        
    def changeCursor(self, event):
        #print 'event.widget', event.widget
        self.setActiveGrabberID( event)
        #print 'changeCursor activeGrabberID=',self.activeGrabberID
        #print self.cursorD
        try:
            self.canvas.config(cursor=self.cursorD[self.activeGrabberID])
        except:
            pass
        
    def restoreCursor(self, event):
        self.canvas.config(cursor='arrow')
        
    def hitKeyOverGrabObject(self, event):
        if DEBUG_PRINT: print "pressed char", repr(event.char),'keysym', event.keysym,'keycode', event.keycode
        
        if event.keysym == 'Delete':
            if self.activeGrabberID in self.legalGrabL:
                print 'Deleting currently selected widget, ID=',self.widgetID
                self.FormWin.deleteActiveDummyWidget()
                #self.clearAllHandlersAndGrabHandles()
                #self.bindCallingFormWindow()
                self.returnConrolToFormWindow(event)
        
    def btnPressHandle(self, event):
        #print 'button press'
        #print 'btnPressHandle self.canvas.find_all()',self.canvas.find_all()
        self.grabx = int(self.canvas.canvasx(event.x))
        self.graby = int(self.canvas.canvasy(event.y))
        if DEBUG_PRINT: print 'grab x,y=',self.grabx, self.graby
        
        self.setActiveGrabberID( event)
        self.dx = 0
        self.dy = 0
        if DEBUG_PRINT: print 'grabbed item',self.activeGrabberID
        
        if self.activeGrabberID not in self.legalGrabL:
            self.returnConrolToFormWindow(event)
        
        
    def returnConrolToFormWindow(self, event):
        # restore resizing ability
        self.FormWin.minsize(0,0)
        self.FormWin.maxsize(0,0)

        KEYPRESS_EVENT = 2
        BUTTONPRESS_EVENT = 4
        if int(event.type) == KEYPRESS_EVENT:
            # this is a key press command
            if DEBUG_PRINT: print "Key Press Command... return to Form Window"
            self.clearAllHandlersAndGrabHandles()
            self.bindCallingFormWindow()
            
        else:
            if DEBUG_PRINT: print "self.canvas.cget('cursor')",self.canvas.cget('cursor')
            if DEBUG_PRINT: print 'event type=',event.type
            # this is a click outside of the grabber
            if DEBUG_PRINT: print "Click outside of GrabHandles"
            self.clearAllHandlersAndGrabHandles()
            self.bindCallingFormWindow()
            self.unhandledClickRoutine(event)
        
    def delAllRubberRectangle(self):
        while len(self.rubberRectL)>0:
            rr = self.rubberRectL.pop()
            self.canvas.delete(rr)
            
    def makeRubberRectangle(self, bb):
        self.delAllRubberRectangle()
        rr = self.canvas.create_rectangle ( bb, outline=self.color )
        self.rubberRectL.append(rr)
        self.rubberRect = rr
        
    def btnMotionHandle(self, event):
        #print 'btnMotionHandle self.canvas.find_all()',self.canvas.find_all()
        if 1:#try:
            self.dx = int(self.canvas.canvasx(event.x) - self.grabx) * self.dxMultD[self.activeGrabberID]
            self.dy = int(self.canvas.canvasy(event.y) - self.graby) * self.dyMultD[self.activeGrabberID]
        #except:
        #    self.dx = 0
        #    self.dy = 0
        #print '<%i,%i>'%(self.dx,self.dy),
        
        newbb = self.newBBox()
        self.makeRubberRectangle(newbb)
        
        
    def btnReleaseHandle(self, event):
        self.delAllRubberRectangle()
        
        #if self.grabx == None:
        #    self.dx = 0
        #    self.dy = 0
        #    return
            
        self.releasex = int(self.canvas.canvasx(event.x))
        self.releasey = int(self.canvas.canvasy(event.y))
        self.dx = int((self.releasex - self.grabx) * self.dxMultD[self.activeGrabberID])
        self.dy = int((self.releasey - self.graby) * self.dyMultD[self.activeGrabberID])
            
        if DEBUG_PRINT: print 'release x,y=',self.releasex, self.releasey
        if DEBUG_PRINT: print '\nbutton release'
        if DEBUG_PRINT: print 'dx dy=',self.dx,self.dy
        
        if (self.dx != 0) or (self.dy != 0):
            self.moveOrModifyWidget()
        
    def moveOrModifyWidget(self):
        newbb = self.newBBox()
        
        if DEBUG_PRINT: print 'final bounding box=',newbb
        
        x1,y1,x2,y2 = self.initBbox
        x1f,y1f,x2f,y2f = newbb
        wi = x2-x1+1
        wf = x2f-x1f+1
        hi = y2-y1+1
        hf = y2f-y1f+1
        
        #change form definition object
        self.formDefObj.optionD['x']=x1f
        self.formDefObj.optionD['y']=y1f
        #self.formDefObj.tkOptionD['width']=wf
        self.formDefObj.setPixelWidth(wf)
        #self.formDefObj.tkOptionD['height']=hf
        self.formDefObj.setPixelHeight(hf)
        if DEBUG_PRINT: print 'self.formDefObj.optionD',self.formDefObj.optionD
        
        if DEBUG_PRINT: print 'wi,wf',wi,wf
        if DEBUG_PRINT: print 'hi,hf',hi,hf
        if DEBUG_PRINT: print 'x1,x1f',x1,x1f
        if DEBUG_PRINT: print 'y1,y1f',y1,y1f
        grabL = [self.widgetID, self.ul_id ,self.l_id,self.ll_id ,self.ur_id ,self.r_id ,self.lr_id ,self.top_id,self.bot_id ]
        if x1!=x1f or y1!=y1f:
            snap = int(self.MainWin.snapValue.get())
            snapx = int(int(x1f + snap/2)/snap) * snap
            snapy = int(int(y1f + snap/2)/snap) * snap
            if DEBUG_PRINT: print 'snapx,snapy',snapx,snapy
            movex, movey = snapx-x1, snapy-y1
            if DEBUG_PRINT: print 'movex, movey',movex, movey,'for snap=',snap
            
            for grab in grabL:
                self.canvas.move(grab, movex, movey)
                
            newbb = snapx,snapy,snapx+wf,snapy+hf # need to reinitialize because of snap logic
            self.formDefObj.optionD['x']=snapx
            self.formDefObj.optionD['y']=snapy
        else:
            if wi != wf:
                self.canvas.itemconfig(self.widgetID, width=wf)
                
                for grab in [self.ur_id ,self.r_id ,self.lr_id ]:
                    self.canvas.move(grab, wf-wi, 0)
                for grab in [self.top_id,self.bot_id ]:
                    self.canvas.move(grab, (wf-wi)/2, 0)
                    
            if hi != hf:
                self.canvas.itemconfig(self.widgetID, height=hf)
                grabL = [self.ul_id ,self.l_id,self.ll_id ,self.ur_id ,self.r_id ,self.lr_id ,self.top_id,self.bot_id ]
                for grab in [self.ll_id ,self.lr_id ,self.bot_id  ]:
                    self.canvas.move(grab, 0, hf-hi)
                for grab in [self.l_id,self.r_id  ]:
                    self.canvas.move(grab, 0, (hf-hi)/2)
            
        self.initBbox = newbb
        self.x1,self.y1,self.x2,self.y2 = newbb
        
        # refresh edit window
        if DEBUG_PRINT: print '==========> REFRESHING edit window'
        self.refreshEditWindow()

        
    def showGrabbers(self):
        
        #x1,y1 = self.canvas.coords(self.widget) # requires tags option in create_window
        #x1=int(x1)
        #y1=int(y1)
        #print 'x1,y1=',x1,y1
        #print 'self.canvas.find_all()',self.canvas.find_all()
                
        #print self.canvas.itemcget( self.widget, 'width' )
        
        if DEBUG_PRINT: print "self.widget.cget('width')",self.widget.cget('width')
        try:
            if DEBUG_PRINT: print "self.widget.cget('height')",self.widget.cget('height')
        except:
            if DEBUG_PRINT: print 'widget has no height'
        x1,y1,x2,y2 = self.canvas.bbox( self.widget )# requires tags option in create_window
        #x1,x2 = self.canvas.canvasx(x1), self.canvas.canvasx(x2)
        #y1,y2 = self.canvas.canvasy(y1), self.canvas.canvasy(y2)
        x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
        
        self.initBbox = (x1,y1,x2,y2)
        
        if DEBUG_PRINT: print 'x1,y1,x2,y2',x1,y1,x2,y2
        self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
        
        
        pixelW = x2-x1+1
        pixelH = y2-y1+1
        if DEBUG_PRINT: print 'pixelW,pixelH',pixelW,pixelH
        self.formDefObj.setPixelWidth(pixelW)
        self.formDefObj.setPixelHeight(pixelH)
        
        
        if DEBUG_PRINT: print "self.widget.cget('width')",self.widget.cget('width')
        try:
            if DEBUG_PRINT: print "self.widget.cget('height')",self.widget.cget('height')
        except:
            pass
        
        # make return rectangle.  If clicked, then return to FormWin
        try:
            wform = self.formDefTopObj.optionD['width'] + 2
            hform = self.formDefTopObj.optionD['height'] + 2
        except:
            wform = 300
            hform = 300
        if int(wform)<1: wform=300
        if int(hform)<1: hform=300
            
        self.returnRect = self.canvas.create_rectangle ( 1, 1, wform, hform,
                 outline=self.color, fill=self.canvas.cget('bg') ) 
        self.canvas.tag_bind(self.returnRect, '<ButtonPress-1>',   self.returnConrolToFormWindow )
        self.canvas.tag_lower(self.returnRect)# need to lower in zorder to make snap grid visible
        
        # other widgets on canvas should indicate a return to FormWin
        for ow in self.otherWidgetL:
            try:
                owtag = self.canvas.itemcget(ow,'window')
                owtag = self.canvas.nametowidget(owtag)
                if DEBUG_PRINT: print 'owtag',owtag
                owtag.bind('<ButtonPress-1>',   self.returnConrolToFormWindow )
            except:
                if DEBUG_PRINT: print 'No "window" property on widget tag',ow

        
        def makeGrabRect(xul, yul):
            return self.canvas.create_rectangle ( xul, yul, xul+self.hw, yul+self.hw,
                fill=self.color, outline=self.color )
        
        # left side grabbers
        xleft = x1 - self.hw -1
        yul = y1 - self.hw
        self.ul_id = makeGrabRect(xleft, yul)

        yul = y1 + (y2-y1)/2 - self.hw/2
        self.l_id = makeGrabRect(xleft, yul)

        yul = y2
        self.ll_id = makeGrabRect(xleft, yul)
        
        # right side grabbers
        xleft = x2 
        yul = y1 - self.hw
        self.ur_id = makeGrabRect(xleft, yul)

        yul = y1 + (y2-y1)/2 - self.hw/2
        self.r_id = makeGrabRect(xleft, yul)

        yul = y2
        self.lr_id = makeGrabRect(xleft, yul)
        
        # top and bottom grabbers
        xleft = (x1+x2)/2 - self.hw/2
        yul = y1 - self.hw
        self.top_id = makeGrabRect(xleft, yul)

        yul = y2
        self.bot_id = makeGrabRect(xleft, yul)
        
        # now bind handlers
        self.legalGrabL = [self.widgetID, self.ul_id ,self.l_id,self.ll_id ,self.ur_id ,self.r_id ,self.lr_id ,self.top_id,self.bot_id ]
        
        for grab in self.legalGrabL:
            self.canvas.tag_bind(grab, '<ButtonPress-1>',   self.btnPressHandle )
            self.canvas.tag_bind(grab, '<Button1-Motion>',  self.btnMotionHandle )
            self.canvas.tag_bind(grab, '<ButtonRelease-1>', self.btnReleaseHandle )
            
            self.canvas.tag_bind(grab, '<Enter>', self.changeCursor )
            self.canvas.tag_bind(grab, '<Leave>', self.restoreCursor )
            
        # bind widget itself.
        # will need to fix cursor and unbind events
        self.widget.config( cursor='fleur' )
        self.widget.bind( '<ButtonPress-1>',   self.btnPressHandle )
        self.widget.bind( '<Button1-Motion>',  self.btnMotionHandle )
        self.widget.bind( '<ButtonRelease-1>', self.btnReleaseHandle )
            
        self.widget.bind( '<Enter>', self.changeCursor )
        self.widget.bind( '<Leave>', self.restoreCursor )
        
        self.cursorD = {self.widgetID:'fleur',
            self.ul_id:'top_left_corner' ,self.l_id:'left_side',
            self.ll_id:'bottom_left_corner' ,self.ur_id:'top_right_corner' ,self.r_id:'right_side' ,
            self.lr_id:'bottom_right_corner' ,self.top_id:'top_side', self.bot_id:'bottom_side' }

            
        self.dxMultD = {self.widgetID:1, self.ul_id:1 ,self.l_id:1, self.ll_id:1 ,self.ur_id:1 ,
            self.r_id:1 ,self.lr_id:1 ,self.top_id:0,self.bot_id:0 }
            
        self.dyMultD = {self.widgetID:1, self.ul_id:1 ,self.l_id:0, self.ll_id:1 ,self.ur_id:1 ,
            self.r_id:0 ,self.lr_id:1 ,self.top_id:1,self.bot_id:1 }

        #print self.cursorD
        #self.canvas.bind( '<ButtonPress-1>',   self.returnConrolToFormWindow )

        
if __name__ == "__main__":
    
    root = Tk()
    canvas = Canvas(root, width=400, height=400)

    canvas.pack(fill=X, expand=YES)

    b = Button(canvas, text='OK by Me') #, width=13, height=2)
    #b.place(x=50,y=50)
    canvas.create_window( 50,50, window=b, tags=b, anchor='nw')
    #canvas.itemconfigure( b, width=44 )

    #print root.tk.splitlist(root.tk.call("font", "families"))
    print b.cget('font') #.metrics()


    #s = GrabHandles( canvas, b)

    mainloop()
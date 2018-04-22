#!/usr/bin/env python
from Tkinter import *
# see book examples in C:\Python23\Doc\TK_Examples

class EditWindow( Toplevel ):
        
    def cleanupOnQuit(self):
        if self.MainWin.allow_subWindows_to_close:
            # I'm not sure that transient windows need this, but I'm trying to be careful
            self.parent.focus_set()
            self.destroy()
        
        print '"No Kill I", Horta'
        self.MainWin.statusMessage.set('To Exit Applicaton, Use Main Window.')
    
    def __init__(self, MainWin):
        
        Toplevel.__init__(self, MainWin, bg='#90EE90')#'lightgreen': '#90EE90',
        self.title('Edit Window')
        
        x = MainWin.winfo_x() 
        if x<10: x=10
        y = MainWin.winfo_y() + MainWin.winfo_height()+ 30 + 10
        if y<370: y=370
        # position over to the upper right 
        self.geometry( '+%i+%i'%(x,y))
        
        Label(self,text='Edit Window',width=30,height=15, bg='#90EE90').pack(side=TOP, fill=X, expand=YES)
        
        self.MainWin = MainWin
        
        # only main window can close this window
        self.protocol('WM_DELETE_WINDOW', self.cleanupOnQuit)
    
    def clearAll(self):
        
        for k,i in self.children.items():
            i.destroy()
            


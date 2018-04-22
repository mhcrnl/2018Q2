#!/usr/bin/env python

from src_templates import legalPythonIdentifier
sampleMenuStr='''
File
    New
        Worksheet
        Text File
    Open
    Save
    
    Exit
Edit
    Find
    Copy
    Cut
    Paste
    '''

class myMenuItem( object ):
    
    def __init__(self, label):
        self.label = label
        self.subLabelL = []
        self.parent = None
    def addSubItem(self, subItem):
        self.subLabelL.append( subItem )
        subItem.parent = self
    def lenSubmenu(self):
        return len(self.subLabelL)
        
    def getSubItemAtLevel(self, N):
        m = self
        for i in range(N-1):
            if len(m.subLabelL)>0:
                m = m.subLabelL[-1]
        return m
        
    def printSum(self):
        
        sSubs = ''
        for sub in self.subLabelL:
            sSubs += sub.label + ' -- '
        
        print '------------ start -----------------'
        print '"%s"'%self.label, 'len list =',len(self.subLabelL),sSubs
        print '------------- end -----------------'
        for sub in self.subLabelL:
            sub.printSum()
        print '----'

def  numIndentSpaces( s ):
    return len(s) - len(s.lstrip())
    
def buildMenuSource( descStr ):
    
    # prune beginning and ending blank lines
    descL = descStr.split('\n')
    #print 'len(descL)=',len(descL)
    for i in range( len(descL)-1, -1, -1):
        if descL[i].strip() != '':
            break
        del descL[i]
    #print 'len(descL)=',len(descL)
    for i in range( len(descL)):
        if descL[i].strip() != '':
            break
        del descL[i]
    #print 'len(descL)=',len(descL)
    #print 'descL =',descL
    #print
    # now interpret the pruned list for indentation
    
    if len(descL)==0:
        return ''
    
    i = 0
    nspaceLast = numIndentSpaces( descL[0] )
    indentL = []
    for label in descL:
        nspace = numIndentSpaces( label )
        if nspace > nspaceLast:
            i += 1
        elif nspace < nspaceLast:
            i -= 1
        
        if i<0: i=0
        indentL.append( [i,label.strip()] )
        nspaceLast = nspace
        
    #print 'indentL',indentL
    #print
    
    # make list of menu Items
    menuL = []
    for N,label in indentL:
        m = myMenuItem(label)
        if N==0:
            menuL.append(m)
        else:
            try:
                mtop = menuL[-1]
                madd = mtop.getSubItemAtLevel(N)
                madd.addSubItem(m)
            except:
                menuL.append(m)
        
    #for mItem in menuL:
    #    mItem.printSum()
        
    return menuL

sMenuBar = '        self.menuBar = Menu(%s, relief = "raised", bd=2)\n'
sMenu    = '\n        top_%s = Menu(self.menuBar, tearoff=0)\n'
sItem    = '        top_%s.add("command", label = "%s", command = self.%s)\n'
sSpacer  = '        top_%s.add_separator()\n'
sCascade = '        self.menuBar.add("cascade", label="%s", menu=top_%s)\n'
sCascade2= '        top_%s.add("cascade", label="%s", menu=top_%s)\n'
sMenuConfig = '\n        %s.config(menu=self.menuBar)\n'
def getSubmenuSource( mItem ):
    topName = legalPythonIdentifier( mItem.label )
    sL = [sMenu%topName]
    for s in mItem.subLabelL:
        if s.lenSubmenu()==0:
            if s.label.strip() != '':
                name = 'menu_%s_%s'%(mItem.label, s.label)
                name = legalPythonIdentifier( name )
                sL.append(sItem%(topName, s.label, name))
            else:
                sL.append(sSpacer%topName)
        else:
            sL = sL + getSubmenuSource(s)
    
    if mItem.parent:
        topNameParent = legalPythonIdentifier( mItem.parent.label )
        sL.append(sCascade2%(topNameParent, mItem.label, topName))
    else:
        sL.append(sCascade%(mItem.label, topName))
    return sL
    

def getMenuSource( menuL, rootName='MainWin' ):
    srcList = [sMenuBar%rootName]
    
    for m in menuL:
        # most top level menu items will have subitems
        if m.lenSubmenu()>0:
            srcList = srcList + getSubmenuSource(m) 
        else:
            sTopItem= '        self.menuBar.add("command", label = "%s", command = self.%s)\n'
            name = 'menu_%s'%(legalPythonIdentifier( m.label ))
            srcList = srcList + [sTopItem%( m.label, name)]
    
    srcList.append(sMenuConfig%(rootName))
    return srcList


def getMenuFunctionSource( menuL, rootName='MainWin' ):
    pass

if __name__ == "__main__":
    
    descStr='''
File
    New
        Worksheet
        Text File
    Open
    Save
    
    Exit
Edit
    Find
    Copy
    Cut
    Paste
    '''
    
    menuL = buildMenuSource( descStr )
    
    menuSrcL = getMenuSource( menuL, rootName='master'  )
    print '======================================================'
    
    #fOut = file('test.py','w')
    print '''
from Tkinter import *

class Mytestapp:
    def __init__(self, %s):
'''%'master'
    for line in menuSrcL:
        print line,
        
    print '''root = Tk()
app = Mytestapp(root)
root.mainloop()
'''

    #fOut.close()
    
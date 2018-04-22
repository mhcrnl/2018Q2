#!/usr/bin/env python
import os
import cPickle as pickle
import CompDef
DEBUG_PRINT = 0

class FormDef( object ):
    def setSpecialOption(self, name, value):
        self.hiddenD[name] = value
        
    def getSpecialOption(self, name ):
        return self.hiddenD.get(name, '')
        
    def __init__(self, name='myApp', mydir='.'):
        
        #self.name = name
        self.curdir = os.path.abspath(mydir)
        self.fName = os.path.normpath( self.curdir +'/'+ name + '.def') # pickle of definition
        
        # form and widgets have non-tk options here (e.g. name, x, y)
        self.optionD = {'name':name,'x':350, 'y':20, 'width':300, 'height':300}
        self.hiddenD = {'maxCompID':0, 'guitype':'main',
            'hasmenu':'no', 'menu':'File\n  New\n  Open\n  Save',
            'hasstatusbar':'no','hasstddialmess':'no', 'hasstddialfile':'no', 
            'hasstddialcolor':'no', 'hasstdalarm':'no', 'resizable':'no'}
        self.tkOptionD = {} # form and widgets have Tk options here (e.g. width, background, etc.)
        self.compType = 'toplevel'
        self.helpD = frameOptD
        
        self.compTypeCountD = {}
        
        self.compObjL = [] # a list of component objects
        
        self.readFileOK = 1 # for New files, set flag to "OK"
        if os.path.isfile( self.fName ): # if file already exists, read it
            try:
                self.readPickleFile()
                self.readFileOK = 1
            except:
                print 'ERROR reading',self.fName
                self.readFileOK = 0
        #else:
        #    self.savePickleFile()
        if DEBUG_PRINT: print 'On Form Create, w,h=',self.optionD['width'],self.optionD['height']
        
    def nextComponentName(self, compType):
        if self.compTypeCountD.has_key(compType):
            return compType.capitalize() + '_%i'%(self.compTypeCountD[compType]+1)
        else:
            return compType.capitalize() + '_1'
            
    def getNextAvailableCompID(self):
        maxval = 0
        for comp in self.compObjL:
            if comp.optionD.has_key( 'compID'):
                if comp.optionD['compID'] > maxval:
                    maxval = comp.optionD['compID']
        nextVal = maxval + 1 
        if self.hiddenD.has_key('maxCompID'):
            nextVal = max( nextVal, self.hiddenD['maxCompID']+1 )
        self.hiddenD['maxCompID'] = nextVal
        return nextVal# return next biggest number
        
    def delComponentByName(self, name):
        '''MUST have "name" value in the option dictionary'''
        
        for c in self.compObjL:
            if c.name == name:
                self.compObjL.remove(c)
                print 'Deleted "%s" from form'
        
    def addComponent(self, compType, optionD, tkOptionD):
        '''MUST have "name" value in the option dictionary'''
        
        if self.compTypeCountD.has_key(compType):
            self.compTypeCountD[compType] += 1
        else:
            self.compTypeCountD[compType] = 1
        
        if compType in ['button','label','entry','checkbutton','message','radiobutton','listbox','text']:
            self.compObjL.append( CompDef.TextWidthComp( optionD['name'], compType, optionD, tkOptionD) )
            
        if compType in ['labelframe','canvas']:
            self.compObjL.append( CompDef.PixelWidthComp( optionD['name'], compType, optionD, tkOptionD) )
        
        # give each component a dummy component and a component ID number
        self.compObjL[-1].dummyWidget = None
        
        # if it doesn't already have one, give the component an ID number
        if not self.compObjL[-1].optionD.has_key('compID'):
            self.compObjL[-1].optionD['compID'] = self.getNextAvailableCompID()
            #print 'added compID to',self.compObjL[-1].optionD['name'],'of',self.compObjL[-1].optionD['compID']
            #print self.compObjL[-1].optionD
        else:
            pass
            #print 'already have compID for',self.compObjL[-1].optionD['name'],'of',self.compObjL[-1].optionD['compID']
            #print self.compObjL[-1].optionD
    
    def makeDictionaryNative(self, D):
        return
        # need any strings pickled in *.def file to have native line endings
        s = chr(0xD) + chr(0xA)
        for k,val in D.items():
            if type( D[k] ) == type('string'):
                # replace all line separator characters with 0xD, 
                # then replace all 0xD with os.linesep
                val = val.replace( s, chr(0xD) )
                val = val.replace(chr(0xA), chr(0xD))
                D[k] = val.replace(chr(0xD), '\n') 
                
    def readPickleFile(self):
        fIn = file(self.fName, 'r')
        self.optionD,self.tkOptionD,self.hiddenD = pickle.load( fIn )
        # need any strings pickled in *.def file to have native line endings
        self.makeDictionaryNative(self.optionD)
        self.makeDictionaryNative(self.tkOptionD)
        self.makeDictionaryNative(self.hiddenD)
        
        compL =  pickle.load( fIn )# compL is a list of tuples of format ( compType, optionD, tkOptionD )
        fIn.close()

        self.compObjL = [] # a list of component objects
        for compType, optionD, tkOptionD in compL:
            # need any strings pickled in *.def file to have native line endings
            self.makeDictionaryNative(optionD)
            self.makeDictionaryNative(tkOptionD)
            self.addComponent( compType, optionD, tkOptionD)
            

    def savePickleFile(self, newPath=''):
        
        if newPath:
            try:
                # make sure we have full path
                fullpath = os.path.abspath(newPath)
                fname = os.path.basename( fullpath )
                name = fname.split('.')[0]
                suffix = fname.split('.')[1]
                if suffix.lower() != 'def':
                    print 'ERROR... illegal file name',fname
                    return 0 # indicates an error
            
                #self.name = name
                self.curdir = os.path.dirname( fullpath )
                self.fName = os.path.normpath(self.curdir +'/'+ name + '.def') # pickle of definition
                if DEBUG_PRINT: print 'pickle save to',self.fName
                self.optionD['name'] = name
            except:
                print 'ERROR... saving file:',newPath
                return 0 # indicates an error
            
        
        # compL is a list of tuples of format ( compType, optionD, tkOptionD )
        compL = []
        for obj in self.compObjL:
            compL.append( [obj.compType, obj.optionD, obj.tkOptionD] )
            
        fOut = file(self.fName, 'w')
        pickle.dump( [self.optionD,self.tkOptionD,self.hiddenD], fOut, 0 ) # protocol 0 is ASCII
        pickle.dump( compL, fOut, 0 )
        fOut.close()
        return 1 # indicates a good save

#borderwidth# width of the border

frameOptD = {}
frameOptStr = '''background# The background color
highlightbackground# color when not focus
relief# Border decoration FLAT SUNKEN, RAISED, GROOVE RIDGE'''

#highlightcolor# color when focused
#highlightthickness# width of the highlight border
#takefocus# If true, accepts input focus
#height# height of the label. text units or pixels
#width# width of the label text units or pixels

strL = frameOptStr.split('\n')
for s in strL:
    sL = s.split('#')
    if len(sL)==2:
        frameOptD[sL[0].strip()] = sL[1].strip()


if __name__ == "__main__":
    
    fd = FormDef( 'myTestApp' )
    print 'curdir=',fd.curdir
    print 'fName=',fd.fName
    fd.tkOptionD['background']='yellow'
    
    if 1:
        N = (len( fd.compObjL )+2) * 20
        I = len( fd.compObjL ) + 1
        fd.addComponent('button', {'name':'TestBtn%i'%I, 'x':'%i'%N, 'y':'%i'%(N+10,)}, {'width':'15'})
        #fd.savePickleFile()
    
        fd.addComponent('label', {'name':'TestLabel%i'%I,  'x':'%i'%(N+20,), 'y':'%i'%(N+30,)}, 
            {'text':'Just for Fun', 'width':'15', 'background':'red'})
        fd.savePickleFile()        
    else:
        for obj in fd.compObjL:
            print 'for "%s" object "%s"'%(obj.compType, obj.name)
            for key,val in obj.optionD.items():
                print key,val
            for key,val in obj.tkOptionD.items():
                print key,val
            print
        
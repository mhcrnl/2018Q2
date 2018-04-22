#! /usr/bin/env python
#
# Support module generated by PAGE version 4.2g
# In conjunction with Tcl version 8.6
#    Feb. 02, 2014 03:19:38 PM


import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

def set_Tk_var():
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global instance
    instance = StringVar()


colors = ['white', 'gold', 'cyan', 'salmon', 'wheat', 'pale green',
          'dodger blue', 'pink', 'burlywood1',]
cc = -1

def create_called(rt):
    import called
    cl = len(colors)
    global cc
    cc += 1
    if cc == cl - 1:
        cc = 0
    color = colors[cc]
    g = "+100+%s" % str(65 + (cc * 100))
    p_dict = {'geom': g, 'instance': 2, 'color' : color}
    firebrick = called.create_Called(rt,param=p_dict)

count = 0
def init(top, gui, arg=None):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    global count
    count += 1
    string = "Instance = %s" % str(count)
    gui.instance.set(string)
    if arg != None:
        top_level.geometry(arg['geom'])
        print 'init: arg[\'geom\'] =', arg['geom']    # rozen   pyp
        top_level.configure(background = arg['color'])
        root.update()



def destroy_window ():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None



#!/usr/bin/env python
from Tkinter import *
import tk_happy

root = Tk()
MainWin = root
MainWin.title('Main Window')

happy = tk_happy.main_window.TK_Happy( MainWin )
# must start mainloop for the following auto load to work properly
MainWin.mainloop()

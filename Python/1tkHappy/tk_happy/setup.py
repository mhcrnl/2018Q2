#!/usr/bin/env python
# setup.py 
from distutils.core import setup 


setup(name="tk_happy",
      version='0.3',
      description = 'Rapid Application Development for Tkinter',
      author="Charlie Taylor",
      author_email="charlietaylor@users.sourceforge.net",
      url='http://tk-happy.sourceforge.net/overview.html',
      package_dir = { "tk_happy":""},
      packages=['tk_happy'],
      license='BSD',
      long_description='''The main idea behind tk_happy is to allow a fully "wired"
            python Tkinter GUI application to be created in minutes.  
            The users main responsibility is to add logic to the Tkinter framework
            created by tk_happy.''',
      classifiers = [
          'Development Status :: Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: BSD',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: GUI',
          ],

     )

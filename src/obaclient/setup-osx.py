from setuptools import setup
import py2app
from os import path
from glob import glob

import shutil
shutil.rmtree('../../dist-osx', True)

# data_files = [("media", ['../../data/media/obaclient.icns']),
#              ("", ['config.cfg'])]

files = ["..\..\data\media"]

from plistlib import Plist
plist = Plist.fromFile('Info.plist')
plist.update(dict(
    LSPrefersPPC=True,
))

setup(
      
	setup_requires=["py2app"],
	app = 	["main.py"],
	
	data_files = ['../../data/media'],
	options =	dict(py2app=dict(
					plist=plist,
					bdist_base="build-osx",
					dist_dir="../../dist-osx",
					# iconfile="../../data/media/obaclient.ico"
				))
)

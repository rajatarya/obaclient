from distutils.core import setup
import py2exe
from os import path
from os import os
from glob import glob

import shutil
shutil.rmtree('../../dist', True)

mfcdir = 'C:\Python27\Lib\site-packages\pythonwin'
mfcfiles = [path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", "Microsoft.VC90.MFC.manifest"]]

data_files = [("Microsoft.VC90.MFC", mfcfiles),
              ("media", ['..\..\data\media\obaclient.ico']),
              ("", ['config.cfg'])]

setup(
      
    version = "0.1.0",
    description = "One Bus Away Desktop Client",
    name = "obaclient",

    data_files = data_files,
    
    # targets to build
    windows = [{
                "script" : "main.py",
                "icon_resources" : [(1, "../../data/media/obaclient.ico")]
                }],

    console = [{
                "script" : "main.py",
                "icon_resources" : [(1, "../../data/media/obaclient.ico")]
                }],

    options={
              "py2exe":{
                          "dist_dir" : "../../dist",
                          "bundle_files":"3"
              }
      },
    
    zipfile = None,

)

os.rename('../../dist/main.exe','../../dist/OBAClient.exe') 
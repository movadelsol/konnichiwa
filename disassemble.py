#coding:utf-8
from __future__ import with_statement
from statistics import mean, median, variance,stdev

import matplotlib.pyplot as plt
import numpy as np
import tkinter.filedialog as tkfd
import codecs
import sys
from PIL import Image
import csv
import os
import cv2

def cut_files(fullfilename, output, sizex, sizey, frameno):
    location=['TOP','R','G','B','LOW','COAX','DEPTH']
    output = output+"\\"+location[frameno]+".png"
    if (frameno==6):
        data  = np.fromfile(fullfilename, dtype=np.uint16)
        frame = data[3*sizex*sizey:]
        frame = frame.reshape(sizey,sizex)
    else:
        data  = np.fromfile(fullfilename, dtype=np.uint8)
        frame = data[frameno*sizex*sizey:(frameno+1)*sizex*sizey]
        frame = frame.reshape(sizey,sizex)
#    print(frame.shape)
    cv2.imwrite(output, frame) 

def do_the_dishes(targetpath):
    # with all raw file
    os.chdir(targetpath)
    for entry in os.scandir('.'):
    # read one raw name : target
        if (entry.name.endswith('.raw')):
            newfoldername=entry.name.rstrip('.raw')
            print( "NFN {0} => {1}".format(entry.name,newfoldername) )
            # make a folder with the target
            try:
                os.mkdir(targetpath+"\\"+newfoldername)
            except FileExistsError:
                print('mkdir was skipped')

            # cut_file    
            for i in range(7):
                cut_files(entry.name,newfoldername,2048,2048,i)
    
def trythis(targetpath):
	os.chdir(targetpath)
	print(os.getcwd())
	
if __name__ == '__main__':
#   Disassemble any imagefile under the folder C:\BF2Data\SAKICORP\SAKI_DEMOBOARD2\Resources.
	targetpath = "C:\\BF2Data\\SAKICORP\\SAKI_DEMOBOARD2\\Resources"
	originalpath=os.getcwd()
	print(os.getcwd())
	trythis(targetpath)
#    do_the_dishes(targetpath)
	os.chdir(originalpath)
	print(os.getcwd())
	exit()

  # THIS IS THE END OF PROGRAM
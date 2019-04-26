# -*- coding: utf-8 -*
# $Id:$
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
import os
import subprocess
from skimage import io, draw
from matplotlib import pyplot as plt
from os import listdir
from os.path import isdir, isfile, join

base = 'D:/work/tool/python/openCvPython/models/research/object_detection/protos/'

if __name__ == '__main__':
	mypath = base
	idlist = []
	folders = [f for f in listdir(mypath) if isfile(join(mypath,f))]
	for path in folders:
		print("B[{}],I[{}]".format(path,""))
		sts = subprocess.call("protoc "+path+" --python_out=.",shell=True)
		print("done:",sts)
	print("Function Complete")

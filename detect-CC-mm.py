# -*- coding: utf-8 -*-
# $Id: detect-mm.py 10383 2019-03-19 03:02:42Z osawa $
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
import os
from skimage import io, draw
from matplotlib import pyplot as plt
import time

# Choose Feature Type from {HAAR,LBP,HOG}
FEATURE="HAAR"
base = 'D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/'
datestr=time.strftime(format("%d%b%Y%p%I"))
#
def task4Fov(basedir,branch,id):
	filein = base+branch+'/Resources/'+id+'/R.png'
#	print("Filein:{}".format(filein))
	img = cv2.imread(filein)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# EDIT THE LEAF FOLDER
	cascade = cv2.CascadeClassifier('D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/cascade/fourth/cascade.xml')
	scaleFactor=1.1
	minNeighbours=5
	flags=cv2.CASCADE_SCALE_IMAGE
	minSize=(92,92)
	maxSize=(200,200)
	#
	faces = cascade.detectMultiScale(gray,scaleFactor,minNeighbours,flags,minSize,maxSize)
	n=0
	outbase=basedir+'/'+id

        # make a folder with the target
	try:
	    os.mkdir(outbase)
	except FileExistsError:
	    print('mkdir {} was skipped'.format(outbase))

	for (x,y,w,h) in faces:
	    cropped = img[y:y+h,x:x+w]
	    outname = outbase+ '/' + str(n) + '.png'
	    io.imsave(outname,cropped)
	    n += 1

	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	io.imsave(outbase+'/figure-1.png',img)


from os import listdir
from os.path import isdir, isfile, join

if __name__ == '__main__':
	branches =['0227OK.bdimg','0227Bridge_No.3.bdimg','0228PinLower_No.8.bdimg']
#
# for python3
# scan single layer
	for branch in branches:
		outbase= base+branch+'/'+FEATURE+'-'+datestr
		mypath = base+branch+'/Resources'
		            # make a folder with the target
		try:
		    os.mkdir(outbase)
		except FileExistsError:
		    print('mkdir {} was skipped'.format(outbase))
		
		folders = [f for f in listdir(mypath) if isdir(join(mypath,f))]
		for path in folders:
			print("B[{}],I[{}]".format(branch,path))
			task4Fov(outbase,branch,path)
#		for path in os.scandir(base+branch+'/Resources'):
#			if os.path.isdir(path):
#				task4Fov(outbase,branch,path.name)

	print("Function Complete")
#


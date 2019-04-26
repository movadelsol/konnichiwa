# -*- coding: utf-8 -*-
# $Id:$
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
import os
from skimage import io, draw
from matplotlib import pyplot as plt
import time

base = 'D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227Copper_No.2.bdimg/'
datestr=time.strftime(format("%d%B%Y"))
ext = 'Resources/'

def task4Fov(id):
	filein = base+ext+id+'/B.png'
	print("Filein:{}".format(filein))
	img = cv2.imread(filein)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#カスケードファイルの読み込み
	cascade = cv2.CascadeClassifier('D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/cascade/fourth/cascade.xml')
	scaleFactor=1.1
	minNeighbours=5
	flags=cv2.CASCADE_SCALE_IMAGE
	minSize=(92,92)
	maxSize=(200,200)
	#
	faces = cascade.detectMultiScale(gray,scaleFactor,minNeighbours,flags,minSize,maxSize)
	n=0
	outbase=base+datestr+id
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
#	io.imshow(img)
#	plt.show()


if __name__ == '__main__':

	outbase=base+datestr
	            # make a folder with the target
	try:
	    os.mkdir(outbase)
	except FileExistsError:
	    print('mkdir {} was skipped'.format(outbase))
	
	idlist = []
# scan one layer
	for path in os.scandir(base+'Resources'):
		if path.is_dir():
			idlist.append(path.name)
# scan multi layer
#	for dirpath,dirnames,filenames in os.walk(base+'Resources'):
#		for dirname in dirnames:
#			idlist.append(dirname)

	for id in idlist:
		print(id)
#		task4Fov(id)

	print("Function Complete")

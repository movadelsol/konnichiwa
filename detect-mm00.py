# -*- coding: utf-8 -*-
# $Id: detect-mm.py 10317 2019-03-14 01:14:40Z osawa $
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
import os
from skimage import io, draw
from matplotlib import pyplot as plt
import time

base = 'D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/'
datestr=time.strftime(format("%d%B%Y"))
#
def task4Fov(branch,id):
	filein = base+branch+'/Resources/'+id+'/B.png'
#	print("Filein:{}".format(filein))
	img = cv2.imread(filein)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# reading cascade file
	cascade = cv2.CascadeClassifier('D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/cascade/fourth/cascade.xml')
	scaleFactor=1.1
	minNeighbours=5
	flags=cv2.CASCADE_SCALE_IMAGE
	minSize=(92,92)
	maxSize=(200,200)
	#
	faces = cascade.detectMultiScale(gray,scaleFactor,minNeighbours,flags,minSize,maxSize)
	n=0
	outbase=base+branch+'/'+datestr+'/'+id
#	print("Outbase:{}".format(outbase))

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


if __name__ == '__main__':
	branches =['0227OK.bdimg','0227Bridge_No.3.bdimg','0228PinLower_No.8.bdimg']
#	branches =['0228Nosolder_No.4.bdimg','0228ExSolderetc_No.5.bdimg',]
#
	for branch in branches:
		outbase=base+branch+'/'+datestr
		            # make a folder with the target
		try:
		    os.mkdir(outbase)
		except FileExistsError:
		    print('mkdir {} was skipped'.format(outbase))
		
		idlist = []

		for path in os.scandir(base+branch+'/Resources'):
			if os.path.isdir(path):
				pathstr = str(path).split("'")
				idlist.append(pathstr[1])

		for id in idlist:
			print("B[{}],I[{}]".format(branch,id))
			task4Fov(branch,id)

	print("Function Complete")

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
	filein = base+branch+'/Resources/'+id
	img = cv2.imread(filein+'/R.png')
	img_r = cv2.split(img)[0]
	img = cv2.imread(filein+'/G.png')
	img_g = cv2.split(img)[0]
	img = cv2.imread(filein+'/B.png')
	img_b = cv2.split(img)[0]
	print("R info:{}".format(img_r.shape))
	print("G info:{}".format(img_g.shape))
	print("B info:{}".format(img_b.shape))

	img = cv2.merge((img_r,img_g,img_b))
	fileout = base+branch+'/Resources/'+id+'/RGB.png'
	io.imsave(fileout,img)


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

	print("Function Complete")
# END


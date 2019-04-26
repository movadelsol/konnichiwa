# -*- coding: utf-8 -*-
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
import os
from skimage import io, draw
from matplotlib import pyplot as plt

base = 'D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/'
ext = 'Resources/OwlPhysicalImageResource_uid7C6EDD0__'
id = 'esdnddjf'

def task4Fov(id):
	filein = base+ext+id+'/B.png'
	img = cv2.imread(filein)
	#img = cv2.imread('D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/Resources/OwlPhysicalImageResource_uid7C6EDD0__bcdlpbg/B.png')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#カスケードファイルの読み込み
	cascade = cv2.CascadeClassifier('D:/work/DIP-DATA-20190227/sumitomo_denso_DIP/Dip_Jigu/breakdown/0227OK.bdimg/cascade/first/cascade.xml')
	scaleFactor=1.1
	minNeighbours=5
	flags=cv2.CASCADE_SCALE_IMAGE
	minSize=(92,92)
	maxSize=(200,200)
	#
	faces = cascade.detectMultiScale(gray,scaleFactor,minNeighbours,flags,minSize,maxSize)
	n=0
	outbase =base+'result-7MAR2019/'+id
	            # make a folder with the target
	try:
	    os.mkdir(outbase)
	except FileExistsError:
	    print('mkdir was skipped')

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
	os.scandir(base+'Resources')
	idlist = []
	for path in os.scandir(base+'Resources'):
		if os.path.isdir(path):
			pathstr = str(path)
#			print(path)	
			locUs = pathstr.find('__')
#			print("Location:{}:{}".format(locUs, pathstr[locUs+2:]))
			idlist.append(pathstr[locUs+2:-2])
	for id in idlist:
		task4Fov(id)
#		print("id:{}".format(id))
#	ids = ['myxvqwul','nayomawj']
#	for id in ids:
#		task4Fov(id)
	print("Function Complete")

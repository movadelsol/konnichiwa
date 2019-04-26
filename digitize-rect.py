# -*- coding: utf-8 -*-
# digitize-rect.py
import os
import cv2
import numpy as np
import csv
import apTrace as trace
# double click invokes drawing a blue circle
# Global Variables
img = cv2.imread('MzAzODk3NA.jpeg')
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
drag_start = None
sel = (0,0,0,0)
tr = trace.myTrace("apTrace",12)
#
def main():
#	global tr
	rectangles=[]
	ESC=27
	while(1):
		k = cv2.waitKey(1) & 0xFF
		if k == ord('m'):
			None
		elif k == ord('a'):
			rectangles.append(sel)
			tr.apTrace(10,"appending:%d,%d,%d,%d",sel[0],sel[1],sel[2],sel[3])
		elif k == ord('s'):
			with open("writer.csv","w",newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
				for rect in rectangles:
					tr.apTrace(10,"listing:%s",rect)
					writer.writerow(rect)
		elif k == ord('r'):
			img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
			for rect in rectangles:
				cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0,255,0), 1)
				cv2.imshow("gray", img)
		elif k == ord('c'):
			img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
			cv2.imshow("gray", img)
		elif k == ord('q'):   # Discard the list
			rectangles.clear()  
		elif k == ESC:
#			fh.close()
			break

# mouse callback function
def on_mouse(event, x, y, flags, param):
    global drag_start, sel
    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = x, y
        sel = 0,0,0,0
    elif event == cv2.EVENT_LBUTTONUP:

#        cv2.imshow("result", result8)
        drag_start = None
    elif drag_start:
        #print flags
        if flags & cv2.EVENT_FLAG_LBUTTON:
            minpos = min(drag_start[0], x), min(drag_start[1], y)
            maxpos = max(drag_start[0], x), max(drag_start[1], y)
            sel = minpos[0], minpos[1], maxpos[0], maxpos[1]
            img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            cv2.rectangle(img, (sel[0], sel[1]), (sel[2], sel[3]), (0,255,255), 1)
            cv2.imshow("gray", img)
        else:
            print("selection is complete")
            drag_start = None
    else:
        None

if __name__ == '__main__':
	tr.apTrace(10,"CWD:%s",os.getcwd())
	cv2.namedWindow('gray',1)
	cv2.setMouseCallback('gray',on_mouse)
	gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow("gray",gray)
	main()
	cv2.destroyAllWindows()

# -*- coding: utf-8 -*-
"""
Created on Fri May 23 21:25:51 2014

@author: frederik
"""

import sys

sys.path = ['/opt/ros/hydro/lib/python2.7/dist-packages'] + sys.path

import cv2, cv

#cap = cv2.VideoCapture('video.avi')

box = []
def on_mouse(event, x, y, flags, params):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Mouse Position: ', x, ',' , y
        box.append( (x, y) )

#cv2.rectangle(img, pt1, pt2, color)
#cv2.line(img, pt1, pt2, color) 
drawing_box = False


cv2.namedWindow('real image')
cv.SetMouseCallback('real image', on_mouse, 0)
count = 0
while(1):
    #_,img = cap.read()
    img = cv2.imread('ludo.jpg')    
    #img = cv2.blur(img, (3,3))

    cv2.namedWindow('real image')
    cv2.imshow('real image', img)

    if cv2.waitKey(5) == 27:
        cv2.destroyAllWindows()
        break
print box
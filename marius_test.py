import sys
sys.path = ['/opt/ros/hydro/lib/python2.7/dist-packages'] + sys.path
import cv2, cv

box = []
def on_mouse(event, x, y, flags, params):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Mouse Position: ', x, ',' , y
        box.append( (x, y) )

pos_list = [[(227, 41), (187, 36), (184, 59), (188, 82), (186, 103), (188, 123), (206, 144), (229, 144), (249, 146), (270, 145), (292, 145), (310, 146), (312, 167), (312, 182), (291, 185), (272, 187), (249, 186), (228, 185), (206, 185), (187, 208), (189, 225), (187, 251), (186, 270), (186, 292), (185, 308), (168, 312), (145, 310), (147, 293), (146, 268), (146, 249), (144, 227), (144, 206), (128, 186), (104, 188), (81, 187), (62, 187), (38, 187), (22, 186), (21, 167), (20, 144), (41, 144), (60, 146), (83, 146), (101, 143), (129, 146), (145, 124), (147, 100), (145, 82), (145, 61), (144, 41), (145, 18), (167, 17), (167, 36), (165, 59), (166, 81), (166, 103), (165, 122), (167, 144)],
            [(288, 234), (187, 36), (184, 59), (188, 82), (186, 103), (188, 123), (206, 144), (229, 144), (249, 146), (270, 145), (292, 145), (310, 146), (312, 167), (312, 182), (291, 185), (272, 187), (249, 186), (228, 185), (206, 185), (187, 208), (189, 225), (187, 251), (186, 270), (186, 292), (185, 308), (168, 312), (145, 310), (147, 293), (146, 268), (146, 249), (144, 227), (144, 206), (128, 186), (104, 188), (81, 187), (62, 187), (38, 187), (22, 186), (21, 167), (20, 144), (41, 144), (60, 146), (83, 146), (101, 143), (129, 146), (145, 124), (147, 100), (145, 82), (145, 61), (144, 41), (145, 18), (167, 17), (293, 163), (268, 167), (246, 166), (229, 163), (208, 166), (185, 163)],
            [(97, 230), (187, 36), (184, 59), (188, 82), (186, 103), (188, 123), (206, 144), (229, 144), (249, 146), (270, 145), (292, 145), (310, 146), (312, 167), (312, 182), (291, 185), (272, 187), (249, 186), (228, 185), (206, 185), (187, 208), (189, 225), (187, 251), (186, 270), (186, 292), (185, 308), (168, 312), (145, 310), (147, 293), (146, 268), (146, 249), (144, 227), (144, 206), (128, 186), (104, 188), (81, 187), (62, 187), (38, 187), (22, 186), (21, 167), (20, 144), (41, 144), (60, 146), (83, 146), (101, 143), (129, 146), (145, 124), (147, 100), (145, 82), (145, 61), (144, 41), (145, 18), (167, 17), (166, 292), (165, 269), (166, 253), (166, 225), (169, 207), (167, 186)],
            [(50, 102), (187, 36), (184, 59), (188, 82), (186, 103), (188, 123), (206, 144), (229, 144), (249, 146), (270, 145), (292, 145), (310, 146), (312, 167), (312, 182), (291, 185), (272, 187), (249, 186), (228, 185), (206, 185), (187, 208), (189, 225), (187, 251), (186, 270), (186, 292), (185, 308), (168, 312), (145, 310), (147, 293), (146, 268), (146, 249), (144, 227), (144, 206), (128, 186), (104, 188), (81, 187), (62, 187), (38, 187), (22, 186), (21, 167), (20, 144), (41, 144), (60, 146), (83, 146), (101, 143), (129, 146), (145, 124), (147, 100), (145, 82), (145, 61), (144, 41), (145, 18), (167, 17), (38, 165), (62, 164), (82, 164), (104, 164), (124, 165), (145, 165)] ]


cv2.namedWindow('real image')
cv.SetMouseCallback('real image', on_mouse, 0)

tested_states = []

#

move_list = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 39, 0]], 6]
move_list = [[[0, 0, 49, 57], [40, 27, 48, 39], [2, 31, 0, 4], [4, 27, 11, 12]], 5]
move_list = [[[0, 0, 0, 1], [0, 0, 14, 0], [27, 0, 0, 0], [0, 0, 42, 0]], 4]
move_list = [[[0, 0, 0, 3], [0, 0, 20, 0], [0, 28, 0, 27], [0, 0, 0, 47]], 5]

all_moves = [[[[0, 0, 0, 3], [0, 0, 20, 0], [0, 28, 0, 27], [0, 0, 0, 47]], 5] , [[[0, 0, 0, 1], [0, 0, 14, 0], [27, 0, 0, 0], [0, 0, 42, 0]], 4], [[[0, 0, 49, 57], [40, 27, 48, 39], [2, 31, 0, 4], [4, 27, 11, 12]], 5] ]

import pickle
with open('state_liste.dat', 'rb') as f:
    all_moves = pickle.load(f)

for move_list in all_moves[200:]:
    
    img = cv2.imread('ludo.jpg')   
    
    color = [(0,255,0),(0,255,255),(0,0,255),(255,0,0) ]
    
    cv2.putText(img,str(move_list[1]), (300,30), cv2.FONT_HERSHEY_PLAIN,3, (0,0,0), 4 )
    
    for index, move in enumerate(move_list[0]):
        print move        
        for num, player in enumerate(move):  
            cv2.circle(img, ( pos_list[index][player][0] + ( num - 2 )*3 , pos_list[index][player][1]), 3, color[index], 3)
            cv2.circle(img, ( pos_list[index][player][0] + ( num - 2 )*3 , pos_list[index][player][1]), 5, (0,0,0), 1)
            if index == 0:             
                cv2.putText(img,str(num + 1), ( pos_list[index][player][0] + ( num - 2 )*3 , pos_list[index][player][1]), cv2.FONT_HERSHEY_PLAIN,2, (0,0,0), 3 )
                cv2.putText(img,str(num + 1), ( pos_list[index][player][0] + ( num - 2 )*3 , pos_list[index][player][1]), cv2.FONT_HERSHEY_PLAIN,2, (255,255,255), 2 )
    
    
    cv2.imshow('real image', cv2.pyrUp(img))
    
    k = cv2.waitKey(0)
    
    print k
    
    output = [0,0,0,0]
    if k == 49:   
        output[0] = 1
    if k == 50: 
        output[1] = 1    
    if k == 51: 
        output[2] = 1    
    if k == 52: 
        output[3] = 1
    if k == 27:
        break
    
    tested_states.append( [ move_list , output ] )

print tested_states 

with open('marius_liste4.dat', 'wb') as f:
    pickle.dump( tested_states , f)

print len(pos_list)
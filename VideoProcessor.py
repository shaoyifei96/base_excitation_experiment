import matplotlib
matplotlib.use('Agg')
import os
import cv2
from cv2 import aruco
import numpy as np
from cv2 import Rodrigues 
from math import sqrt
import matplotlib.pyplot as plt
import glob
from scipy.signal import argrelextrema

# Setup Aruco Dictionary
aruco_dict = aruco.Dictionary_get( aruco.DICT_6X6_1000 )
arucoParams = aruco.DetectorParameters_create()

# These 4 lines are used to create a picture for each of the markers 
# that are used in the code (not needed if they already exist)
# marker1 = aruco.drawMarker(aruco_dict,23,200,1)
# marker2 = aruco.drawMarker(aruco_dict,24,200,1)
# cv2.imwrite('marker1.jpg',marker1) 
# cv2.imwrite('marker2.jpg',marker2)

# Retrieve camera calibration parameters
dist = np.loadtxt('distance_coef_calibration.txt')
mtx = np.loadtxt('matrix_calibration.txt')

# Ask user for file location of input video and which output(s) are needed
# fname = input("Input file name (with file type ie; input.mp4): ")
# cap = cv2.VideoCapture(str(fname))
# motorfreq = input("What was the frequency of the motor in this trial? ")
# outputimageq = input("Would you like this program to output each frame of the video as a picture? (Y/N) ")
# picout = False
# if(str(outputimageq) == 'y' or str(outputimageq) == 'Y' or str(outputimageq) == 'yes' or str(outputimageq) == 'Yes' or str(outputimageq) == 'YES'):
	# picout = True

# vidout = False
# outputvidq = input("Would you like this program to output a video? (Y/N) ")
# if(str(outputvidq) == 'y' or str(outputvidq) == 'Y' or str(outputvidq) == 'yes' or str(outputvidq) == 'Yes' or str(outputvidq) == 'YES'):
	# h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	# w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	# out = cv2.VideoWriter('output/video/output'+motorfreq+'.avi',cv2.VideoWriter_fourcc(*'MJPG'),30.0,(int(w),int(h)))
vidout = True
sidel = 5.08
# grphout = False
# outputgrphq = input("Would you like this program to output a graph of position? (Y/N) ")
# if(str(outputgrphq) == 'y' or str(outputgrphq) == 'Y' or str(outputgrphq) == 'yes' or str(outputgrphq) == 'Yes' or str(outputgrphq) == 'YES'):
grphout = True
maxima = []
err = []
r = []
vid = glob.glob('input/*.mp4')
maxy = 2.5
for filename in vid:
	cap = cv2.VideoCapture(filename)
	tempname = filename.split('/')
	tempname1 = str(tempname[1])
	tempname2 = tempname1.split('.')
	fname = str(tempname2[0])
	h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	out = cv2.VideoWriter('output/video/'+fname+'.avi',cv2.VideoWriter_fourcc(*'MJPG'),30.0,(int(w),int(h)))
	
	#Preparations for the video loop
	j = 0
	finaldistx = []
	finaldisty = []
	finaldistz = []
	totdistance = []
	time = []
	firstpass = True
	offset = [0,0,0]
	font = cv2.FONT_HERSHEY_SIMPLEX
	while(cap.isOpened()):
		j = 1 + j
		ret, img = cap.read()
		if(ret ==True):
			corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=arucoParams)
			img2 = aruco.drawDetectedMarkers(img, corners, ids)
			h,w,cha = img2.shape
			rvecs, tvecs, objpoints = aruco.estimatePoseSingleMarkers(corners,sidel,mtx,dist)
			try:
				if(ids[0] == 23):
					index23 = 0
					index24 = 1
				elif(ids[0] == 24):
					index23 = 1
					index24 = 0
				aruco.drawAxis(img2,mtx,dist,rvecs[index23,0],tvecs[index23,0],sidel/2)
				aruco.drawAxis(img2,mtx,dist,rvecs[index24,0],tvecs[index24,0],sidel/2)
				Rmat23,jacob23 = Rodrigues(rvecs[index23,0])
				Rmat24,jacob24 = Rodrigues(rvecs[index24,0])
				R23inv = np.linalg.inv(Rmat23)
				R24inv = np.linalg.inv(Rmat24)
				co24to23 = np.matmul(R23inv,tvecs[index24,0]-tvecs[index23,0])
				distance = co24to23
				# P23 = np.matmul(Rmat23,rvecs[index23,0])+tvecs[index23,0]
				# P24 = np.matmul(Rmat24,rvecs[index24,0])+tvecs[index24,0]
				# distance = np.matmul(R23inv,(P24 - tvecs[index23,0]))
				# Transmat23 = np.zeros((4,4))
				# Transmat24 = Transmat23
				# Transmat23[:3,:3]= Rmat23
				# Transmat24[:3,:3]= Rmat24
				# Transmat23[:4,3] = [0, 0, 0, 1]
				# Transmat24[:4,3] = [0, 0, 0, 1]
				# Transmat23[:3,3] =  np.transpose(tvecs[index23,0])
				# Transmat24[:3,3] =  np.transpose(tvecs[index24,0])
				if(firstpass == True):
					offset = distance
					firstpass = False
				distance = distance -offset
				tempdist = sqrt(distance[0]*distance[0] +distance[1]*distance[1]+distance[2]*distance[2])
				totdistance.append(distance[1])
				finaldistx.append(distance[0])
				finaldisty.append(distance[1])
				finaldistz.append(distance[2])
				time.append((j-1)/30)
				cv2.putText(img2, 'X,Y,Z = ' + str(distance), (0, h-50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
				# if(picout == True):
					# cv2.imwrite('output/frames/'+'frame'+str(j)+motorfreq+'.jpg',img2)
				if(vidout == True):
					out.write(img2)
			except:
				if(vidout == True):
					cv2.putText(img2, 'X,Y,Z = [? ? ?]', (0, h-50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
					out.write(img2)
		else:
			break
	if(vidout == True):
		out.release()
	totdist = np.asarray(totdistance)
	cap.release()
	sort = np.sort(totdist)
	min = sort[:10]
	sort = sort[::-1]
	max = sort[:10]
	minavg = min.mean()
	maxavg = max.mean()
	totavg = (minavg + maxavg)/2
	sdom = max.std()
	err.append(sdom)
	maxima.append((maxavg - totavg)/maxy)
	omega = int(fname.split('_')[1])
	r.append(omega)
	print("Finished " + str(omega))
	# Plot the results
	if(grphout ==True):
		fig,(ax) = plt.subplots(1,1)
		ax.plot(time,totdistance)
		fig.savefig('output/graph/graphdist'+fname+'.png')

disp, axdisp = plt.subplots(1,1)
axdisp.errorbar(r,maxima,yerr=err,fmt = 'o', ecolor = 'red')
disp.savefig('output/disptrans41.png')
print(r)
print('\n')
print(maxima)
print('\n')
print(err)
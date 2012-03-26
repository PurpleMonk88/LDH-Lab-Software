from __future__ import division
import cv, numpy
import time, math

def CapCam(CamNum,capture):
    frame = cv.QueryFrame(capture)
    small = cv.CreateImage((frameW,frameH),frame.depth,frame.nChannels)
    cv.Resize(frame,small)
    cv.ShowImage("camera"+str(CamNum), small)
    imagesL.append(small)
    #cv.WriteFrame(writer,small)

cv.NamedWindow("camera1", 1)
capture = cv.CaptureFromCAM(0)
time0 = time.time()
frameW  = 640 # images width
frameH  = 480 # images height
filename = "test1"
imagesL = list()

while True:
    
    CapCam(1,capture)
    time1 = time.time()
    print time1-time0
    if cv.WaitKey(10) == 27:
        cv.DestroyWindow("camera1")
		
        break

fps = numpy.round(len(imagesL)/(time1-time0))
print fps
isColor = 1
#fps     = 20# or 30, frames per second
writer 	= cv.CreateVideoWriter(filename+"_Cam1.avi",cv.CV_FOURCC('D', 'I', 'V', 'X') , fps,(frameW,frameH),isColor)

for k in imagesL:
    cv.WriteFrame(writer,k)
    

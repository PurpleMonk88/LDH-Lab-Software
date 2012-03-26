from __future__ import division
import cv, numpy
import time

def CapCam(CamNum,writer,capture):
    frame = cv.QueryFrame(capture)
    cv.PutText(frame,"FPS = "+str(numpy.round(fps)),(10,15),f1,-1)
    cv.PutText(frame,"Camera"+str(CamNum),(10,30),f1,-1)
    small = cv.CreateImage((frameW,frameH),frame.depth,frame.nChannels)
    cv.Resize(frame,small)
    cv.ShowImage("camera"+str(CamNum), small)
    cv.WriteFrame(writer,small)

cv.NamedWindow("camera1", 1)
cv.NamedWindow("camera2", 1)
capture1 = cv.CaptureFromCAM(0)
capture2 = cv.CaptureFromCAM(1)
capture3 = cv.CaptureFromCAM(2)
capture4 = cv.CaptureFromCAM(3)

isColor = 1
fps     = 10 # or 30, frames per second
frameW  = 480 # images width
frameH  = 360 # images height
filename = "test1"
writer1 	= cv.CreateVideoWriter(filename+"_Cam1.avi",cv.CV_FOURCC('D', 'I', 'V', 'X') , fps,(frameW,frameH),isColor)
writer2 	= cv.CreateVideoWriter(filename+"_Cam2.avi",cv.CV_FOURCC('D', 'I', 'V', 'X'), fps,(frameW,frameH),isColor)
writer3 	= cv.CreateVideoWriter(filename+"_Cam3.avi",cv.CV_FOURCC('D', 'I', 'V', 'X'), fps,(frameW,frameH),isColor)
writer4 	= cv.CreateVideoWriter(filename+"_Cam4.avi",cv.CV_FOURCC('D', 'I', 'V', 'X'), fps,(frameW,frameH),isColor)

time1 = 1

f1 = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,0.5,0.5,0,1,1)
CamNum = 1
while True:
    time2 = time1
    time1 = time.time()
    timedif = time1-time2
    fps = 1/timedif
    #if fps >= 5:
    #    delay =0.2-timedif
    #    fps = 5
    #    time.sleep(delay)
    
    CapCam(1,writer1,capture1)
    CapCam(2,writer2,capture2)
    CapCam(3,writer3,capture3)
    CapCam(4,writer4,capture4)

    if cv.WaitKey(10) == 27:
        cv.DestroyWindow("camera1")
        cv.DestroyWindow("camera2")
        cv.DestroyWindow("camera3")
        cv.DestroyWindow("camera4")
        break


    

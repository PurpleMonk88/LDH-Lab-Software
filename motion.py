from __future__ import division
import cv, numpy, time, math, csv, cProfile
from os.path import exists

#Setting up Parameters

isColor     = 1
filename    ="Test_20120309"
maxCorners  = 2500


#Create windows, Captures and writer

capture1 		= cv.CaptureFromFile(filename+".avi")
frame_Current 	= cv.QueryFrame(capture1)
frame_Cnt 		= cv.GetCaptureProperty(capture1,cv.CV_CAP_PROP_FRAME_COUNT)
fps 			= cv.GetCaptureProperty(capture1,cv.CV_CAP_PROP_FPS)
frameW      	= cv.GetSize(frame_Current)[0] # images width
frameH      	= cv.GetSize(frame_Current)[1] #images height
Dif_Comb        = cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
frame_PastBW 	= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
frame_CurrentBW = cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
Dif_Back 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
Dif_Back2 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
Dif_Frame 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
imgc	 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,3)
eig_image 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_32F,1)
temp_image 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_32F,1)
currPyr 		= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_32F,1)
backtot         = cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_8U,1)
velX 			= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_32F,1)
velY 			= cv.CreateImage(cv.GetSize(frame_Current),cv.IPL_DEPTH_32F,1)
OnTop           = cv.CreateImage((frameW,frameH*2),cv.IPL_DEPTH_8U,3)
imagesL 		= list()
Pwid 			= cv.GetSize(frame_Current)[0]+8
Phei 			= numpy.round((cv.GetSize(frame_Current)[1])/3)
prevPyr 		= cv.CreateImage((Pwid,Phei),cv.IPL_DEPTH_32F,1)
count 			= -1
writer 			= cv.CreateVideoWriter(filename+"_flow.avi",-1, fps,(frameW,frameH*2),isColor)
time0 = time.time()

#Open Image and CSV files and put them into Arrays
CSVname = filename
if exists(CSVname+'.csv')==0:
    FileCSV = csv.writer(open(CSVname+'.csv','ab'))
    FileCSV.writerow(['Time', 'RGB','Angle','length','x','y'])
else: FileCSV = csv.writer(open(CSVname+'.csv','ab'))



#Start reading webcam feed

for a in range( int(frame_Cnt)-1):

   
    time1 = time.time()
    timei = time1-time0
    
    #Set Past Frame To Black and White and smooth
	
    print('Frame: '+str(a+1)+' of '+str(int(frame_Cnt)))
    count  			= count+1
    frame_Past		= frame_Current
    cv.CvtColor(frame_Past,frame_PastBW, cv.CV_BGR2GRAY)
    cv.Smooth(frame_PastBW,frame_PastBW,cv.CV_MEDIAN)
    
	
    #Set Current Frame to Black and White and smooth
	
    frame_Current 	= cv.QueryFrame(capture1)
    cv.CvtColor(frame_Current,frame_CurrentBW, cv.CV_BGR2GRAY)
    cv.Smooth(frame_CurrentBW,frame_CurrentBW,cv.CV_MEDIAN)

	
    #Find the Background
	
    bufim 		= frame_CurrentBW
    if count <30 and count>1:
        cv.ConvertScale(bufim,bufim,0.5)
        cv.ConvertScale(backtot,backtot,0.5)
        cv.Add(bufim,backtot,backtot)
    

		
    #Check the Differences between current frame and background/previous frame 

    cv.AbsDiff(frame_CurrentBW,backtot,Dif_Back)
    cv.AbsDiff(frame_CurrentBW,frame_PastBW,Dif_Frame)

	
    #Set threshold so its Binary, either 0 or 255
	
    cv.Threshold(Dif_Back,Dif_Back,30,255,cv.CV_THRESH_BINARY)
    cv.Threshold(Dif_Frame,Dif_Frame,5,255,cv.CV_THRESH_BINARY)
    if count >29 :
        cv.Add(Dif_Comb,Dif_Back,Dif_Comb,None)
    
    
	
    #Find the good points to track
	
    features = cv.GoodFeaturesToTrack(Dif_Frame,eig_image,temp_image,
                                      maxCorners,0.01,10,None,3,0,0.04)

    
    #Calculate the flow of points
	
    Mov, stat, trackerr = cv.CalcOpticalFlowPyrLK(frame_PastBW,frame_CurrentBW,prevPyr,currPyr,
                            features,(5,5),5,
                            (cv.CV_TERMCRIT_ITER|cv.CV_TERMCRIT_EPS, 20, 0.03)
                            ,0)

    
	# Save the good points into Lists
	
    cv.Zero(imgc)
    x1,x2,y1,y2,angle,dist= (list() for i in range(6))
	
    for k in range((numpy.shape(features)[0])):
	
        featk  = (features[k])
        movk   = (Mov[k])

        if stat[k] ==1 and trackerr[k] < 1000:

            x1.append(featk[0]) , y1.append(featk[1])
            x2.append(movk[0]) , y2.append(movk[1])
            dist.append(math.sqrt(math.pow((x2[-1]-x1[-1]),2)+math.pow((y2[-1]-y1[-1]),2)))
            angle.append(math.atan2(y1[-1]-y2[-1],x1[-1]-x2[-1]))

			
    # Get rid of bad data
    
    #time.sleep(0.5)
    avgdist = numpy.mean(dist)
    i = -1
    #
    for l in dist:
        i = i+1
        if l < 5*avgdist  and Dif_Comb[y1[i],x1[i]] ==255.0 and l>2:
            RGB =frame_Current[y1[i],x1[i]]
            cv.Line(imgc,(x1[i],y1[i]),(x2[i],y2[i]), RGB, 1,8,0)
            arrx 	= (x2[i] + 3*math.cos(angle[i] +math.pi/4))
            arry 	= (y2[i] + 3*math.sin(angle[i] +math.pi/4))
            cv.Line(imgc, (arrx,arry) ,(x2[i],y2[i]), RGB, 1,8,0)
            arrx  	= (x2[i] + 3*math.cos(angle[i] -math.pi/4))
            arry  	= (y2[i] + 3*math.sin(angle[i] -math.pi/4))
            cv.Line(imgc, (arrx,arry) ,(x2[i],y2[i]), RGB, 1,8,0) 
            FileCSV.writerow([timei, RGB,angle[i],i,x1[i],y1[i]])

            
            
    cv.SetImageROI(OnTop,(0,0,frameW,frameH))
    cv.Resize(frame_Current,OnTop)
    cv.ResetImageROI(OnTop)
    cv.SetImageROI(OnTop,(0,frameH,frameW,frameH))
    cv.Resize(imgc,OnTop)
    cv.ResetImageROI(OnTop)
    
    #Display the Windows
	
    #cv.ShowImage("Difference",Dif_Comb)
    #cv.ShowImage("Current",OnTop)
    #cv.ShowImage("Background",backtot)
    #cv.ShowImage("Difference between frames",Dif_Frame)
    #imagesL.append(imgc)
    cv.WriteFrame(writer,OnTop)
	
	
    #Break out of the loop when escape is pressed
	
    #if cv.WaitKey(0) == 27:
     #   cv.DestroyWindow("Current")
    #    break

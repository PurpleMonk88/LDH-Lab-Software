from __future__ import division
import time, numpy, math, cv, csv, glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


point = (0,0)
R = numpy.array([])
G = numpy.array([])
B = numpy.array([])
ERGB = numpy.array([])
timeS = numpy.array([])
RGB = numpy.zeros([1,3])


filename = raw_input('Please Enter The Sample/Run Name: ')
pdf = PdfPages(filename+'.pdf')
FileCSV = csv.writer(open(filename+'.csv','ab'))
FileCSV.writerow(['Time /min', 'R data', 'G Data', 'B Data', 'ERGB Data', 'Pinking Time',
                  'Yellowing Time','Final Degredation Time'])


isColor = 1
fps     = 15 # or 30, frames per second
frameW  = 640 # images width
frameH  = 480 # images height
f1 = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,0.5,0.5,0,1,1)
writer 	= cv.CreateVideoWriter(filename+"_Cam1.avi",cv.CV_FOURCC('D', 'I', 'V', 'X') , fps,(frameW,frameH),isColor)

def smoothGen(Band):
    
    Output = numpy.zeros_like(Band)
    for k in range(len(Band)):
        if k>20 and k < (len(Band)-20):
            Output[k] = numpy.mean(Band[k-20:k])
        if k<=20:
            Output[k] = numpy.mean(Band[0:len(Band)])
        if k >= len(Band)-20:
            Output[k] = numpy.mean(Band[k-20:k])
            
    return Output  


def mouseClick(event,x,y,param,_):
   
    global point
    if event ==cv.CV_EVENT_LBUTTONDOWN:
        point = (x,y)
        click = True
    else: point = (0,0) 
    
    return point


def xax(timeArr):
    
    if timeArr[-1] < 1:
        x = numpy.ceil(timeArr[-1]/1)*1
    else : x = numpy.ceil(timeArr[-1]/5)*5
    
    return x  


def checkzero(CheckArr):
    
    sol = numpy.zeros(len(CheckArr))
    for i in range(len(CheckArr)):
        if CheckArr[i] < 1:
            sol[i] = CheckArr[i]+0.01
        else: sol[i] = CheckArr[i]

    return sol

capture = cv.CaptureFromCAM(0)
time2 = 0
time3 = 0 

#Select the point to analyse
while True:
    
    img = cv.QueryFrame(capture)
    cv.SetMouseCallback("Click the point to analyse",mouseClick, None)
    cv.ShowImage("Click the point to analyse", img)
    
    if point == (0,0):
        point = (0,0)
    else:
        cv.DestroyWindow("Click the point to analyse")
        break  
    
    if cv.WaitKey(10) == 27:
        cv.DestroyWindow("Click the point to analyse")
        break

cv.NamedWindow("camera", 1)
time0 = time.time()
plt.ion()
plt.hold(False)

#Plot the webcam feed and data
while True:
    
    time1= (time.time()-time0)/60
    timeS = numpy.append(timeS,time1)

    img = cv.QueryFrame(capture)
    cv.Rectangle(img,(point[0]-6,point[1]-6),(point[0]+6,point[1]+6),cv.RGB(155,0,25),1)    
    coag = cv.Avg(img[(point[1]-5):(point[1]+5),(point[0]-5):(point[0]+5)])
    coag = checkzero(coag)
    
    R = numpy.append(R,coag[2]/2.54)
    G = numpy.append(G,coag[1]/2.54)
    B = numpy.append(B,coag[0]/2.54)
    
    ERGB1 = math.log10(100/(coag[0]/2.54)) + 0.95*math.log10(100/(coag[1]/2.54)) + 0.922*(100/(coag[2]/2.54))
    
    ERGB = numpy.append(ERGB,ERGB1)

    fig1 = plt.subplot(211)
    plt.plot(timeS,R,'r',timeS,G,'g',timeS,B,'b')  
    plt.ylim(0,100)
    plt.xlabel('time /min')
    plt.ylabel('% Reflectance')
    
    fig2 = plt.subplot((212),sharex = fig1)
    plt.plot(timeS,ERGB,'k')
    plt.ylim(0,10)
    plt.xlabel('time /min')
    plt.ylabel('RGB Extinction')
    plt.xlim(0,xax(timeS)) 
    
    plt.draw()
    cv.ShowImage("camera", img)
    time2 = numpy.round(time3)
    time3 = numpy.round(timeS[-1])
    
    if cv.WaitKey(10) == 27:
        cv.DestroyWindow("camera")
        plt.ioff()
        plt.clf()
        plt.close()
        break

    cv.PutText(img,"FPS = "+str(numpy.round(fps)),(10,15),f1,-1)
    cv.ShowImage("camera", img)
    cv.WriteFrame(writer,img)
      
#Smooth the 3 colour bands                
R = smoothGen(R)
G = smoothGen(G)
B = smoothGen(B)
ERGB = smoothGen(ERGB)

RoverB = numpy.zeros(len(R))
RoverG = numpy.zeros(len(G))

Pink = (0,0)
Yellow = (0,0)
Black = (0,0)
y = (0,100)
RoverB = R/B
RoverG = R/G


#Find the Pinking Point
for m in range(len(RoverB)):
    
    if RoverB[m] > 1.05*(numpy.mean(RoverB[0:10])):
        Pink = (timeS[m], timeS[m])
        break
  
    
#Find the Yellowing point
for m in range(len(RoverB)):
    
    if RoverG[m] > 1.15*(numpy.mean(RoverG[0:10])):
        Yellow =  (timeS[m], timeS[m])
        break
   
            
#Find the total degradation point if there is one
for m in range(len(RoverB)):
    
    if numpy.mean([R[m],G[m],B[m]]) < 12:
        Black = (timeS[m], timeS[m])
        break


#Write the RGB data to CSV
for f in range(len(R)):
    
    FileCSV.writerow([timeS[f],R[f],G[f],B[f],ERGB[f],Pink[0],Yellow[0],Black[0]])

fig1 = plt.subplot(211)
plt.plot(timeS,R,'r',timeS,G,'g',timeS,B,'b',
         Pink,y,'pink',Yellow,y,'y',Black,y,'k') 
plt.ylim(0,100)
plt.xlabel('time /min')
plt.ylabel('% Reflectance')
    
fig2 = plt.subplot((212),sharex = fig1)
plt.plot(timeS,ERGB,'k')
plt.ylim(0,10)
plt.xlabel('time /min')
plt.ylabel('RGB Extinction')
plt.xlim(0,xax(timeS))

pdf.savefig()
pdf.close()




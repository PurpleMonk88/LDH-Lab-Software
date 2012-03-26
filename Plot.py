import cv

imgc	 		= cv.CreateImage((400,400),cv.IPL_DEPTH_8U,3)
point =(0,0)
def mouseMove(event,x,y,param,_):
   
    global point
    if event ==cv.CV_EVENT_MOUSEMOVE:
        point = (x,y)
        click = True
    else: point = (0,0) 
    
    return point
	
while True:
    #cv.Zero(imgc)
    #img = cv.QueryFrame(capture)
    cv.SetMouseCallback("Click the point to analyse",mouseMove, None)
    cv.ShowImage("Click the point to analyse", imgc)
    
    if point == (0,0):
        point = (0,0)
    else:
        cv.Line(imgc, (point[0],0) ,(point[0],400), (255,0,0), 1,8,0)
        

    
    if cv.WaitKey(10) == 27:
        cv.DestroyWindow("Click the point to analyse")
        break
import cv, glob,os

print('')
print('-------------------------------------------------------------------')
print('Set the compression method to Microsoft video 1 and the compression')
print('                     quality to 20%')
print('-------------------------------------------------------------------')

AllImages = glob.glob('*.jpg')
AllImages.sort()
nFrames = len(AllImages)

isColor = 1
fps     = 8  # or 30, frames per second
frameW  = 640 # images width
frameH  = 480 # images height
filename = AllImages[0][0:6]
writer 	= cv.CreateVideoWriter(filename+".avi",-1, fps,(frameW,frameH),isColor)

for i in range(nFrames):
    img = cv.LoadImage(AllImages[i]) #specify filename and the extension
    cv.WriteFrame(writer,img)

#cv.ReleaseVideoWriter(writer) #

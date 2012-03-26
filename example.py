from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np

def on_hover(event):
   X1 = event.xdata
   Y1 = event.ydata
   print X1,Y1

x = [0,1,2,3]
y = [0,1,2,3]
X1, Y1 = 0,0
fig = plt.figure()
plt.ion()
plt.hold(False)
ax1 = plt.subplot2grid((2,2),(0,0), colspan=2)
ax1.set_title('click to build line segments')
ax1.scatter(x,y)
cid = fig.canvas.mpl_connect('motion_notify_event', on_hover)


ax2 = plt.subplot2grid((2,2),(1,0))
ax2.scatter(X1,Y1)

ax3 = plt.subplot2grid((2,2),(1,1))

cursor = Cursor(ax1, useblit=True, color='black', linewidth=1 )
plt.draw()

plt.ioff()


#plt.show()
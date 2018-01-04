import time
from roboclaw import Roboclaw

#Windows comport name
#rc = Roboclaw("COM9",115200)
#Linux comport name
#rc = Roboclaw("/dev/ttyACM0",115200)
rc = Roboclaw("/dev/ttyS0",115200)

rc.Open()

notdone=True
while notdone:
	#Get version string
	version = rc.ReadVersion(0x80)
	if version[0]==False:
		print "GETVERSION Failed"
	else:
		print repr(version[1])
	time.sleep(1)
	notdone=False


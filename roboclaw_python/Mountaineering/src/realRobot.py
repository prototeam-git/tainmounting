import sys
import RTIMU
import time

class Robot:
    def __init__(self):
        SETTINGS_FILE = "setting"

        self.s = RTIMU.Settings(SETTINGS_FILE)
        self._imu = RTIMU.RTIMU(self.s)
        if (not self._imu.IMUInit()):
            print 'cannot init'
            sys.exit(1)

        self._imu.setSlerpPower(0.02)
        self._imu.setGyroEnable(True)
        self._imu.setAccelEnable(True)
        self._imu.setCompassEnable(True)

        poll_interval = self._imu.IMUGetPollInterval()
        if self._imu.IMURead():
            data = self._imu.getIMUData()
            accel = data["accel"]
            print accel
            self._degree = accel[0]
        else:
            print 'Cannot read imu'
            self._degree = -1000 #Error

    @property
    def degree(self):

        if self._imu.IMURead():
            data = self._imu.getIMUData()
            accel = data["accel"]
            self._degree = accel[0]
            print 'accel: ' + str(accel)
        else:
            print 'cannot read imu'
            self._degree = -1000 #Error
        return self._degree

rb = Robot()

while(1):
    rb.degree
    time.sleep(0.2)

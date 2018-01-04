from ConfigParser import SafeConfigParser
from fakeRobot import Robot
import constants
import time
from roboclaw import Roboclaw

#Windows comport name
# rc = Roboclaw("COM3",115200)
#Linux comport name

class Controller():
    '''
    Controller class where it contains the PID equation
    '''
    def __init__(self, configPath):

        print 'reading config from path...' + configPath
        parser = SafeConfigParser()
        parser.read(configPath)

        #Reading the configurations
        self._P = parser.get('pid_coeff', 'P')
        self._I = parser.get('pid_coeff', 'I')
        self._D = parser.get('pid_coeff', 'D')
        self._PR = parser.get('pid_coeff', 'PR')
        self._PL = parser.get('pid_coeff', 'PL')
        self._speed = parser.get('motion', 'speed')
        self._accel = parser.get('motion', 'accel')
        self._samplingRate = parser.get('pid_coeff', 'samplingRate')
        self._port = parser.get('systems', 'port')

        self._robot = Robot()

        #setup the roboclaw here
        self._rc = Roboclaw(self._port,115200)
        self._rc.Open()

    #Obsolete
    # def P():
    #     doc = "The P property."
    #     def fget(self):
    #         return self._P
    #     def fset(self, value):
    #         self._P = value
    #     def fdel(self):
    #         del self._P
    #     return locals()
    # P = property(**P())
    #
    # def I():
    #     doc = "The I property."
    #     def fget(self):
    #         return self._I
    #     def fset(self, value):
    #         self._I = value
    #     def fdel(self):
    #         del self._I
    #     return locals()
    # I = property(**I())
    #
    # def D():
    #     doc = "The D property."
    #     def fget(self):
    #         return self._D
    #     def fset(self, value):
    #         self._D = value
    #     def fdel(self):
    #         del self._D
    #     return locals()
    # D = property(**D())

    def _getCurDegree(self):
        return self._robot.degree

    def _getCorrection(self, toBeDegree):
        #error Negative value == moving to the left
        #error Positive value == moving to the right
        error = toBeDegree - self._getCurDegree()

        print 'Error: ' + str(error)
        ctlSig = self._P * error            #Simple P control Signal
        print 'Control signal: ' + str(ctlSig)
        return ctlSig

    def _getLeftWheelSpeed(self, toBeDegree):
        ctlSig = self._getCorrection(toBeDegree)
        speed = self._speed - self._speed * ctlSig
        return speed

    def _getRightWheelSpeed(self, toBeDegree):
        ctlSig = self._getCorrection(toBeDegree)
        speed = (self._speed + self._speed * ctlSig) * -1
        return speed

    def _moveFW(self, speedL, speedR):
        self._rc.SpeedAccelM1(constants.ADDRESS, self._accel, speedL)
        self._rc.SpeedAccelM2(constants.ADDRESS, self._accel, speedR)

    def stop(self):
        self._rc.SpeedM1(constants.ADDRESS, 0)
        self._rc.SpeedM2(constants.ADDRESS, 0)

    def moveFWControlled(self, degree, seconds):
        time = 0

        while(time < seconds):
            speedL = self._getLeftWheelSpeed(degree)
            speedR = self._getRightWheelSpeed(degree)
            self._moveFW(speedL, speedR)
            sleep(self._samplingRate / 1000)        #convert ms to secs
            time = time + self._samplingRate / 1000
        self.stop()

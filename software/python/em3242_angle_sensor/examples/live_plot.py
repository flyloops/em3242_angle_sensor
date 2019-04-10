from __future__ import print_function
import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import signal
from em3242_angle_sensor import EM3242_AngleSensor


class EM3242LivePlot(object):

    def __init__(self,port='/dev/ttyACM0'):

        self.em3242 = EM3242_AngleSensor(port)

        self.window_size = 10.0

        self.t_init =  time.time()
        self.t_list = []
        self.angle_list = []

        self.position = 0.0
        self.last_angle = 0.0

        self.is_first = True
        self.running = False
        signal.signal(signal.SIGINT, self.sigint_handler)

        plt.ion()
        self.fig = plt.figure(1)
        self.ax = plt.subplot(111) 
        self.angle_line, = plt.plot([0,1], [0,1],'.b')
        plt.grid('on')
        plt.xlabel('t (sec)')
        plt.ylabel('angle (deg)')
        self.ax.set_xlim(0,self.window_size)
        self.ax.set_ylim(0,360)
        plt.title("EM3242 Angle Sensor ")
        self.angle_line.set_xdata([])
        self.angle_line.set_ydata([])
        self.fig.canvas.flush_events()


    def sigint_handler(self,signum,frame):
        self.running = False

    def update_position(self,angle):
        """
        Unwraps the angle data to get cummulative position.
        """
        if self.is_first:
            self.is_first = False
            self.position = angle
        else:
            diff_angle = angle - self.last_angle
            if diff_angle > 180.0:
                self.position += (360 - angle) - self.last_angle
            elif diff_angle < -180.0:
                self.position += angle + (360.0 - self.last_angle)
            else:
                self.position += diff_angle
        self.last_angle = angle

    def run(self):

        self.em3242.start()
        self.running = True

        with open('data.txt', 'w') as fid:
            while self.running: 
                angle = self.em3242.angle
                self.update_position(angle)

                t_elapsed = time.time() - self.t_init
                self.t_list.append(t_elapsed)
                self.angle_list.append(angle)

                while (self.t_list[-1] - self.t_list[0]) > self.window_size:
                    self.t_list.pop(0)
                    self.angle_list.pop(0)

                self.angle_line.set_xdata(self.t_list)
                self.angle_line.set_ydata(self.angle_list)
                xmin = self.t_list[0]
                xmax = max(self.window_size, self.t_list[-1])
                self.ax.set_xlim(xmin,xmax)
                self.fig.canvas.flush_events()
                fid.write('{0} {1} {2}\n'.format(t_elapsed, angle, self.position))
                print('angle: {0:0.1f}, position: {1:0.1f}'.format(angle, self.position))

        self.em3242.stop()




# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyACM0'

    liveplot = EM3242LivePlot(port=port)
    liveplot.run()




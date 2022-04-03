
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import enum

@enum.unique
class PlotType(enum.Enum):
    line = 1
    XY = 2
    logX = 3
    logY = 4
    logXLogY = 5
    lnX = 6
    lnY = 7
    lnXLnY = 8


## TODO: Add XYZ to XY. Autounderstanding :D
class SimplePlot:
    '''
    Online plotter class
    '''
    def __init__(
        self,
        time_limit = None,
        size_limit = 100,
        dim = None,
        legend = None,
        xlim = None,
        ylim = None
        ):
        self.__t_limit = time_limit
        self.__buf_size = size_limit
        self.__dim = dim
        self.__legend = legend
        self.__states = []
        self.__t_start = None
        self.__first_start = True
        self.__run = True
        self.__ylim = ylim
        self.__xlim = xlim
        self.__type = None

        self.__initialize()

    def __initialize(self):
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_axes([0.075, 0.075, .925, .925])
        plt.show(block = False)

    def stop(self):
        self.__run = False

    def start(self):
        self.__run = True

    def reset(self):
        self.__states = []
        self.__first_start = True
        self.__ax.clear()
        plt.pause(.001)

    @property
    def type(self):
        return self.__type

    def __check_type(self, type: enum.Enum):
        if self.__type is None:
            self.__type = type
            return
        if self.__type != type:
            exit(
                'Wrong plot type: %s. Must be: %s' % \
                    (type.name, self.__type.name)
            )

    def updateXY(self,x,y = None):
        self.__check_type(PlotType.XY)
        t = time.time()
        if self.__first_start:
            self.__dim = 2
            self.__t_start = t
            self.__first_start = False

        if self.__run:
            if y is None:
                self.__states.append([t, x[1], x[2]])
            else:
                self.__states.append([t, [x, y]])
            self.__ax.clear()
            if self.__t_limit is None:
                if len(self.__states) > self.__buf_size:
                    self.__states.pop(0)
            else:
                while len(self.__states) > 1:
                    dt = self.__states[-1][0] - self.__states[0][0]
                    if dt > self.__t_limit:
                        self.__states.pop(0)
                    else:
                        break
            self.__ax.plot(
                [self.__states[x][1][0] for x in range(len(self.__states))],
                [self.__states[x][1][1] for x in range(len(self.__states))]
            )
            if not self.__ylim is None:
                self.__ax.set_ylim(
                bottom = min(self.__ylim),
                top = max(self.__ylim)
            )
            if not self.__xlim is None:
                self.__ax.set_xlim(
                left = min(self.__xlim),
                right = max(self.__xlim)
            )
            self.__ax.legend(self.__legend)
            self.__fig.canvas.draw()
            self.pause(.001)



    def update(self, state):
        self.__check_type(PlotType.line)
        t = time.time()
        if self.__first_start:
            if self.__dim is None:
                self.__dim = len(state)
            if self.__legend is None:
                self.__legend = ['signal ' + str(x) for x in range(self.__dim)]
            self.__t_start = t
            self.__first_start = False
        if self.__run:
            if len(state) == self.__dim:
                self.__states.append([t-self.__t_start, state])
                self.__ax.clear()
                if self.__t_limit is None:
                    if len(self.__states) > self.__buf_size:
                        self.__states.pop(0)
                else:
                    while len(self.__states) > 1:
                        dt = self.__states[-1][0] - self.__states[0][0]
                        if dt > self.__t_limit:
                            self.__states.pop(0)
                        else:
                            break
                self.__ax.plot(
                    [self.__states[x][0] for x in range(len(self.__states))],
                    [self.__states[x][1] for x in range(len(self.__states))]
                )
                if not self.__ylim is None:
                    self.__ax.set_ylim(bottom = min(self.__ylim), top = max(self.__ylim))
                self.__ax.legend(self.__legend)
                self.__fig.canvas.draw()
                self.pause(.001)

    def pause(self,interval):
        backend = plt.rcParams['backend']
        if backend in matplotlib.rcsetup.interactive_bk:
            figManager = matplotlib._pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                canvas.start_event_loop(interval)
                return

if __name__=="__main__":
    import math
    sp_sin = SimplePlot(
        time_limit = 5,
        dim = 1,
        legend = ["sin(t)"],
        ylim = (-1,1)
    )
    sp_cos = SimplePlot(
        size_limit = 250,
        legend = ["cos(t)"],
        ylim = (-1,1)
    )
    sp_XY = SimplePlot(
        time_limit = 15,
        legend = ["X","Y"],
        xlim = (-1,1),
        ylim = (-1,1)
        )
    start_time = time.time()
    while True:
        sin = math.sin(time.time())
        cos = math.cos(time.time())
        demp = math.exp((start_time-time.time())/10)
        sp_sin.update(np.array([sin]))
        sp_cos.update(np.array([cos]))
        sp_XY.updateXY(demp*sin,demp*cos)

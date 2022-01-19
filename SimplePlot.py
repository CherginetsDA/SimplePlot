
import matplotlib.pyplot as plt
import numpy as np
import time

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


    def update(self, state):
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
                plt.pause(.001)

if __name__=="__main__":
    import math
    sp_sin = SimplePlot(time_limit = 5, dim = 1, legend = ["sin(t)"], ylim = (-1,1))
    # sp_cos = SimplePlot(size_limit = 250, legend = ["cos(t)"], ylim = (-1,1))
    while True:
        sp_sin.update(np.array([math.sin(time.time())]))
        # sp_cos.update(np.array([math.cos(time.time())]))

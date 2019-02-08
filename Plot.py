from colour import Color
from itertools import chain
from Point import Point
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import os


class Plot:
    def __init__(self, name):
        self._plotid = 0
        self._name = name
        self._anoms = set()
        # self.readAnoms()
        # self.font = {'family': 'serif',
                    # 'color':  'darkred',
                    # 'weight': 'normal',
                    # 'size': 16,
                    # }

    def readAnoms(self):
        f = open("cases_anom.txt", 'r')
        for line in f:
            self._anoms.add(line.strip())
        # print(self.anoms)

    def saveFunc(self):
        directory = f'plot/{self._name}'
        filen = f'{str(self._plotid)}.png'

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        plt.savefig(f'{directory}/{filen}')

    def plotFunc(self, gp_pts, pts, name, act_name, color_range=10):
        # params common to all scatters
        s = 50
        edgecolors = 'grey'

        # create figure and define titles and legend
        fig = plt.figure(figsize=(9,6.5))
        ax = fig.add_subplot(111, projection='3d')

        self._plotid += 1
        title = f'{name} (event: {self._plotid})'
        rtitle = f'Event: {act_name}'
        ax.set_title(title, fontsize=15)
        ax.title.set_position([.5, -.1])
        ax.set_title(rtitle, loc='right')

        ax.axis([-.5, 3.05, -.5, 3.05])
        ax.set_xlim(-.5, 3.05)
        ax.set_ylim(-.5, 3.05)
        ax.set_zlim(0, 1)
        ax.set_xlabel('EWD', fontsize=15)
        ax.set_ylabel('TWD', fontsize=15)
        ax.set_zlabel('Time', fontsize=15)

        # x = 30
        # y = 30
        # z = 30
        # leg_anom = ax.scatter(x, y, z, marker='v', alpha=.8, c='white',
        #                       edgecolors=edgecolors, s=s)
        # leg_normal = ax.scatter(x, y, z, marker='o', alpha=.8, c='white',
        #                         edgecolors=edgecolors, s=s)
        leg_gp = mpatches.Patch(color='blue')
        leg_older = mpatches.Patch(color=Color('yellow').rgb)
        leg_newer = mpatches.Patch(color=Color('red').rgb)
        plt.legend([leg_gp, leg_older, leg_newer],
                   ["Grace Period", "Older Events", "Newer Events"],
                   bbox_to_anchor=(0.21, 1.15))

        # last times are normalized (0,1)/ j variable and norm are used in the subsequent loops instead of pt._last_time, since pt._last_time keeps the original value
        l = [p._last_time for p in chain(gp_pts, pts)]
        norm = [(i-min(l))/(max(l)-min(l)) for i in l]

        j = 0
        # plot gp points
        for pt in gp_pts:
            x = pt._ewd
            y = pt._twd
            z = norm[j]
            j += 1
            # marker = 'v' if pt._case_id in self._anoms else 'o'
            marker = 'o'
            ax.scatter(x, y, z, c='blue', marker=marker, alpha=0.6, s=s)

        # plot other points
        colors = list(Color('yellow').range_to(Color('red'), color_range))
        if len(pts) > color_range:
            overflow_colors = [Color('yellow')] * (len(pts) - color_range)
        else:
            colors = colors[len(colors) - len(pts):]
            overflow_colors = []

        for pt, color in zip(pts, chain(overflow_colors, colors)):
            # marker = 'v' if pt._case_id in self._anoms else 'o'
            marker = 'o'
            ax.scatter(pt._ewd, pt._twd, norm[j], marker=marker,
                       alpha=0.8, c=color.get_rgb(),
                       edgecolors=edgecolors, s=s)
            j += 1

        plt.show()
        # self.saveFunc()
        plt.close()

"""Plotting using pandas and matplotlib."""

import itertools
from collections import defaultdict
from operator import itemgetter

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import savefig


def plots(data:iter, title, dpi=400, savefile=False, show=True, xlabel='Elements'):
    """Plot given data"""
    gx = pd.DataFrame({'score': data})

    # blue, red, yellow, black, magenta and green color for each container,
    # with a circle or a cross for existing or missing item
    styles = [a + b + '-' for a, b in itertools.product('brykmg', 'ox')]

    plot = gx.plot(style=styles, title=title)
    lines, labels = plot.get_legend_handles_labels()

    plot.legend(lines, labels, loc='best')
    plot.set_xlabel(xlabel)
    plot.set_ylabel('Frequency')

    if savefile:
        plt.savefig(savefile, dpi=dpi)
        print('Plot of statistics data saved in file ' + savefile
              + ' (' + str(dpi) + ' dpi)')
    if show:
        plt.show()


def plot_time(data, savefile=False, show=True, dpi=500,
              nb_run=None, nb_method=None):
    for item in sorted(set(data.keys()) - {'rank'}):
        print(item + ':', data[item])
    print(data['rank'])
    gx = pd.DataFrame(data, columns=sorted(set(data.keys()) - {'rank'}),
                      index=data['rank'])

    # blue, red, yellow, black, magenta and green color for each container,
    # with a circle or a cross for existing or missing item
    # styles = [a + b + '-' for a, b in itertools.product('ox', 'brykmg')]
    styles = [
        # crosses, dots
        'xb-', 'ob-',  # blue   : dumb method
        'xr-', 'or-',  # red    : linear method
        'xy-',         # yellow : linear recursive method
        'xg-', 'og-',  # green  : stdlib method
    ]

    title = ('Runtime measure for {} runs of {} methods\n'
             'function of the percentage of elements in the subset\n'
             'with 100 or 1000 elements').format(nb_run, nb_method)
    plot = gx.plot(style=styles, title=title, figsize=(14.,10.))
    lines, labels = plot.get_legend_handles_labels()

    # get legend outside the plot: cf http://stackoverflow.com/a/4701285
    # Shrink current axis by 20%
    box = plot.get_position()
    plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    plot.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # plot.legend(lines, labels, loc='center right', bbox_to_anchor=(1.3, 0.5),
                # ncol=1, fancybox=True, shadow=True)
    # plot.legend(lines, labels, loc='best')
    plot.set_xlabel('% of element in the subset')
    plot.set_ylabel('Runtime in second')

    if savefile:
        plt.savefig(savefile, dpi=dpi)
        print('Plot of statistics data saved in file ' + savefile
              + ' (' + str(dpi) + ' dpi)')
    if show:
        plt.show()

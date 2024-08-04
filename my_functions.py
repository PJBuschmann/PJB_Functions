import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from functools import reduce
import pandas as pd

def normalize(v):
    return [i/sum(v) for i in v]


def factors(n):    
    return list(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def get_median_int(v):
    l = len(v)
    if l % 2 == 0:
        return v[int(l/2)]
    else:
        return v[int(l/2)]

def marimekko(data: list | dict | pd.Series,
 nrows: int=0,
 ncols: int=0,
 text: bool=False,
 numbers: bool=False,
 fontsize: int=16,
 gap: float=0.005,
 debug: bool=False,
 figsize: tuple=(8,5),
 rounding: float=0.005,
 cmap: str='',
 title: str=''):
    
    length = len(data)
    keys = []

    # TODO: Accept multiple data structures, such as dict or Series

    if type(data) == pd.Series:
        data = data.to_dict()

    if type(data) == dict:
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
        keys = list(data.keys())
        data = data.values()
 
    # Auto-assign ncols & nrows if zero
    if ncols == 0 or nrows == 0:
        if ncols > 0:
            if length%ncols != 0:
                raise ValueError('Length of data is nto a multiple of ncols')
            nrows = int(length / ncols)
        elif nrows > 0:
            if length%nrows != 0:
                raise ValueError('Length of data is nto a multiple of nrows')
            ncols = int(length / nrows)
        else:
            median_factor = get_median_int(sorted(factors(length)))
            ncols, nrows = median_factor, int(length/median_factor)
        if debug: print(nrows, ncols)

    # Checks
    if length != nrows*ncols:
        raise ValueError('Length of data must be equal to ncols * nrows.')
    if ncols < 0 or nrows < 0:
        raise ValueError('Parameters ncols and nrows must be greater or equal to 0.')


    # Accept cmaps to color graph 
    if cmap != '':
        cmap = mpl.colormaps.get_cmap(cmap).reversed()
        colors = cmap(np.arange(0, 1, 1/length))
        if debug: print(colors)

    fig, ax = plt.subplots(figsize=figsize)
    data = sorted(data, reverse=True)
    cols = normalize([0] + [sum(data[i:i+int(length/ncols)]) for i in range(0, length, int(length/ncols))])
    rows = [normalize([0] + data[i:i+nrows]) for i in range(0, length, nrows)]

    for col in range(ncols):
        for row in range(nrows):
            height = rows[col][row+1]-gap
            width = cols[col+1]-gap
            pos = (cols[col+1] + sum(cols[:col+1])-width, rows[col][row] + sum(rows[col][:row]))
            color = (0, 1-(col+row+1)/(ncols+nrows+1), 0.25) if cmap == '' else colors[col*nrows+row]
            ax.add_patch(FancyBboxPatch(pos, width, height, label=f'{row}, {col}', color=color, boxstyle=f'Round, pad=0, rounding_size={rounding}'))
            if text:
                if keys:
                    if numbers:
                        ax.text(pos[0] + width/2, pos[1]+height/2, str(keys[col*nrows+row]) + ': ' + str(round(data[col*nrows+row],2)), ha='center', va='center', fontsize=fontsize*width**.25)
                    else:
                        ax.text(pos[0] + width/2, pos[1]+height/2, str(keys[col*nrows+row]), ha='center', va='center', fontsize=fontsize*width**.25)
                else:
                    ax.text(pos[0] + width/2, pos[1]+height/2, round(data[col*nrows+row],2), ha='center', va='center', fontsize=fontsize*width**.25)
                     
            if debug: print(row, col, pos, width, height)
    if debug: plt.legend()
    plt.axis('off')
    if title != '': plt.title(title)
    return fig

def factors_graph(data):
    mapping = {
        0.0: 'NA',
        1.0: 'Low',
        3.0: 'Medium-Low',
        5.0: 'Medium',
        7.5: 'Medium-High',
        10.0: 'High' 
    }

    colors = {
        0.0: (217/255, 217/255, 217/255),
        1.0: (0/255, 153/255, 51/255),
        3.0: (204/255, 255/255, 102/255),
        5.0: (230/255, 230/255, 0/255),
        7.5: (230/255, 92/255, 0/255),
        10.0: (204/255, 0/255, 0/255) 
    }

    fig, ax = plt.subplots(figsize=figsize)

    length = len(data)
    keys = list(data.keys())
    plt.axis('off')

    for i in range(length):
        pos = (.05, (length-(i+.5))/length)
        ax.text(pos[0], pos[1], keys[i], va='center', ha='center')
        ax.add_patch(Circle((pos[0]+.1, pos[1]), radius=.02, color=colors[data[keys[i]]]))
    return fig
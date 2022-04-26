import numpy as np    
import matplotlib as mpl

def make_cmap(colors:list, position:list=None, bit:bool=False, cmap_name:str='my_colormap'):
    '''
    Make a new color map based on the provided colors

    Parameters
    ----------
    colors : list
        values may either be in 8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default)
    position: list
        colors order
    bit: boolean
        Whether to use 8-bit or arithmetic (default)
    
    Returns
    -------
    Matplotlib Colormap
    '''
    
    bit_rgb = np.linspace(0,1,256)
    if position is None:
        position = np.linspace(0,1,len(colors))
    else:
        assert len(position) == len(colors), 'must be the same as colors'
        assert (position[0] == 0) and (position[-1] == 1), 'position must start with 0 and end with 1'
    if bit:
        colors = [(bit_rgb[color[0]],
                    bit_rgb[color[1]],
                    bit_rgb[color[2]]) for color in colors]

    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap(cmap_name, cdict, 256)
    return cmap

hex2rgb = lambda hexcode: tuple(int(hexcode.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def map_val(val, xmin, xmax, umin, umax):
    return (val - xmin) / (xmax - xmin) * (umax - umin) + umin

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w
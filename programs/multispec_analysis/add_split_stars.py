from matplotlib import pyplot
from astropy.io import fits, ascii
import numpy as np
import os
import pdb
import shutil

def label_stars(ax, x, y, label, color = 'r'):
    for ix, iy, ilabel in zip(x, y, label):
        ax.text(ix, iy, ilabel, color = color)
    


def display_stis_and_wfc3_image(stis_file, wfc3_file):
    '''
    Display STIS and WFC3 image
    '''
    fig = pyplot.figure(figsize = [25, 15])
    ax_stis = fig.add_subplot(1, 2, 1)
    ax_wfc3 = fig.add_subplot(1, 2, 2)
    stis_img = fits.getdata(stis_file, 0)
    wfc3_img = fits.getdata(wfc3_file, 0)
    im_stis = ax_stis.imshow(stis_img, interpolation = None, cmap = 'bone', vmin = 0, vmax = 50)
    im_wfc3 = ax_wfc3.imshow(wfc3_img, interpolation = None, cmap = 'bone', vmin = 0, vmax = 50)
    ax_stis.set_title('STIS Psuedo Image')
    ax_wfc3.set_title('WFC3 Cropped Image')
    ax_stis.set_ylim(900, 1040)
    ax_stis.set_xlim(-10, 70)
    ax_wfc3.set_ylim(900, 1040)
    return im_stis, im_wfc3, ax_stis, ax_wfc3

def plot_star_locations_and_label(coord_file, ax_stis, ax_wfc3):
    '''
    read in everything and plot star locations and label
    '''
    tbdata = ascii.read(coord_file)
    ax_stis.plot(tbdata['wfc3_x'].data -1, tbdata['wfc3_y'].data - 1, 'r+')
    ax_wfc3.plot(tbdata['wfc3_x'].data - 1, tbdata['wfc3_y'].data - 1, 'r+')
    label_stars(ax_stis, tbdata['wfc3_x'].data, tbdata['wfc3_y'].data, tbdata['id'].data)
    label_stars(ax_wfc3, tbdata['wfc3_x'].data, tbdata['wfc3_y'].data, tbdata['id'].data)
    return ax_stis, ax_wfc3

def plot_single_slit_locations(slit_num, ax_stis, cenwave, color = 'y'):
    '''
    Read in a single slit file and replot in a different color
    '''
    print 'slit = ', slit_num
    if slit_num < 10:
        tbdata = ascii.read('slit0{}_{}_phot.dat'.format(int(slit_num), cenwave))
    else:
        tbdata = ascii.read('slit{}_{}_phot.dat'.format(int(slit_num), cenwave))
    ax_stis.plot(np.ones(tbdata['y'].shape)*((slit_num -1)*4 + 2), tbdata['y'].data - 1, 
                        color = color, marker = 'o', linestyle = 'none', markersize = 10)
    pyplot.draw()
    return ax_stis


def set_contrast(image):
    new_contrast_limit = raw_input('Enter new contrast limit ')
    image.set_clim(0, float(new_contrast_limit))
    pyplot.draw()

def add_star_to_slit(slit_num, tbdata_current, tbdata_previous, tbdata_next):
    split_star_id = raw_input('Enter the star ID which is labeled in another slit but should be added to current slit')
    if slit_num != 1:
        if split_star_id in tbdata_previous['ID']:
            indx = np.where(tbdata_previous['ID'] == split_star_id)[0][0]
            tbdata_current.add_row(tbdata_previous[indx])
        if split_star_id != 17:
            if split_star_id in tbdata_next['ID']:
                indx = np.where(tbdata_next['ID'] == split_star_id)[0][0]
                tbdata_current.add_row(tbdata_next[indx])
    return tbdata_current

def move_down_slit(axis_obj):
    current_limits = axis_obj.get_ylim()
    if current_limits[0] == 0:
        axis_obj.set_ylim(900, 1040)
    else:
        axis_obj.set_ylim(max(0, current_limits[0] - 140), max(0,current_limits[1] - 140))
    pyplot.draw()
    return axis_obj

def draw_slit(ax_stis, slit_num):
    l2 = ax_stis.axvline((slit_num - 1)*4 - 0.5, color = 'c')
    l3 = ax_stis.axvline(slit_num*4 - 0.5, color = 'c')
    return l2, l3
def get_filename(slit_num, cenwave):
    if slit_num < 10:
        filename = 'slit0{}_{}_phot.dat'.format(int(slit_num), cenwave)
    else:
        filename = 'slit{}_{}_phot.dat'.format(int(slit_num), cenwave)
    return filename 

def add_stars(slit_num, ax_stis, ax_wfc3, im_stis, im_wfc3, cenwave):
    '''
    #ask if any stars need to be added
    '''
    tbdata_current = ascii.read(get_filename(slit_num, cenwave))
    if slit_num == 1:
        tbdata_previous = None
        tbdata_next = ascii.read(get_filename(slit_num+1, cenwave))
    elif slit_num == 17:
        tbdata_next = None
        tbdata_previous = ascii.read(get_filename(slit_num -1, cenwave))    
    else:
        tbdata_previous = ascii.read(get_filename(slit_num -1, cenwave))    
        tbdata_next = ascii.read(get_filename(slit_num+1, cenwave))
    ax_stis.set_ylim(900, 1040)
    ax_wfc3.set_ylim(900, 1040)
    pyplot.draw()
    to_do_flag = raw_input('Would you like to adjust the contrast (c), enter a star to be added to this slit (a), move down the slit (m), or move to next slit (q) ? ')
    while to_do_flag != 'q':
        if to_do_flag == 'c':
            set_contrast(im_stis)
            set_contrast(im_wfc3)
        elif to_do_flag == 'a':
            tbdata_current = add_star_to_slit(slit_num, tbdata_current, tbdata_previous, tbdata_next)
        elif to_do_flag == 'm':
            ax_stis = move_down_slit(ax_stis)
            ax_wfc3 = move_down_slit(ax_wfc3)
        to_do_flag = raw_input('Would you like to adjust the contrast (c), enter a star to be added to this slit (a), move down the slit (m), or finish (q) ? ')
    if slit_num < 10:
        shutil.copyfile('slit0{}_{}_phot.dat'.format(int(slit_num), cenwave), 'slit{}_{}_phot_no_split.dat'.format(int(slit_num), cenwave))
        ascii.write(tbdata_current, 'slit0{}_{}_phot.dat'.format(int(slit_num), cenwave))
    else:
        shutil.copyfile('slit{}_{}_phot.dat'.format(int(slit_num), cenwave), 'slit{}_{}_phot_no_split.dat'.format(int(slit_num), cenwave))
        ascii.write(tbdata_current, 'slit{}_{}_phot.dat'.format(int(slit_num), cenwave))
    


if __name__ == "__main__":
    os.chdir('../../multispec/ccd_multispec/')
    im_stis, im_wfc3, ax_stis, ax_wfc3 = display_stis_and_wfc3_image('long_slit_img_3936.fits', 'f336w_63.7_cropped.fits')
    ax_stis, ax_wfc3 = plot_star_locations_and_label('final_list_w_hunter_id.dat', ax_stis, ax_wfc3)
    cenwave = 3936
    for slit_num in range(1, 18):
        ax_stis = plot_single_slit_locations(slit_num, ax_stis)
        l2, l3 = draw_slit(ax_stis, slit_num)
        add_stars(slit_num, ax_stis, ax_wfc3, im_stis, im_wfc3, cenwave)
        ax_stis = plot_single_slit_locations(slit_num, ax_stis, cenwave, color = 'r')
        l2.set_visible(False)
        l3.set_visible(False)
    pyplot.close()
    #Question - if a star is split between 2 slits do I need to modify my magnitude guess? - code currently does not

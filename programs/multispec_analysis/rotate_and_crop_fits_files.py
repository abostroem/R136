import os
from astropy.io import fits
import shutil
import numpy as np
import pdb

def crop_ccd_images_to_1024(write_dir, data_dir, cenwave):
    '''
    crop all combined dithered images to 1024x1024. This code assumes that files are named
    <slit>_cenwave_combined_img.fits where slit is e.g. SE9, SE8, etc.

    Files taken at 180 degree rotation (NW files) are rotated to match the orientation of
    the SE files and shifted to match the coordinates of the long slit image

    Parameters
    -----------
    write_dir : str
        path where cropped files should be written. This will be created if it does not 
        already exist. The path should be relative to the base repository directory (R136)
        This code assumes it is run from R136/programs/multispec_analysis
    data_dir : str
        path to where the original fits files are stored. Path should be relative to the 
        base repository directory (R136)
    '''
    os.chdir('../../')
    base_dir = os.getcwd()
    target_names = ['SE9', 'SE8', 'SE7', 'SE6', 'SE5', 'SE4', 'SE3', 'SE2', 'SE1', 'NW1', 'NW2', 'NW3', 'NW4', 'NW5', 'NW6', 'NW7', 'NW8']
    flist = [os.path.join(base_dir, data_dir, '{}_{}_combined_img.fits'.format(targ, cenwave)) for targ in target_names]  
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)
    #Copy original file from data_dir to write_dir
    for ifile in flist:
        new_file = os.path.join(write_dir, os.path.basename(ifile))
        shutil.copyfile(ifile, new_file)
        with fits.open(new_file, mode = 'update') as ofile:
            img = ofile[1].data
            orientat = ofile[1].header['orientat']
            new_img = np.empty((1024, 1024))
            if orientat > 0: #right side up
                new_img = img[:1024, :1024]
            else: #upside down
                new_img[13:] = np.rot90(img, k = 2)[:1011]
            ofile[1].data = new_img

if __name__ == "__main__":
    crop_ccd_images_to_1024('multispec/ccd_multispec/cropped_images', '12465_otfr20121109/ccd/', 3936)
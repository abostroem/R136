import drizzlepac
import os
import glob
from datetime import datetime
import shutil


def clean_output_dir(output_dir):
	'''
	Remove files in output_dir so that astrodrizzle can overwrite them
	'''
    if os.path.exists(output_dir):
        flist = glob.glob(os.path.join(output_dir, '*'))
        for ifile in flist:
            os.remove(ifile)
    else:
        os.makedirs(output_dir)
        
        
        
def run_astrodrizzle(rot_angle, plate_scale):
	'''
	Run astrodrizzle on WFC3 image to create a WFC3 image with the STIS rotation and plate scale
	Inputs:
		rot_angle - different between WFC3 image and STIS orientation
		plate_scale - STIS platescale
	Output:
		WFC3 image with STIS rotation and plate scale
	Note: Users will have to modify the first 3 lines to point to their data (line 1), to
		WFC3 reference files (line2), and to the output directory (line 3)
	'''
    os.chdir('/Users/bostroem/science/images/astrodrizzle_wfc3_ccd_platescale')
    os.environ['iref'] = '/Users/bostroem/science/images/astrodrizzle_wfc3_ccd_platescale/iref/'
    output_dir = os.path.join(os.getcwd(), '{:3.2f}_rot'.format(rot_angle))+'/'
    clean_output_dir(output_dir)
    now = datetime.today()
    print now
    drizzlepac.astrodrizzle.AstroDrizzle('*flt.fits', configobj='astrodrizzle_default.cfg', final_rot = rot_angle, final_scale = plate_scale)
    flist = glob.glob('*.???') + glob.glob('*.????')
    for ifile in flist:
        modification_date = datetime.fromtimestamp(os.stat(ifile).st_mtime)
        if modification_date > now:
            shutil.move(ifile, os.path.join(output_dir, ifile))
    flist = glob.glob('OrIg_files/*')
    for ifile in flist:
        shutil.copyfile(ifile, os.path.join(os.getcwd(), os.path.split(ifile)[1]))
        os.chmod(ifile, 0770)
            
if __name__ == "__main__":
	'''
	Run astrodrizzle on WFC3 image to create a WFC3 image with the STIS rotation and plate scale
	Inputs:
		rot_angle - different between WFC3 image and STIS orientation
		plate_scale - STIS platescale
	Output:
		WFC3 image with STIS rotation and plate scale
	Note: Users will have to modify the first 3 lines to point to their data (line 1), to
		WFC3 reference files (line2), and to the output directory (line 3)
	'''
    run_astrodrizzle(63.6, 0.05078)
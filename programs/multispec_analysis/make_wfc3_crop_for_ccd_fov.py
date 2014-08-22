#---------------------------
#Make WFC3 Image with CCD field of view
#---------------------------
import pyraf
from pyraf import iraf
from iraf import images,imcopy as imcopy


def crop_wfc3_img(img_file, xmin, xmax, ymin, ymax, output_filename):
	'''
	Crop WFC3 image to STIS FOV (from xmin:xmax, ymin:ymax) preserving WCS information
	Input:
		img_file: name of input image to be cropeed
		xmin: lower x value to crop to
		xmax: upper x value to crop to
		ymin: lower y value to crop to
		ymax: upper y value to crop to
		output_filename: name (including path) to output file
	'''
	imcopy('{}[{}:{},{}:{}]'.format(img_file,xmin,xmax,ymin,ymax), output_filename)

if __name__ == "__main__":
    #crop_wfc3_img('../../images/astrodrizzle_wfc3_ccd_platescale/63.5_rot/final_drz_sci.fits',  2376+17, 2444+17, 814+17, 1858+17, '../../multispec/ccd_multispec/f336w_63.5_cropped.fits')
    #crop_wfc3_img('../../images/astrodrizzle_wfc3_ccd_platescale/64.06_rot/final_drz_sci.fits' 2376, 2444,, 814, 1858, '../../multispec/ccd_multispec/f336w_64.06_cropped.fits')
    #crop_wfc3_img('../../images/astrodrizzle_wfc3_ccd_platescale/63.6_rot/final_drz_sci.fits', 2376 + 12, 2444 + 12, 814+14, 1858+14, '../../multispec/ccd_multispec/f336w_63.6_cropped.fits')
    #crop_wfc3_img('../../images/astrodrizzle_wfc3_ccd_platescale/63.80_rot/final_drz_sci.fits', 2376 + 8, 2444 + 8, 814+10, 1858+10, '../../multispec/ccd_multispec/f336w_63.8_cropped.fits')
    crop_wfc3_img('../../images/astrodrizzle_wfc3_ccd_platescale/63.70_rot/final_drz_sci.fits', 2376 + 11, 2444 + 11, 814+12, 1858+12, '../../multispec/ccd_multispec/f336w_63.7_cropped_test.fits')
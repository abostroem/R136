from scipy.optimize import curve_fit
import numpy as np
import pyfits
from matplotlib import pyplot
import pdb

def read_in_and_match_stars():
	#read in fits image and display in figure 1 and figure 2
	img_wfc3 = pyfits.getdata('../f336w_crop.fits', 0)
	img_stis = pyfits.getdata('../long_slit_image_wcs.fits', 0)
	fig1 = pyplot.figure(1)
	fig2 = pyplot.figure(2)
	ax1 = fig1.add_subplot(1, 1, 1)
	ax2 = fig2.add_subplot(1,1,1)
	ax1.imshow(np.log10(img_wfc3), interpolation = 'nearest')
	ax2.imshow(np.log10(img_stis), interpolation = 'nearest')
	#read in list of STIS and WFC3 coordinates
	wx, wy = np.genfromtxt('wfc3_coords_from_phot.reg', unpack = True)
	sx, sy = np.genfromtxt('stis_coords_from_phot.reg', unpack = True)
	#Calculate an approximate offset
	print 108.343-166.73
	#Out[10]: -58.386999999999986
	print 945.445-996.519
	#Out[11]: -51.073999999999955
	new_sy = sy - (-51.073999999999955)
	new_sx = sx - (-58.3869999)
	#Open file to write WFC3 and STIS coordinate pairs
	ofile = open('pair_coords.txt', 'w')
	#Loop over each WFC3 star and identify the matching STIS star
	for iwx, iwy in zip(wx, wy):
		l1 = ax1.plot(iwx, iwy, 'bo', markersize = 3)
		indx = np.argsort(np.sqrt((new_sx - iwx)**2 + (new_sy - iwy)**2))
		l2 = ax2.plot(sx[indx[0]], sy[indx[0]], 'k.', markersize = 3)
		pyplot.draw(); correct = raw_input('Is this correct? ')
		i = 0
		while correct != 'y':
			l2[0].set_visible(False)
			ax2.plot(sx[indx[i+1]], sy[indx[i+1]], 'k.', markersize = 3)
			pyplot.draw()
			i = i + 1
			correct = raw_input('Is this correct? ')
		ofile.write('%f\t%f\t%f\t%f\n' %(iwx, iwy, sx[indx[i]], sy[indx[i]]))
		l1[0].set_visible(False)
		l2[0].set_visible(False)
	pyplot.draw()
	pyplot.close()
	pyplot.close()
	ofile.close()

def plot_offset_w_slit_num():
	#Create plot of y offset w/ slit number
	pyplot.figure()
	slit_num = np.int_(np.array(sx)/8.0) + 1
	pyplot.plot(slit_num, wy - np.mean(wy - sy) - sy, '.')
	visit04 = np.where(slit_num < 13)
	y_off = wy - np.mean(wy - sy) - sy
	coeff1 = np.polyfit(slit_num[visit04], y_off[visit04], 1)
	visit05 = np.where(slit_num >=13)
	coeff2 = np.polyfit(slit_num[visit05], y_off[visit05], 1)
	y1 = np.polyval(coeff1, slit_num[visit04])
	y2 = np.polyval(coeff2, slit_num[visit05])
	print 'Slit num fit visit 04: ', coeff1
	print 'Slit num fit visit 05: ', coeff2
	pyplot.plot(slit_num[visit04], y1)
	pyplot.plot(slit_num[visit05], y2)
	pyplot.xlabel('Slit Number')
	pyplot.ylabel('yoffset = stis_y - mean(stis_y - wfc3_y) - wfc3_y')
	pyplot.title('Offset as a function of Slit Number')
	pyplot.savefig('y_off_trend_w_slit_num.pdf')
	pyplot.close()
	return coeff1, coeff2

def gauss_func(x, a0, a1, a2):
    z = (x - a1) / a2
    y = a0 * np.exp(-z**2 / a2)
    return y

def plot_yoffset_histogram(wx, wy, sx, sy):
	#Create Y offset histogram:
	pyplot.figure()
	n, bins, patches = pyplot.hist((wy - np.mean(wy - sy)) - sy, bins = (np.arange(40) - 20.0)/2.0)
	bincenters = 0.5*(bins[1:]+bins[:-1])
	parameters, covariance = curve_fit(gauss_func, bincenters, n)
	fitdata = gauss_func(np.arange(400)/10.0 - 20.0, *parameters)
	pyplot.plot(np.arange(400)/20.0 - 10.0, fitdata)
	print 'gauss_fit parameters for y-offset (amplitude, mean, stdev)', parameters
	pyplot.xlim(-5, 5)
	pyplot.xlabel('yoffset = WFC3_y - mean(WFC3_y - STIS_y) - STIS_y')
	pyplot.ylabel('Number of stars')
	pyplot.title('Average Offset in Y direction based on %i stars' %(len(sx)))
	pyplot.savefig('average_y_offset.pdf')
	pyplot.close()

def plot_xoffset_histogram(wx, wy, sx, sy):
	#Create X offset histogram:
	pyplot.figure()
	n, bins, patches = pyplot.hist((wx - np.mean(wx - sx)) - sx, bins = (np.arange(30) - 15.0)/1.5)
	bincenters = 0.5*(bins[1:]+bins[:-1])
	parameters, covariance = curve_fit(gauss_func, bincenters, n)
	fitdata = gauss_func((np.arange(40) - 20.)/ 4.0, *parameters)
	pyplot.plot((np.arange(40) - 20.)/ 4.0, fitdata)
	print 'gauss_fit parameters x offset (amplitude, mean, stdev)', parameters
	pyplot.ylabel('Number of stars')
	pyplot.xlabel('X Offset = WFC3_x - np.mean(WFC3_x - STIS_x)) - STIS_x')
	pyplot.title('Average Offset in X direction based on %i stars' %(len(sx)))
	pyplot.savefig('average_x_offset.pdf')
	pyplot.close()

def plot_corrected_yoffset_histogram(coeff1, coeff2, wx, wy, sx, sy):
	#Create Y offset histogram:
	pyplot.figure()
	slit_offset = np.empty((0,))

	for i in np.int_(np.array(sx)/8.0) + 1:
		if i < 13:
			slit_offset = np.append(slit_offset, np.polyval(coeff1, i))
		else:	
			slit_offset = np.append(slit_offset, np.polyval(coeff2, i))
	n, bins, patches = pyplot.hist(((wy - np.mean(wy - sy)) - sy) - slit_offset, bins = (np.arange(80) - 40.0)/4.0) #quarter pixel bins
	bincenters = 0.5*(bins[1:]+bins[:-1])
	parameters, covariance = curve_fit(gauss_func, bincenters, n)
	fitdata = gauss_func(np.arange(400)/20.0 - 10.0, *parameters)
	pyplot.plot(np.arange(400)/ 20.0 - 10.0, fitdata)
	print 'gauss_fit parameters for y-offset (amplitude, mean, stdev)', parameters
	pyplot.xlim(-5, 5)
	pyplot.xlabel('Corrected')
	pyplot.ylabel('Number of stars')
	pyplot.title('Average Offset in Y direction based on %i stars after slit shift correction' %(len(sx)))
	pyplot.savefig('average_corrected_y_offset.pdf')
	pyplot.close()

def confirm_offset_correction(coeff1, coeff2, wx, wy, sx, sy):
	#Create plot of y offset w/ slit number
	pyplot.figure()
	slit_offset = np.empty((0,))

	for i in np.int_(np.array(sx)/8.0) + 1:
		if i < 13:
			slit_offset = np.append(slit_offset, np.polyval(coeff1, i))
		else:	
			slit_offset = np.append(slit_offset, np.polyval(coeff2, i))
	pyplot.plot(np.int_(np.array(sx)/8.0) + 1, (wy - np.mean(wy - sy) - sy) - slit_offset, '.')
	pyplot.xlabel('Slit Number')
	pyplot.ylabel('corrected y offset')
	pyplot.title('Offset as a function of Slit Number after slit shift correction')
	pyplot.savefig('conf_y_off_trend_w_slit_num.pdf')
	pyplot.close()


if __name__ == "__main__":
	wx, wy, sx, sy = np.genfromtxt('pair_coords.txt', unpack = True)
	coeff1, coeff2 = plot_offset_w_slit_num()
	plot_yoffset_histogram(wx, wy, sx, sy)
	plot_xoffset_histogram(wx, wy, sx, sy)
	plot_corrected_yoffset_histogram(coeff1, coeff2, wx, wy, sx, sy)
	confirm_offset_correction(coeff1, coeff2, wx, wy, sx, sy)
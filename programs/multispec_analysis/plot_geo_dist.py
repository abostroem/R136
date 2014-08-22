import numpy as np
import pylab
import os
import pdb


def put_origin_at_center(filename, idir, x_off, y_off):
    ofile_r = open(os.path.join(idir, filename), 'r')
    ofile_w = open(os.path.join(idir, filename.replace('.cat', '_offset.cat')), 'w')
    for iline in ofile_r:
        sline = iline.split()
        if sline[0] == 0.0:
            pdb.set_trace()
        ofile_w.write('%4.6f    %4.6f\n' %(float(sline[0]) - x_off, float(sline[1]) - y_off))
    ofile_w.close()
    ofile_r.close()


def make_geo_dist_plot(wfc3_file, stis_file, idir):
    xw, yw = np.genfromtxt(os.path.join(idir, wfc3_file), unpack = True)
    xl, yl = np.genfromtxt(os.path.join(idir, stis_file), unpack = True)

    print 'xl = ', np.shape(xl), 'xw = ', np.shape(xw)
    assert np.shape(xw) == np.shape(xl), 'Error: Input arrays are not the same size'

    xl_new = np.empty((0,))
    yl_new = np.empty((0,))
    xw_new = np.empty((0,))
    yw_new = np.empty((0,))


    pylab.plot(xl, yl, 'bo')
    #pylab.plot(xw, yw, 'ro')
	#Match stars between WFC3 and STIS lists and output lists with stars in the same order
	#make plot
    for ix, iy in zip(xl, yl):
        indx = np.argmin(np.sqrt((xw - ix)**2 + (yw - iy)**2))
        xl_new = np.append(xl_new, ix)
        yl_new = np.append(yl_new, iy)
        xw_new = np.append(xw_new, xw[indx])
        yw_new = np.append(yw_new, yw[indx])

        pylab.plot([ix, xw[indx]], [iy, yw[indx]], 'r-', lw = 2)
        print ix, iy, xw[indx], yw[indx]
        xw = np.append(xw[:indx], xw[indx+1:])
        yw = np.append(yw[:indx], yw[indx+1:])
    write_output_file(xl_new, yl_new, xw_new, yw_new, idir)
        #raw_input()
    #pdb.set_trace()

def write_output_file(xl_new, yl_new, xw_new, yw_new, idir):
    ofile = open(os.path.join(idir, 'geo_dist_loc.dat'), 'w')
    ofile.write('#[1] ID (e.g. a number running from 1 to 91). \n#[2, 3] The two columns in f336w_crop1_final_vetted_offset.cat. \n#[4, 5] The two columns in long_slit1_final_vetted_offset.cat.\n#[5] The slit number where the star has the largest fraction of its flux, starting at 0.\n')
    for i, ixl, iyl, ixw, iyw in zip(range(len(xl_new)), xl_new, yl_new, xw_new, yw_new):
        ofile.write('%3i    %5.2f    %5.2f    %5.2f    %5.2f   %2i\n' %(i, ixw, iyw, ixl, iyl,  np.floor((ixl + 76.570977)/8)))
    ofile.close()
                                         


if __name__ == "__main__":
    geo_dist_dir = '/user/bostroem/science/images/astrodrizzle_wfc3/final'
    put_origin_at_center('long_slit1_final_vetted.cat', geo_dist_dir, 76.570977, 408.18546)
    put_origin_at_center('f336w_crop1_final_vetted.cat', geo_dist_dir, 140.703, 461.39)
    make_geo_dist_plot('f336w_crop1_final_vetted_offset.cat', 'long_slit1_final_vetted_offset.cat', geo_dist_dir)

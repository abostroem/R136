from matplotlib import pyplot
from astropy.io import fits
import glob
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime
import subprocess
import shutil

def make_date_string():
    today_date = datetime.today()
    year = today_date.year
    month = today_date.month
    day = today_date.day
    if (month < 10) and (day < 10):
        date_str = '%i0%i0%i'.format(year, month, day)
    elif (month < 10) and (day >= 10):
        date_str = '%i0%i%i' %(year, month, day)
    elif (day < 10) and (month >= 10):
        date_str = '%i%i0%i'
    else:
        date_str = '%i%i%i' %(year, month, day)
    return date_str

def make_plot(infile, vmin = 0, vmax = 50, pp = None):
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    img = fits.getdata(infile, 1)
    disp = ax.imshow(img, interpolation = 'nearest', vmin = vmin, vmax = vmax, cmap = 'bone')
    plot_spec_loc(ax = ax)
    ax.set_xlim(0, 1024)
    ax.set_ylim(0, 1024)
    ax.set_title(infile)
    if pp:
        pp.savefig()
        pyplot.close()
        return pp
    pyplot.close()

def plot_spec_loc(ax = None):
    if not ax:
        fig = pyplot.figure()
        ax = fig.add_subplot(1,1,1)
    flist_x1d = glob.glob('*star????.fits')
    for ifile in flist_x1d:
        tbdata = fits.getdata(ifile, 1)
        ax.plot(tbdata['X'], tbdata['Y'], 'r--')
    if not ax:
        pyplot.close()
    else:
        return ax

def make_pdf(file_path, prefix):
    exts = ['back_1', 'back_2', 'res_1', 'res_2', 'res_3', 'synt_1', 'synt_2', 'synt_3']
    starting_dir = os.getcwd()
    os.chdir(file_path)
    prefix += '_combined_img_ext001_'
    pdf_obj = PdfPages('{}_preview.pdf'.format(prefix))

    for ext in exts:
        filename = prefix+ext+'.fits'
        pdf_obj = make_plot(filename, pp = pdf_obj)
    pdf_obj.close()
    os.chdir(starting_dir)

def run_multispec(date, crback, ncelly):
    if os.path.exists('{}_crback_{}_ncelly_{}'.format(date, crback, ncelly)):
        shutil.rmtree('{}_crback_{}_ncelly_{}'.format(date, crback, ncelly))
    os.makedirs('{}_crback_{}_ncelly_{}'.format(date, crback, ncelly))
    ofile = open('run_multispec.pro', 'w')
    #ofile.write('@set_path.pro\n')
    #ofile.write('PRO idl_test_runs \n')
    ofile.write('set_path \n')
    #ofile.write("MULTISPEC, 'files.dat', 'slit10_3936_phot2.dat', EXPOS=1, DIR_OUT='{}_crback_{}_ncelly_{}/', DIR_FITS_IN='fits_in/', LIMMAG=17.0, DISPL=[0.0,1e10],
    ofile.write("MULTISPEC, 'files.dat', 'slit10_3936_phot2.dat', EXPOS=1, $ \n")
    ofile.write("\t DIR_OUT='{}_crback_{}_ncelly_{}/', $ \n".format(date, crback, ncelly) )
    ofile.write("\t DIR_FITS_IN='fits_in/', LIMMAG=17.0, DISPL=[0.0,1e10], $ \n")
    ofile.write("\t NPOINTSMIN=[3,5], DELTAMAX=[2.0,0.02], COUNTSMIN=[0.1,200.,200.], $\n ")
    ofile.write("\t COR_OUTPUT='slit10_3936_cor.dat', /COMMONSLOPE, /SIMPLEBACK, $ \n ")
    ofile.write("\t CRBACK = {}, /POSBACK, NCELLX=1024, NCELLY={}, MAXFLUXFAC=10.0, PROC=2 \n ".format(crback, ncelly))
    ofile.write('exit \n')
    #ofile.write('END')
    ofile.close()
    subprocess.call('/Applications/exelis/idl82/bin/idl run_multispec.pro', shell = True)

if __name__ == "__main__":
    os.chdir('../../multispec/grid_test_slit10/')
    crback_range = [1, 15] #ncelly range should always be less than crback
    date = make_date_string()
    for crback in range(crback_range[0], crback_range[1]+1):
        for ncelly in range(1, crback):
            run_multispec(date, crback, ncelly)
            make_pdf('{}_crback_{}_ncelly_{}'.format(date, crback, ncelly), 'NW1_3936')


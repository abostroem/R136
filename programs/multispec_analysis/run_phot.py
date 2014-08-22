import pyraf
from pyraf import iraf
from iraf import digiphot,apphot,daofind as daofind
from iraf import digiphot,apphot,phot as phot
from iraf import digiphot,apphot,datapars as datapars
from iraf import digiphot,apphot,centerpars as centerpars
from iraf import digiphot,apphot,findpars
from iraf import digiphot,apphot,fitskypars
from iraf import digiphot,apphot,photpars

import os

def set_parameters():
    datapars.fwhmpsf = 2.0
    datapars.sigma = 0.05
    datapars.datamin = 0.0
    datapars.datamax = 2000.0
    datapars.exposure = 'TEXPTIME'

    centerpars.calgorithm = 'none'

    fitskypars.salgorithm = 'mode'
    fitskypars.annulus = 8.0
    fitskypars.dannulus = 5.0

    photpars.apertures = 3.0


    findpars.threshold = 75.0

def run_daofind(output = 'f336w_test5.coo'):
    daofind.image = 'f336w_crop.fits[0]'
    daofind.output = output
    daofind()

def run_phot(coords = 'f336_test5.coo', output = 'phot_output_wfc3_sourcelist.mag'):
    phot.image = 'f336w_crop.fits[0]'
    phot.coords = coords
    phot.output = output
    phot()

if __name__ == "__main__":
    os.chdir('/user/bostroem/science/images/astrodrizzle_wfc3/final/add_more_stars')
    set_parameters()
    #run_daofind()
    run_phot(coords = 'f336_test5.coo', output = 'phot_output_wfc3_sourcelist2.mag')

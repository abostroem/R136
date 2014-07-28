@set_path.pro

PRO idl_test_runs
;change CRBACK from 15 to 20

set_path

MULTISPEC, 'files.dat', 'slit10_3936_phot.dat', EXPOS=1, DIR_OUT='out/', DIR_FITS_IN='fits_in/', LIMMAG=17.0, DISPL=[0.0,1e10], $
  NPOINTSMIN=[3,5], DELTAMAX=[2.0,0.02], COUNTSMIN=[0.1,200.,200.], COR_OUTPUT='slit10_3936_cor.dat', /COMMONSLOPE, /SIMPLEBACK, $
  CRBACK=20, /POSBACK, NCELLX=1024, NCELLY=64, MAXFLUXFAC=10.0, PROC=2
  
END
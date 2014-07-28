@set_path.pro
;NCELLY must be a factor of 2^n
;change line 6 procedure name
; change line 11 phot filename
; change line 11 DIR_OUT
PRO idl_final_run2_phot4
;change NCELLY from 16 to 8

set_path

MULTISPEC, 'files.dat', 'slit01_3936_phot4.dat', EXPOS=1, DIR_OUT='out_final1_test_gauss_psf/', DIR_FITS_IN='fits_in/', LIMMAG=17.0, DISPL=[0.0,1e10], $
  NPOINTSMIN=[3,5], DELTAMAX=[2.0,0.02], COUNTSMIN=[0.1,200.,200.], COR_OUTPUT='slit01_3936_cor.dat', /COMMONSLOPE, /SIMPLEBACK, $
   CRBACK = 5, NCELLX=1024, NCELLY=8, MAXFLUXFAC=10.0, PROC=2, GAUSSIAN = [1.13,179.553]
  
END
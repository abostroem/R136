PRO CREATE_4COL_TABLE

;Add double precision

READCOL, 'stis_each_slit_marked_lower_finetune.dat', stis_low_x, stis_low_y, FORMAT = 'D,D'
READCOL, 'stis_each_slit_marked_upper_finetune.dat', stis_hi_x, stis_hi_y, FORMAT = 'D,D'
READCOL, 'wfc3_mark_each_slit_lower_finetune.dat', wfc3_low_x, wfc3_low_y, FORMAT = 'D,D'
READCOL, 'wfc3_mark_each_slit_upper_finetune.dat', wfc3_hi_x, wfc3_hi_y, FORMAT = 'D,D'

z = MRDFITS('f336w_crop.fits', 0, hdr)
EXTAST, hdr, astr

OPENW, 22, 'astrometry_table.dat'

FOR i = 0, N_ELEMENTS(stis_low_x) - 1 DO BEGIN
   XY2AD, wfc3_low_x[i], wfc3_low_y[i], astr, wfc3_low_a, wfc3_low_d
   XY2AD, wfc3_hi_x[i], wfc3_hi_y[i], astr, wfc3_hi_a, wfc3_hi_d
   ra = [wfc3_low_a, wfc3_hi_a]
   dec = [wfc3_low_d, wfc3_hi_d]
   x = [stis_low_x[i], stis_hi_x[i]]
   y = [stis_low_y[i], stis_hi_y[i]]
   STARAST, ra, dec, x, y, cd
   crval = [ra[0], dec[0]]
   crpix = [x[0], y[0]] +1
   MAKE_ASTR, astr_new, cd = cd, crpix = crpix, crval = crval
   GETROT, astr_new, rot, cdel
   ;col1 = SQRT((ra[0]-ra[1])^2 + (dec[0]-dec[1])^2)*60.0D*60.0D  ;check if this is right
   col1 = SQRT((x[0] - x[1])^2 + (y[0] - y[1])^2) *0.0246
   col2 = cdel[1]*60.0D*60.0D 
   col3 = 64.0073D
   col4 = rot
   PRINTF, 22, col1, col2, col3, col4
   ;STOP
ENDFOR
CLOSE, 22
END
   

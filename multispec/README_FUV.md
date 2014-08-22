#Steps to Making FUV Multispec Files

  1. Find the rotation angle between the STIS data and the original (North up) WFC3 image
    1. Use iraf imcopy to crop the WFC3 image to a reasonable size.
    2. ID 2 stars per slit in 2 different slits that as far away from R136a as possible
    3. Make 4 files containing the x and y positions for the upper star WFC3, upper star STIS, lower star WFC3, lower star STIS. Col1 = x, Col2 = y
    4. Run create_4col_table.pro (you will need to modify the input file names to match the files in step 3), to output a table (astrometry_table.dat) with 4 columns: (a) distance in arcseconds between the two stars from the WFC3 image, [b] plate scale in arcseconds/px for the STIS data based on the astrometric solution obtained with those two stars, [c] orientation in degrees (N=0, E=90) based on the WFC3 image, and [d] orientation in degrees based on the astrometric solution.
      1. Column 1: I took the sqrt((x1 - x2)^2 + (y1 - y2)^2) * plate_scale (0.0246 for STIS G140L)
      2. Column 2: I used the positive cdel value from getrot *3600 (it gives the plate scale in degress/pix)
      3. Column 3: The WFC3 image has been rotated so that north is up. The STIS image has not been rotated. I therefore used the average ORIENTAT value from the STIS headers (values range from 64.0079 - 64.0067)
      4. Column 4: I used the rot value from get rot
    5. Check that the plate scale and angle have small errors (For FUV: 63.72±0.06” for angle, 24.626±0.022 for plate scale). Confirm that the plate scale matches the IHB.
  2. Create a WFC3 image with the angle and plate scale found in step 1.5 using drizzle_wfc3_for_ccd.py (note: there is no reason that couldn’t be applied to the MAMA data.
  3. Crop Drizzled WFC3 image to approximately STIS size using make_wfc3_crop_for_stis_fov.py. Modify xmin, xmax, ymin, ymax to match STIS image
  4. Run EXAST.pro on cropped WFC3 image to get WCS keywords. Change CRPIX and use PUTAST.pro to put WCS into STIS pseudo image. This should allow to align in DS9. I’m sorry I don’t have more information on modifying CRPIX, I don’t have the code I used to do this and I don’t have IDL to test it.
  5. Build a distortion map: 
    1. Run DAOFIND and DAOPHOT on the WFC3 cropped image (hereafter referred to as the WFC3 image). Select 50+ bright isolated stars and make a list of their ID and coordinates
    2. Use centroiding with a rectangle of 25 in x and 7 in y (this is for FUV, not sure about CCD) to get STIS positions. I ran DAOFIND on the STIS Pseudo image to get this information.
    3. For each star plot the STIS position and the diff in x and diff in y * 50 using plot_geo_dist.py. This also outputs a file with the format: You may need to check that the slit number is correct here  
      1. [1] ID (e.g. a number running from 1 to 91).
      2. [2] The two columns in f336w_crop1_final_vetted_offset.cat.
      3. [3] The two columns in long_slit1_final_vetted_offset.cat.
      4. [4] The slit number where the star has the largest fraction of its flux.
    4. Make histogram of Delta X and Delta Y (WFC3 - STIS)
    5. Plot the offset Delta Y vs Slit number to look for any drift with time
    6. If there is a trend with slit position, fit it and remove from Delta Y, remake histogram. These histograms tell you how much distortion there is in your images. It should be very small. The precision in X should be about 1/3 of the slit.
    7. Many of these plots are made in the make_pair_coords.py script
  6. Make a file of x_WFC3, y_WFC3, cts_WFC3 (either one from DAOPHOT), slit, y_STIS, x_STISoffset. x_WFC3, y_WFC3, and cts_WFC3 are pretty straightforward. slit is the slit number (let's start with 1, I would need a table with file name - slit number conversions). y_STIS is the y_coordinate in STIS pixels as y_WFC3 + correction. Finally, x_STISoffset is the equivalent to y_STIS but with respect to the center of the slit. As a convention, let's use the FITS one (center of first pixel is 1). For the FUV I created this table using create_multispec_table.py.  This is what the script does behind the scenes: The wfc3_x, wfc3_y, and wfc3_cts are directly from the DAOPHOT output. stis_x_corr_slit_centered = stis_x_corr - ((slit_num - 1.0)*8.0 + 4.5), stis_x = wfc3_x + median(wfc3_x - stis_x) - (slit_num - 1.0)*8 + 4, stis_y = wfc3_y  + median(wfc3_y - stis_y) - delta_y
  7. Here is where I handed things off to Jesús. I believe he took my file and created the _phot.dat files from it. At this point he made the cross-dispersion plots and we added in missing data, corrected points which said they were in one slit but which were really in another, eliminate duplicate sources


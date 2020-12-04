""""
+
 NAME:
   generate_dir_from

 PURPOSE:
   Generate a list of the directories of the galaxy fits files
   in MaNGA data MPL10, make it easier to perform batch processing.
   (Based on the archiving method of MPL10: plate-ifudeisgn)
   
 *** The documentation is for Python 3.0 ***

 CALLING SEQUENCE:
   generate_dir_from, location_of_smapgal_file

 INPUT PARAMETER:
   LOCATION_OF_SAMPLEGAL: string, directory of the MaNGA
       sample file "sampgal_mpl10.fits", default directory
       is "MPL10/sampgal_mpl10.fits"
     - IMPORTANT: The input is the directory of a specifc file,
         just work for MaNGA MPL10.

 OUTPUT PARAMETER:
   GAL_DIR: A list of strings, inwhich each string is a directory
       of a galaxy fits file.

 MODIFICATION HISTORY:
   V1.0.0 -- Created by Pengpei Zhu, 09 Nov 2020

"""
#import some useful modules
#
from astropy.io import fits
import numpy as np


def generate_dir_from(
    location_of_smapgal
):  #the input is a string, filename'MPL10/sampgal_mpl10.fits'

    #open the fits file and show the information of it
    #
    hdul = fits.open(location_of_smapgal)

    #define the binary table and print its header
    #the binary table is a catlog of all 9600 MaNGA galaxies
    #
    bintable = hdul[1]

    #define data from binary table
    data = bintable.data
    #define plate & ifu as string arraies from PLATE & IFUDESIGN column of the table
    plate = data['PLATE'].astype('str')
    ifu = data['IFUDESIGN'].astype('str')

    #generate directories and names for galaxies
    #first define a list of indices representing 9600 galaxies
    #
    indices = list(range(0, len(plate)))

    gal_dir = [
    ]  # then create an empty list to load the location of the files in

    #finally generate the locations, first the dir and then the file name
    #
    for i in indices:
        dapdir = 'MPL10/' + plate[i] + '/' + ifu[i] + '/'
        dapname = 'manga-' + plate[i] + '-' + ifu[
            i] + '-MAPS-SPX-MILESHC-MASTARHC2.fits.gz'
        local = dapdir + dapname
        gal_dir.append(local)

    return gal_dir

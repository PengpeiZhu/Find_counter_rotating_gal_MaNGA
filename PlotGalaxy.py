"""
+
 NAME:
   PLOT_GALAXY

 PURPOSE:
   Plot MaNGA galaxies' stellar velocity map, stellar velocity dispersion map, Ha gas velocity map, and optical image.

 CALLING SEQUENCE:
   PLOT_GALAXY, PLATE, IFU, SAVEFIG

 INPUT PARAMETERS:
   PLATE: MaNGA observation plate
   IFU: integral field unit design
   SAVEFIG: if true then save fig to figures/manga{plate}-{ifu}.png

 OUTPUT PARAMETER:
   NONE, plot the figure and save it

 MODIFICATION HISTORY:
   V1.0.0 -- Created by Pengpei Zhu, 26 Dec 2020
   V1.0.1 -- Added savefig function, 09 Jan 2021
"""
import import_ipynb  # this module makes me able to import ipyb files
import numpy as np
import matplotlib.pyplot as plt
import warnings
from astropy.io import fits


def plot_galaxy(plate, ifu, savefig = False):

    filedir = 'MPL10/' + str(plate) + '/' + str(ifu) + '/' + 'manga-' + str(
        plate) + '-' + str(ifu) + '-MAPS-SPX-MILESHC-MASTARHC2.fits.gz'
    hdu = fits.open(filedir)  #open the file
    svel = hdu[
        'STELLAR_VEL'].data  #Line-of-sight stellar velocity, relative to the input guess redshit
    ssig = hdu[
        'STELLAR_SIGMA'].data  #Raw line-of-sight stellar velocity dispersion
    sivar = hdu[
        'STELLAR_VEL_IVAR'].data  #Inverse variance of stellar velocity measurements.
    smask = hdu[
        'STELLAR_VEL_MASK'].data  #Data quality mask for stellar velocity measurements.
    snr = hdu[
        'SPX_SNR'].data  #Mean g-band weighted signal-to- noise ra!o per pixel.
    gvel = hdu[
        'EMLINE_GVEL'].data  #Line-of-sight emission-line velocity, rela!ve to the input guess redshift
    hdu.close()  #Close the file

    #eleminate the zeros
    svel[svel == 0] = 'nan'
    ssig[ssig == 0] = 'nan'
    gvel[gvel == 0] = 'nan'

    fig = plt.figure(constrained_layout=True, figsize=(16, 16))
    fig.suptitle(str(plate) + '-' + str(ifu), fontsize=20)
    gs = fig.add_gridspec(2, 3)

    ax1 = fig.add_subplot(gs[0, 0])
    im1 = ax1.imshow(svel, cmap='jet', vmin=-150, vmax=150)
    ax1.set_title('Stellar Velocity Map',fontsize = 18)
    fig.colorbar(im1, ax=ax1, shrink=0.55)

    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(ssig, cmap='jet', vmin=0, vmax=250)
    ax2.set_title('Stellar Velocity Dispersion Map',fontsize = 18)
    fig.colorbar(im2, ax=ax2, shrink=0.55)

    ax3 = fig.add_subplot(gs[0, 2])
    im3 = ax3.imshow(gvel[23], cmap='jet', vmin=-150, vmax=150)
    ax3.set_title('Gas Velocity Map',fontsize = 18)
    fig.colorbar(im3, ax=ax3, shrink=0.55)

    image = plt.imread('images_v3_0_1/' + 'SDSS_manga-' + str(plate) + '-' +
                       str(ifu) + '.png')
    ax4 = fig.add_subplot(gs[1, :])
    im4 = ax4.imshow(image)
    ax4.set_title('Galaxy Image',fontsize = 18)
    
    if savefig:
        plt.savefig(f'figures/manga-{plate}-{ifu}.png')

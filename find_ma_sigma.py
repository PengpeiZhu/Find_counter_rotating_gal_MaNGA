"""
+
 NAME:
   FIND_MA_SIGMA

 PURPOSE:
   Determine the velocity dispersion values(sigmas) along
   the major axis of a MaNGA galaxy


 CALLING SEQUENCE:
   FIND_MA_SIGMA, SVEL, SSIG

 INPUT PARAMETERS:
   SVEL: stellar velocity of a MaNGA galaxy, class <numpy.ndarray>
   SSIG: stellar velocity dispersion of a MaNGA galaxy, class <numpy.ndarray>

 OUTPUT PARAMETER:
   MA_SIGMA: the velocity dispersion along the major axis.
        class <list>

 MODIFICATION HISTORY:
   V1.0.0 -- Created by Pengpei Zhu, 14 Nov 2020
   V1.0.1 -- Fixed the bug that for some galaxy PAs ny is out of index range, 20 Nov 2020
   V1.0,2 -- Fixed the bug that some rounded integers are out of bounds, 01 Dec 2020
"""

from fit_kinematic_pa import fit_kinematic_pa  # the Michele Cappellari Pafit Module
import numpy as np
import matplotlib.pyplot as plt


def find_ma_sigma(svel, ssig):

    #those lines of code rearrange the MaNGA data arraies to make them
    #suitable for the Pafit function
    #nx & ny have shape [xx,]; xbin & ybin have shape [xx,xx]
    #
    nx = (np.arange(svel.shape[0]) - svel.shape[0] / 2)
    ny = -(np.arange(svel.shape[1]) - svel.shape[1] / 2)
    xbin, ybin = np.meshgrid(nx, ny, sparse=False, indexing='xy')

    #find the best fitting angle for kinematic major axis
    #
    angBest, angErr, vSyst = fit_kinematic_pa(xbin,
                                              ybin,
                                              svel,
                                              plot=False,
                                              quiet=True)

    #define some trigonometric parameters to find major axis
    #
    rad = np.sqrt(max(nx**2 + ny**2))
    ang = [0, np.pi] + np.radians(angBest)

    #preform a polyfit to find a 1deg func
    #that can describe major axis
    #
    a, b = np.polyfit(-rad * np.sin(ang), rad * np.cos(ang), 1)

    #finally find the stellar velocity dispersions corresponding
    #to the major axis and write in to a list called mavel(major axis vel)
    #
    ma_sigma = []

    #this part is to prevent when angBest is smaller than 45 degree or greater than 135 degree,
    #we can't treat x as an independ variable, instead should use ny as IV.
    if 45. < angBest < 135.:
        for i in nx:
            #use round() here to get the closest int
            #so we can use those ints as indeices to find stellar vel
            #
            x_int = int(
                round(i + svel.shape[0] / 2)
            )  # plus half of svel.shape here for correction on index
            y_int = int(round(a * i + b + svel.shape[1] / 2))

            #this if arguement is for eleminate those rounded ints which are out of bounds
            #
            if y_int < ssig.shape[1] and x_int < ssig.shape[0]:
                sig = ssig[
                    y_int,
                    x_int]  #use x,y as index to find the corresponding sigma values
                ma_sigma.append(sig)

    else:
        for i in ny:
            y_int = int(round(i + svel.shape[1] / 2))
            x_int = int(round((i - b) / a + svel.shape[0] / 2))
            if y_int < ssig.shape[1] and x_int < ssig.shape[0]:
                sig = ssig[y_int, x_int]
                ma_sigma.append(sig)

    #eliminate the zero values
    #
    ma_sigma = [x for x in ma_sigma if x != 0]

    return ma_sigma

"""
SISTER
Space-based Imaging Spectroscopy and Thermal PathfindER
Author: Adam Chlus
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import sys
import numpy as np
import hytools_lite as htl
from hytools_lite.io.envi import WriteENVI
from MDN import image_estimates
from scipy.interpolate import interp1d


HICO_WAVES = [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495,
             501, 507, 512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598,
             604, 610, 616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696,
             701, 707, 713]

def main():
    ''' Estimate chlorophyll A concentration from hyperspectral imagery.

    This function is a wrapper around chlorophyll A MDN estimator from

    https://github.com/STREAM-RS/MDN

    Pahlevan, N., Smith, B., Binding, C., Gurlin,
    D., Li, L., Bresciani, M., & Giardino, C. (2021).
    Hyperspectral retrievals of phytoplankton absorption
    and chlorophyll-a in inland and nearshore coastal waters.
    Remote Sensing of Environment, 253, 112200.

    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('rfl_file', type=str,
                        help='Input reflectance image')
    parser.add_argument('out_dir', type=str,
                          help='Output directory')
    args = parser.parse_args()

    out_dir = args.out_dir+'/' if not args.out_dir.endswith('/') else args.out_dir

    rfl = htl.HyTools()
    rfl.read_file(args.rfl_file,'envi')

    #Use NDVI as a water mask
    ndvi = rfl.ndi()
    ndvi_thres = 0.1

    #Clear system arguments, needed or else error thrown by MDN function
    sys.argv = [sys.argv[0]]

    chl = np.zeros((rfl.lines,rfl.columns))
    iterator =rfl.iterate(by = 'chunk',chunk_size = (500,500))
    while not iterator.complete:
        chunk = iterator.read_next()/np.pi
        water = (ndvi[iterator.current_line:iterator.current_line+chunk.shape[0],
                      iterator.current_column:iterator.current_column+chunk.shape[1]] < ndvi_thres).sum()
        if water > 0:
            interper = interp1d(rfl.wavelengths,chunk)
            hico_chunk = interper(HICO_WAVES)
            chla, idxs  = image_estimates(hico_chunk, sensor='HICO')
            chl[iterator.current_line:iterator.current_line+chunk.shape[0],
                iterator.current_column:iterator.current_column+chunk.shape[1]] = chla[:,:,0]

    #Mask pixels outside of bounds
    chl[ndvi > ndvi_thres] = -9999
    chl[~rfl.mask['no_data']] = -9999

    # Export chlorophyll A map
    chla_header = rfl.get_header()
    chla_header['bands']= 1
    chla_header['band names']= ['chla']
    chla_header['wavelength']= []
    chla_header['fwhm']= []
    chla_header['data ignore value']= -9999
    out_file = "%s/%s_chla" % (out_dir,rfl.base_name)
    writer = WriteENVI(out_file,chla_header)
    writer.write_band(chl,0)

if __name__ == "__main__":
    main()

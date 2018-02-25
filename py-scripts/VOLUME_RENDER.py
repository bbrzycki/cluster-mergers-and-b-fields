import yt
import numpy as np
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, VolumeSource
import glob


full_path_header='/data/mimir/jzuhone/data/fid_mag/1to3_b1/fiducial_1to3_b1_hdf5_plt_cnt_'

data_fns = glob.glob(full_path_header + '0[0-9][0-9][05]')
# Sort them
data_fns.sort()

ts = yt.DatasetSeries(data_fns)
for ds in ts:
    print('Creating scene',str(ds)[-4:])
    sc = yt.create_scene(ds)
    sc.camera.zoom(3.0)
    sc.save('RENDERED_IMAGES/%s.png' % str(ds), sigma_clip=8)
    print('Finishing image',str(ds)[-4:])

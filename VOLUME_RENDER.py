import yt
import numpy as np
from yt.visualization.volume_rendering.transfer_function_helper import TransferFunctionHelper
from yt.visualization.volume_rendering.api import Scene, VolumeSource
import glob


full_path_header="/data/mimir/jzuhone/data/fid_mag/1to1_b0/fiducial_1to1_b0_mag_hdf5_plt_cnt_"

data_fns = glob.glob(full_path_header + "0[0-9][0-9][05]")
# Sort them
data_fns.sort()

ts = yt.DatasetSeries(data_fns)
for ds in ts:
    print("Creating scene",str(ds)[-4:])
    sc = yt.create_scene(ds)
    sc.save('RENDERED_IMAGES/%s.png' % str(ds), sigma_clip=8)
    print("Finishing image",str(ds)[-4:])

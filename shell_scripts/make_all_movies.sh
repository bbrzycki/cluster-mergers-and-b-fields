#!/bin/csh
foreach i (1to1_b0 1to1_b0.5 1to1_b1 1to3_b0 1to3_b0.5 1to3_b1 1to10_b0 1to10_b0.5 1to10_b1)
    set fields=(all_cic density entropy kT magnetic_field_strength)
    foreach field ($fields)
        set match="data_products/mag/${i}/full_slice_plots/${field}_8Mpc/fiducial_${i}_mag_hdf5_plt_cnt_*_Slice_z_${field}.png"
        ffmpeg -r 5 -f image2 -i $match -vcodec libx264 -pix_fmt yuv420p -crf 25 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -y "movies/${i}_${field}_movie.mp4"
    end
    echo $i 
end
#EOF

#ffmpeg -r 5 -f image2 -i "1to3_b1_profiles_%*.png" -vcodec libx264 -pix_fmt yuv420p -crf 25 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -y 1to3_b1_entropy_p.mp4;
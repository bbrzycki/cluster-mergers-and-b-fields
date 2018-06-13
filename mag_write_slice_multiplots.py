import magnolia
import magnolia.magfields

if __name__ == '__main__':

    data_dir = '/data/mimir/jzuhone/data/'
    plot_dir = '../plots'

    sim_names = ['1to1_b0',
                 '1to1_b0.5',
                 '1to1_b1',
                 '1to3_b0',
                 '1to3_b0.5',
                 '1to3_b1',
                 '1to10_b0',
                 '1to10_b0.5',
                 '1to10_b1']

    all_epochs = [['0000','0070','0150','0250','0350','0500'],
                  ['0000','0070','0150','0250','0350','0500'],
                  ['0000','0070','0150','0250','0350','0500'],
                  ['0000','0060','0150','0250','0350','0500'],
                  ['0000','0060','0150','0250','0350','0500'],
                  ['0000','0060','0150','0250','0350','0450'],
                  ['0000','0055','0150','0250','0350','0500'],
                  ['0000','0055','0150','0250','0350','0500'],
                  ['0000','0055','0150','0250','0350','0500']]

    # do all profiles
    for i, sim_name in enumerate(sim_names):

        ds_header_plt_cnt = 'fiducial_%s_mag_hdf5_plt_cnt_' % sim_name
        ds_header_part = 'fiducial_%s_mag_hdf5_part_' % sim_name

        multiplot_info = [['density',ds_header_plt_cnt,1.0e-30,1.0e-25,'arbre',plot_dir+'/'+sim_name+'_density_multiplot.pdf'],
                          ['magnetic_field_strength',ds_header_plt_cnt,1e-10,1e-5,'arbre',plot_dir+'/'+sim_name+'_magnetic_field_strength_multiplot.pdf'],
                          ['kT',ds_header_plt_cnt,0.5,20,'algae',plot_dir+'/'+sim_name+'_kT_multiplot.pdf'],
                          [('deposit','all_cic'),ds_header_part,1e-31,1e-25,'cubehelix',plot_dir+'/'+sim_name+'_all_cic_multiplot.pdf']]

        for (field,ds_header,zlim1,zlim2,cmap,output_fn) in multiplot_info:
            ds_paths = ds_header + all_epochs[i]
            magnolia.make_multiplot(field,ds_paths,zlim1,zlim2,cmap,output_fn)

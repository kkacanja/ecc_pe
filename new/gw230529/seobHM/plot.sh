#pycbc_inference_plot_posterior --input-file ./result_f_boot100.hdf.checkpoint \
#--output-file /home/kkacanja/public_html/ecc_pe/plots/gw230529/gw230529_posteriors_seobHM_norwalk_boot.png \
#--parameters inclination mchirp q spin1z spin2z eccentricity rel_anomaly \
#--z-arg snr \

pycbc_inference_plot_posterior --input-file ./result.hdf \
--output-file /home/kkacanja/public_html/ecc_pe/plots/gw230529/gw230529_posteriors_seobHM_rwalk_coa.png \
--z-arg snr \

#--parameters inclination mchirp q spin1z spin2z eccentricity rel_anomaly \
#--z-arg snr \


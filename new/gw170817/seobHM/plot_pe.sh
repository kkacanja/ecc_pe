#pycbc_inference_plot_posterior --input-file ./result.hdf \
#--output-file /home/kkacanja/public_html/ecc_pe/plots/gw170817/gw170817_posteriors_seobHM_complete.png \
#--parameters inclination mchirp q spin1z spin2z eccentricity rel_anomaly \
#--z-arg snr \


pycbc_inference_plot_posterior --input-file ./result_norwalk.hdf.checkpoint \
--output-file /home/kkacanja/public_html/ecc_pe/plots/gw170817/gw170817_posteriors_seobHM.png \
--parameters inclination mchirp q spin1z spin2z eccentricity rel_anomaly \
--z-arg snr \

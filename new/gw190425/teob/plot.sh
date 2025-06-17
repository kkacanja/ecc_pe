pycbc_inference_plot_posterior --input-file ./result.hdf \
--output-file /home/kkacanja/public_html/ecc_pe/plots/gw190425/gw190425_posteriors_teob.png \
--parameters inclination mchirp q spin1z spin2z eccentricity anomaly \
--z-arg loglikelihood
#--vmin 12.2 --vmax 12.6 \

pycbc_inference_plot_posterior --input-file ./result_25hz.hdf \
--output-file /home/kkacanja/public_html/ecc_pe/plots/gw190425/gw190425_posteriors_teob_25.png \
--parameters inclination mchirp q spin1z spin2z eccentricity anomaly \
--z-arg loglikelihood

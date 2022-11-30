snakemake -j8 vc_target && \
bash ./run-serial.sh relax && \
snakemake -j8 vc_eos && \
snakemake -j8 elast_target && \
bash ./run-serial.sh elast && \
snakemake -j8 elast_dat

# Sniffles_vcf_2_vg_vcf
obatin output from Sniffles and filter with read by vg input
## purpose
get PAVs in your genome from pacbio_mapping_vcf(NGMLR+Sniffles), and merge the vcfs into *vg* to build a graphical based genome.
## dependencies
environment：
### path.os
### vg <https://github.com/vgteam/vg>
### samtools <https://github.com/samtools/samtools>
### ngmlr <https://github.com/philres/ngmlr>
### sniffles <https://github.com/fritzsedlazeck/Sniffles>
## steps
### preparation of input
One step
```
ngmlr -t 8 -r GENOME -q FASTA -o SAM
samtools sort -O BAM -@ 20 -o BAM SAM &
```
Two step
```
sniffles -t 8 -m BAM -v VCF
```
Three step
```
python Sniffles_vcf_2_vg_vcf.py -i VCF -g GENOME
```
### outputs
In a workdir "name", *.normal.sort.reduce.vcf is the final vcf, for a further analysis.

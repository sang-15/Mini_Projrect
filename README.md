# Overview
This is the repository created for COMP483 mini project: <br />
Providing a Python wrapper to investigate if the original *E.coli* K-12 strain from 1922 (Bachmann 1972 (PMID: 4568763)) has been evolved over time.

## Perequisites
- **[Python3](https://www.python.org/)** <br />

  - **[Biopython](https://biopython.org/)** <br />

- **[SRA-Toolkit](https://www.ncbi.nlm.nih.gov/sra)** <br />
For downloading files from NCBI as well as coverting it into the fastq format <br /> 

- **[SPAdes](https://cab.spbu.ru/software/spades/)** <br />
For genome assembly <br />

- **[Prokka](https://github.com/tseemann/prokka)** <br />
For rapid prokaryotic genome annotation <br />

- **[TopHat](https://ccb.jhu.edu/software/tophat/manual.shtml)** <br />
For mapping the reads of the *E.coli* transcriptome project of a K-12 derivative [BW38028](https://www.ncbi.nlm.nih.gov/sra/SRX604287) <br />

  - **[Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)** <br />

- **[Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/)** <br />
For quantifying the transcriptomic expression from the *E.coli* transcriptome project of a K-12 derivative [BW38028](https://www.ncbi.nlm.nih.gov/sra/SRX604287) <br />

  - **[SAM tools](http://samtools.sourceforge.net/)** <br />
 
 
## Running wrapper <br />
Use the following code in the command line <br />
```
python3 EcoliWrapper.py
```

## Output 
The wrapper will generate a 'Results' folder under '$HOME/' directory, and the folder contains the following: <br />

- miniproject.log 
  - Command used for SPAdes
  - The number of contigs with a length > 1000 
  - The length of the assembly
  - Command used for Prokka
  - Discrepancy between Prokka annotation and RefSeq for E. coli K-12 (NC_000913)
- long.fasta 
  - A fasta file containing all contigs with length > 1000
- transcriptome_data.fpkm 
  - A csv format file with seqname, start, end, strand and FPKM for each record.
  - Based on SRR1411276 quantification
- SRR and NC_000913 data
  - SRR8185310
  - SRR1411276
  - NC_000913
- Spade output
- Prokka output
- EcoliK12_index
  - Built via bowtie2 with NC_000913 data
- Tophat output
- Cufflinks output


## Test data
Since all the SRR used for this project are hard coded within the wrapper, so user does not need to supply any information. <br />
However, if it is the case, the user can substitue the SRR in the wrapper to perform relative analysis to that specific SRR. <br />

- SRR8185310:  <br />
Used for conducting assembly and annotation, as well as comparisions to RefSeq for E. coli K-12 (NC_000913)

- SRR1411276:  <br />
Used for mapping and quantification, as well as generating the transcriptome_data.fpkm 

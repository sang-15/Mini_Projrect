# Overview
This is the repository created for COMP483 mini project: providing a Python wrapper to investgate if the original *E.coli* K-12 strain from 1922 (Bachmann 1972 (PMID: 4568763)) has been evolved over time.

## Perequisites
- **[Python3](https://www.python.org/)** <br />

- **[SRA-Toolkit](https://www.ncbi.nlm.nih.gov/sra)** <br />
For downloading files from NCBI as well as coverting it into the fastq format <br /> 

- **[SPAdes](https://cab.spbu.ru/software/spades/)** <br />
For genome assembly <br />

- **[Prokka](https://github.com/tseemann/prokka)** <br />
For rapid prokaryotic genome annotation <br />

- **[TopHat](https://ccb.jhu.edu/software/tophat/manual.shtml)** <br />
For mapping the reads of the *E.coli* transcriptome project of a K-12 derivative [BW38028](https://www.ncbi.nlm.nih.gov/sra/SRX604287) <br />

- **[Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/)** <br />
For quantifying the transcriptomic expression from the *E.coli* transcriptome project of a K-12 derivative [BW38028](https://www.ncbi.nlm.nih.gov/sra/SRX604287) <br />

## Running wrapper <br />
Use the following code in the command line <br />
```
python3 MyWrapper.py
```

## Output 
The wrapper will generate 2 output files <br />
1. A 'DataIput' folder including data downloaded and used during process
2. A 'result' folder including the all output files generated, and a 'miniproject.log' file

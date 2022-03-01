import os
import argparse
import logging
import Bio.SeqIO as SeqIO
import glob
import csv



#Setup

#Create the result folder
os.system('mkdir Results')

#Setup Logging
filename = 'miniproject.log'
path = 'Results/'

log = logging.getLogger()
log.setLevel(logging.DEBUG)

handler = logging.FileHandler(path+filename, 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(message)s'))
log.addHandler(handler)



#Retrieve the Illumina reads for the resequencing of K-12 project from NCBI:
os.system('prefetch -v SRR8185310 --output-directory Results/')

#Convert the sra file into fastq format
os.system('fastq-dump Results/SRR8185310/SRR8185310.sra --outdir Results/SRR8185310/')



#Assembly

#Using SPAdes to assemble the genome
os.system('spades.py -k 55,77,99,127 -s Results/SRR8185310/SRR8185310.fastq -t 2 --only-assembler -o Results/spade_result/')

#Logging command used
log.info('SPAdes was run with the following command to assemble the K12 genome - SRR8185310:')
log.info('spades.py -k 55,77,99,127 -s Results/SRR8185310/SRR8185310.fastq -t 2 --only-assembler -o Results/spade_result/')
log.info(' ')

#Calculate the number of contigs with a length > 1000, calculate the length of the assembly, 
#and write the long contigs into a new file as long.fasta
long = []
count = 0
length = 0
for contig in SeqIO.parse('Results/spade_result/contigs.fasta', 'fasta'):
    if len(contig.seq) > 1000:
        count += 1
        length += len(contig.seq)
        long.append(contig)
            
SeqIO.write(long, 'Results/long.fasta', "fasta")

##Logging the number of long contigs found
log.info('There are ' + str(count) + ' contigs > 1000 in the assembly.')
log.info(' ')

##Logging the length of the assembly with only long contigs
log.info('There are ' + str(length) + ' bp in the assembly.')
log.info(' ')



#Annotation

#Use Prokka to annotate this assembly with Prokka default Escherichia genus database.
os.system('prokka --genus Escherichia --outdir Results/prokka_results/ Results/long.fasta')
#Logging command used
log.info('Prokka was run with following command for annotation:')
log.info('prokka --genus Escherichia --outdir Results/prokka_results/ Results/long.fasta')
log.info(' ')

Logging prokka's results
log.info('The Prokka analysis summary is list as following: ')
log.info(' ')

#Locate the txt file under Prokka
prokka_txt = glob.glob("Results/prokka_results/*.txt")
prokka_txt = ''.join(prokka_txt)

#Open input file text, read input file as a string, remove the empty line at the end and split the input file by line
input_string = open(prokka_txt, 'r').read().rstrip().split('\n')

for i in range(len(input_string)):
    log.info(input_string[i])
    if i == 4:
        trna = input_string[i]
        trna = trna.split(': ')[1]
    elif i == 5:
        cds = input_string[i]
        cds = cds.split(': ')[1]
log.info(' ')

#Calculate the discrepancty found by Prokka to RefSeq for E. coli K-12 (NC_000913), which has 4140 CDS and 89 tRNAs annotated.
trna = int(trna) - 89
cds = int(cds) - 4140

##Logging discrepancy
if trna < 0 and cds < 0:
    log.info('Prokka found ' + str(abs(cds)) + ' less CDS and ' + str(abs(trna)) + ' less tRNA than the RefSeq.')
elif trna > 0 and cds < 0:
    log.info('Prokka found ' + str(abs(cds)) + ' addtional CDS and ' + str(abs(trna)) + ' less tRNA than the RefSeq.')
elif trna < 0 and cds > 0:
    log.info('Prokka found ' + str(abs(cds)) + ' less CDS and ' + str(abs(trna)) + ' additional tRNA than the RefSeq.')
else:
    log.info('Prokka found ' + str(abs(cds)) + ' addtional CDS and ' + str(abs(trna)) + ' additional tRNA than the RefSeq.')    
log.info(' ')



#Mapping

#Download data from RefSeq E. coli K-12 (NC_000913) for building indexes
os.system('wget ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna -P Results/NC_000913/')

#Use bowtie2 to build index with prefix - 'EcoliK12'
os.system('bowtie2-build --threads 2 -q Results/NC_000913/NC_000913.fna EcoliK12')

#Make a new folder under Result to keep all indexes generated
os.system('mkdir Results/EcoliK12_index')
os.system('mv EcoliK12*.bt2l Results/EcoliK12_index/')

#Download data from the E. coli transcriptome project of a K-12 derivative BW38028 
#SRR1411276: https://www.ncbi.nlm.nih.gov/sra/SRX604287
os.system('prefetch -v SRR1411276  --output-directory Results/')

##Convert the sra file into fastq format
os.system('fastq-dump Results/SRR1411276/SRR1411276.sra --outdir Results/SRR1411276/')

#Use Tophat to map reads from SRR1411276 to index, and save the results to 'Results/tophat_out/'
os.system('tophat2 -o Results/tophat_out/ --no-novel-juncs Results/EcoliK12_index/EcoliK12 Results/SRR1411276/SRR1411276.fastq')



#Quantification

#Use Cufflinks to quantify transcriptomic expression and save the output to 'Results/Cufflinks_out/'
os.system('cufflinks -q -p 2 -o Results/Cufflinks_out/ Results/tophat_out/accepted_hits.bam')

#Rewrite the quantified transciptomic expression generated from Crufflinks to 'transcriptome_data.fpkm', which is a
#csv format file with seqname, start, end, strand and FPKM for each record.

fpkm = open('Results/transcriptome_data.fpkm', 'w')
writer = csv.writer(fpkm, delimiter = ',')

with open('Results/Cufflinks_out/transcripts.gtf') as handle:
    reader = csv.reader(handle, delimiter = '\t')
    for row in reader:

        #Split the last column of attributes
        temp = row[-1].split('; ')

        #Save the record of FPKM 
        for att in temp:
            if att.startswith('FPKM '):
                f = att[6:-1]

        #Write the information into 'transcriptome_data.fpkm'        
        new = []
        new.append(row[0])
        new.append(row[3])
        new.append(row[4])
        new.append(row[6])
        new.append(f)
        writer.writerow(new)
        
fpkm.close()

from Bio import SeqIO
from Bio.SeqUtils import GC

a = 1;
#Antwort Teil a
for seq_record in SeqIO.parse("Pluritest_PC_Burn_in_HumGen_16022016_0843_1_ch88_read467_strand_all.fasta", "fasta"):
    print("\n")
    print("Seq Nummer:", a)
    print("Seq ID:", seq_record.id)
    print("Seq Inhalt:", repr(seq_record.seq))
    # print(seq_record.seq)
    print("Seq Länge:", len(seq_record))
    print("GC Gehalt:", GC(seq_record.seq), "%")
    a = a+1

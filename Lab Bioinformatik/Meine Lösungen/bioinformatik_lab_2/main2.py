#Antwort Teil 2 a) c)
import pysam

bamfile = pysam.AlignmentFile("Alignment_Data_sorted.bam", "rb")

position = ""
hoechstWert = 0
for pileupcolumn in bamfile.pileup('burn-in' , 1 ,2):
    #print ("\ncoverage at base %s = %s" %(pileupcolumn.pos, pileupcolumn.n))
    if (pileupcolumn.n > hoechstWert):
        hoechstWert = pileupcolumn.n
        position = pileupcolumn.pos
        print(pileupcolumn)

#print("\ndas Höchste Aligment ist %s in position %s" %(hoechstWert , position))


# Die Ausgabe Zeigt jede coverage von jedem vorhandenen Datensatz
